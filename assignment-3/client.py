import socket
import threading
from concurrent import futures
import time
import json
import sys
import random

from rsa import RSA
import pkda

import pkda_pb2
import pkda_pb2_grpc
import grpc


class ClientServicer(pkda_pb2_grpc.ClientServicer):
    PKDA_ADDRESS = f"[::]:{pkda.PORT}"

    id: str = None
    private_key: str = None
    public_key: str = None
    keystore: dict = {}
    is_inputting: bool = False
    is_ready: bool = False
    my_nonce: str = None
    their_nonce: str = None

    def __init__(self, id: str):
        self.id = id
        self.rsa = RSA()

    def generate_nonce(self):
        return random.randint(0, 2**256)

    def get_client_by_id(self, client_id: str):
        if client_id not in self.keystore or self.keystore[client_id] is None:
            with grpc.insecure_channel(self.PKDA_ADDRESS) as channel:
                stub = pkda_pb2_grpc.PKDAStub(channel)
                response = stub.GetPublicKey(
                    pkda_pb2.PublicKeyRequest(client_id=client_id)
                )
                response = json.loads(response.encrypted_message)
                self.keystore[client_id] = (
                    response if response["client_public_key"] is not None else None
                )
        return self.keystore[client_id]

    def ReceiveMessage(self, request, context):
        if not self.is_ready:
            if not self.is_initiator:
                if not self.my_nonce:
                    message = json.loads(request.encrypted_message)
                    self.destination_client_id = message["source"]
                    self.their_nonce = message["nonce"]
                    self.my_nonce = self.generate_nonce()
                    self.send_message(
                        self.destination_client_id,
                        json.dumps(
                            {
                                "message": json.dumps({"nonce": self.my_nonce}),
                                "nonce": self.their_nonce,
                            }
                        ),
                    )
                else:
                    received_nonce = int(request.encrypted_message)
                    if received_nonce == self.my_nonce:
                        self.is_ready = True
                        print("Connection established!")
            else:
                message = json.loads(request.encrypted_message)
                if message["nonce"] == self.my_nonce:
                    self.their_nonce = json.loads(message["message"])["nonce"]
                    self.send_message(self.destination_client_id, str(self.their_nonce))
                    self.is_ready = True
                    print("Connection established!")
        else:
            if self.is_inputting:
                sys.stdout.write("\r\033[K")
            print(f"< {request.encrypted_message}")
            if self.is_inputting:
                sys.stdout.write("> ")
                sys.stdout.flush()
        return pkda_pb2.BaseResponse(status=pkda_pb2.Status.OK)

    def register_with_pkda(self):
        print("Registering client with PKDA...")
        with grpc.insecure_channel(self.PKDA_ADDRESS) as channel:
            stub = pkda_pb2_grpc.PKDAStub(channel)
            response = stub.RegisterClient(
                pkda_pb2.RegisterClientRequest(
                    client_id=self.id,
                    client_address=self.address,
                    client_public_key=json.dumps(self.rsa.public_key),
                    timestamp=int(time.time()),
                )
            )
            self.pkda_public_key = response.pkda_public_key

    def start_chat(self):
        self.is_initiator = input("Are you the initiator? (y/n) ").lower() == "y"
        if self.is_initiator:
            self.destination_client_id = input("Start chat with: ")
            responder = self.get_client_by_id(self.destination_client_id)
            if responder is None:
                print("[x] Client not found")
                return
            self.my_nonce = self.generate_nonce()
            self.send_message(
                self.destination_client_id,
                json.dumps({"source": self.id, "nonce": self.my_nonce}),
            )
        else:
            print("Getting ready to receive message...")
        while not self.is_ready:
            time.sleep(1)
        while True:
            self.is_inputting = True
            message = input("> ")
            self.is_inputting = False
            self.send_message(self.destination_client_id, message)

    def send_message(self, destination_id: str, message: str = None):
        destination = self.get_client_by_id(destination_id)
        if destination is None:
            print("[x] Client not found")
            return
        dest_public_key, dest_address = (
            destination["client_public_key"],
            destination["client_address"],
        )
        with grpc.insecure_channel(dest_address) as channel:
            stub = pkda_pb2_grpc.ClientStub(channel)
            response = stub.ReceiveMessage(
                pkda_pb2.EncryptedMessage(
                    source=self.id,
                    encrypted_message=message,
                )
            )
            if response.status == pkda_pb2.Status.ERROR:
                print(f"[x] Error sending message: {response.message}")

    def serve(self):
        port = 0
        host = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", port))
            host, port = s.getsockname()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.address = f"{host}:{port}"
        pkda_pb2_grpc.add_ClientServicer_to_server(self, self.server)
        self.server.add_insecure_port(self.address)
        self.server.start()
        print(f"[.] Client {self.id} started on {self.address}")


if __name__ == "__main__":
    client_id = input("Enter client ID: ")
    client = ClientServicer(client_id)
    client.serve()
    client.register_with_pkda()
    client.start_chat()
    client.server.wait_for_termination()

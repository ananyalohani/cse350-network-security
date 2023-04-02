import socket
import threading
from concurrent import futures
import time

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

    def __init__(self, id: str):
        self.id = id
        self.rsa = RSA()

    def SendMessage(self, request, context):
        print(
            f"[.] Received message from Client {request.source}: {request.encrypted_message}")
        return pkda_pb2.Message(
            source=self.id,
            encrypted_message="poop"
        )

    def register_with_pkda(self):
        print("Registering client with PKDA...")
        with grpc.insecure_channel(self.PKDA_ADDRESS) as channel:
            stub = pkda_pb2_grpc.PKDAStub(channel)
            response = stub.RegisterClient(
                pkda_pb2.RegisterClientRequest(
                    client_id=self.id,
                    client_address=self.address,
                    client_public_key=self.rsa.public_key,
                    timestamp=int(time.time())
                )
            )
            self.pkda_public_key = response.pkda_public_key

    def serve(self):
        port = 0
        host = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", port))
            host, port = s.getsockname()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.address = f"{host}:{port}"
        pkda_pb2_grpc.add_ClientServicer_to_server(self, server)
        server.add_insecure_port(self.address)
        server.start()
        print(f"[.] Client {self.id} started on {self.address}")
        return server


if __name__ == "__main__":
    client_id = input("Enter client ID: ")
    client = ClientServicer(client_id)
    server = client.serve()
    client.register_with_pkda()
    server.wait_for_termination()

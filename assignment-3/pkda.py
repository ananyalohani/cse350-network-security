import socket
from rsa import RSA
import time
import json
from concurrent import futures

import pkda_pb2
import pkda_pb2_grpc
import grpc

PORT = 56149


class PKDAServicer(pkda_pb2_grpc.PKDAServicer):
    rsa: RSA = None
    private_key: int = None
    public_key: int = None
    key_store: dict = None

    def __init__(self):
        self.rsa = RSA()
        self.key_store = {}
        print(f"[.] Initialised PKDA with public key: {self.rsa.public_key}")

    def RegisterClient(self, request, context):
        print(f"[.] Received registration request from {request.client_id}")
        if request.client_id in self.key_store:
            return pkda_pb2.RegisterClientResponse(
                pkda_public_key=None, timestamp=int(time.time())
            )
        self.key_store[request.client_id] = (
            request.client_address,
            request.client_public_key,
        )
        return pkda_pb2.RegisterClientResponse(
            pkda_public_key=json.dumps(self.rsa.public_key), timestamp=int(time.time())
        )

    def GetPublicKey(self, request, context):
        requested_client = (
            self.key_store[request.client_id]
            if request.client_id in self.key_store
            else None
        )
        timestamp = int(time.time())
        response = {
            "client_id": request.client_id,
            "client_address": requested_client[0] if requested_client else None,
            "client_public_key": requested_client[1] if requested_client else None,
            "timestamp": timestamp,
        }
        response_string = json.dumps(response)
        # sign = self.rsa.sign(response_string)
        # response_string = json.dumps([response_string, sign])
        # encrypted_response = self.rsa.encrypt(response_string)
        return pkda_pb2.EncryptedMessage(encrypted_message=response_string)

    def serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", PORT))
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.address = f"[::]:{PORT}"
        pkda_pb2_grpc.add_PKDAServicer_to_server(self, self.server)
        self.server.add_insecure_port(self.address)
        self.server.start()
        print(f"[.] PKDA node started on {self.address}")


if __name__ == "__main__":
    pkda = PKDAServicer()
    pkda.serve()
    pkda.server.wait_for_termination()

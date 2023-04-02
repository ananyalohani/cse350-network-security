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
        self.private_key = self.rsa.private_key
        self.public_key = self.rsa.public_key
        self.key_store = {}
        print(f"[.] Initialised PKDA with public key: {self.public_key}")

    def RegisterClient(self, request, context):
        if request.client_id in self.key_store:
            return pkda_pb2.RegisterClientResponse(
                pkda_public_key=None,
                timestamp=int(time.time())
            )

        self.key_store[request.client_id] = (
            request.client_public_key,
            request.client_address
        )
        return pkda_pb2.RegisterClientResponse(
            pkda_public_key=self.public_key,
            timestamp=int(time.time())
        )

    def GetPublicKey(self, request, context):
        response = {
            'client_id': request.client_id,
            'client_public_key': self.key_store[request.client_id][0] if request.client_id in self.key_store else None,
            'timestamp': int(time.time()),
        }
        response_string = json.dumps(response)
        # sign = self.rsa.sign(response_string)
        # response_string = json.dumps([response_string, sign])
        # encrypted_response = self.rsa.encrypt(response_string)
        return pkda_pb2.EncryptedMessage(
            encrypted_response=response_string
        )


def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", PORT))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_address = f"[::]:{PORT}"
    pkda_pb2_grpc.add_PKDAServicer_to_server(
        PKDAServicer(),
        server,
    )
    server.add_insecure_port(server_address)
    server.start()
    print(f"[.] PKDA node started on {server_address}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

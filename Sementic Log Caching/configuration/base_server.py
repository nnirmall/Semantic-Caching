import grpc
from concurrent import futures
import inspect
class BaseGRPCServer:
    def __init__(self, port: str):
        self.port = port
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    def add_servicer(self, add_servicer_fn, servicer):
        add_servicer_fn(servicer, self.server)

    def start(self):
        self.server.add_insecure_port(f"[::]:{self.port}")
        print(f"""gRPC server running on port {self.port} \n""")
        self.server.start()
        self.server.wait_for_termination()

from configuration.base_server import BaseGRPCServer
from core_engine.servicer import EnginerServicer
from core_engine.proto import core_engine_pb2_grpc
import time
import threading


def run_core_engine_server(): 
    print("Please wait...")
    core_engine_server = BaseGRPCServer(port = 50051)
    core_engine_server.add_servicer(
        core_engine_pb2_grpc.add_CoreEngineServiceServicer_to_server,
        EnginerServicer()
    )
   
    core_engine_server.start()




if __name__ == "__main__":
    print("\nStarting Core Engine gRPC Server...\n")
    run_core_engine_server()
   
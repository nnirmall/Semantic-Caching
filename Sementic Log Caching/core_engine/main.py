# from configuration.base_server import BaseGRPCServer
from configuration.base_server import BaseGRPCServer
from core_engine.servicer import EnginerServicer
from core_engine.proto import core_engine_pb2_grpc


def run_core_engine_server(): 
    core_engine_server = BaseGRPCServer(port = 50051)
    core_engine_server.add_servicer(
        core_engine_pb2_grpc.add_CoreEngineServiceServicer_to_server,
        EnginerServicer()
    )
    core_engine_server.start()

    
if __name__ == "__main__": 
    run_core_engine_server()

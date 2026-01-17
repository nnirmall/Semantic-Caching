import grpc
from configuration.config import get_service_address
from gateway.proto import core_engine_pb2_grpc, core_engine_pb2
import inspect

class GRPCStubManager:

    __setup_registry = {
            "CoreEngineService": {
                "engine_name": "ENGINE_ADDR",
                "stub": core_engine_pb2_grpc.CoreEngineServiceStub,
                "methods": core_engine_pb2
                },
            "CoreEngineService2": {
                "engine_name": "ENGINE_ADDR",
                "stub": core_engine_pb2_grpc.CoreEngineServiceStub,
                },
    }
    
    def __init__(self):
        __stack = inspect.stack()
        __caller_name = __stack[1].frame
        __caller_instance = __caller_name.f_locals.get('self')

        if __caller_instance:
            initializer_class = __caller_instance.__class__
            initializer_class_name = initializer_class.__name__
        else:
            initializer_class_name = None

        self.__config = self.__setup_registry.get(initializer_class_name)

    def _getStub(self):
        __engine_addr = get_service_address(self.__config["engine_name"])
        __channel = grpc.insecure_channel(__engine_addr)
        __stub = self.__config["stub"](__channel)
        return __stub

    def _getRequestType(self, request_method: str):
        return self.__config["methods"].__getattribute__(request_method)()
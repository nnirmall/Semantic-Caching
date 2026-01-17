import grpc
from gateway.proto import core_engine_pb2
from gateway.dependencies import GRPCStubManager
from google.protobuf.json_format import MessageToDict

class CoreEngineService:
    def __init__(self):
        try:
            self.__manager = GRPCStubManager()
            self.__stub = self.__manager._getStub()
            self.__request = self.__manager._getRequestType("GetStatsRequest")
        except Exception as e:
            print(f"Error initializing CoreEngineService: {e}")
    
    def get_stats(self):
        try:
            response = self.__stub.GetStatus(self.__request)
            data = MessageToDict(
                response,
                preserving_proto_field_name=True,
                always_print_fields_with_no_presence=True
            )
            return data
        except grpc.RpcError as e:
            print(f"Error calling GetStatus: {e.code()} - {e.details()}")

    
    def post_ingest_log(self, request):
        print("Posting ingest log to Core Engine...")
        try:
            ingest_request = self.__manager._getRequestType("IngestLogRequest")(
                payload=request,
                source=request.source
            )
            response = self.__stub.PostIngestion(ingest_request)
            data = MessageToDict(
                response,
                preserving_proto_field_name=True,
                always_print_fields_with_no_presence=True
            )
            return data
        except grpc.RpcError as e:
            print(f"Error calling IngestLog: {e.code()} - {e.details()}")
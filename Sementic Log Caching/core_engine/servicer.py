


from interface.log_request import LogRequest
import grpc
from google.protobuf.json_format import MessageToDict
from core_engine.services.engine import LogEngine
from core_engine.proto import core_engine_pb2, core_engine_pb2_grpc

class EnginerServicer(core_engine_pb2_grpc.CoreEngineServiceServicer):
    """
        Implementation of the EngineService gRPC service.

        Log Ingesting entrypoint. 
        Accepts logs from ANY source (CLI, Kafka, Code).
    
    """
    # def __init__(self, manager_class):
    #     self.manager = manager_class()
    #     print("[Server] EnginerServicer initialized")

    def IngestLog(self, request: LogRequest, context):
        data = LogEngine().process(request.payload)

        if not data:
            return core_engine_pb2.IngestLogResponse(
                context.set_code(5),
                context.set_details("Ingest not found"),
                status = False,
                action = "failed",
                id = "",
                source = "no source",
               
            )
        return core_engine_pb2.IngestLogResponse(
            status = data.success,
            action = data.action,
            id = data.id,
            source = request.source
        )

    def GetStatus(self, request, context):
        # stats = self.log_engine.get_stats()
        # if not stats:
        #     stats = {"patterns": 0}
        print(f"GetStatus called with request: {request}")
        
        try:
            # Get stats from your business logic
            # stats = LogEngine.GetStats()
            
            total_logs = 0
            compressed_logs = 0
        
            compression_ratio = 0.0

            data = MessageToDict(request)
            print(data)

            response = core_engine_pb2.GetStatsResponse(
                total_logs=str(total_logs),
                compressed_logs=str(compressed_logs),
                compression_ratio=str(compression_ratio)
            )
            
            print(f"Returning response: {response}")
            print(f"Returning response: {type(response)}")


            print("Hey I just want to see if this works" + str(LogEngine().get_stats()))
            return response
            
        except Exception as e:
            print(f"Error in GetStatus: {e}")
            import traceback
            traceback.print_exc()
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error getting stats: {str(e)}')
            return core_engine_pb2.GetStatsResponse()
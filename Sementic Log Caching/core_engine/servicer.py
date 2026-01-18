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
    def __init__(self):
        self.manager_class = LogEngine()
        print("\nCore Engine is up and running...")

    def PostIngestion(self, request, context):

        payload = MessageToDict(
            request,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True
        )
        data = self.manager_class.process(payload)

        if not data:
            return core_engine_pb2.IngestLogResponse(
                context.set_code(5),
                context.set_details("Ingest not found"),
                action = "failed",
                semantic_id = "",
                compression_ratio = " no compression_ratio",
               
            )
        
        return core_engine_pb2.IngestLogResponse(
            action = data['action'],
            semantic_id = data['semantic_id'],
            compression_ratio = data['compression_ratio']
        )

    def GetStatus(self, request, context):

        ## Need to handle null responses from the manager class
        try:
            data = self.manager_class.get_stats()
            if not data:
                return core_engine_pb2.GetStatsResponse(
                    context.set_code(5),
                    context.set_details("Ingest not found"),
                    unique_semantic_patterns = "no unique_semantic_patterns",
                    total_logs_absorbed = "no total_logs_absorbed",
                    compression_rate = " no compression_rate",
                    top_patterns = "no top_patterns"
                
                )
            
            return core_engine_pb2.GetStatsResponse(
                unique_semantic_patterns = data['unique_semantic_patterns'],
                total_logs_absorbed = data['total_logs_absorbed'],
                compression_rate = data['compression_rate'],
                top_patterns = data['top_patterns']
            )
        except Exception as e:
            print(f"Error in GetStatus: {e}")
            import traceback
            traceback.print_exc()
            
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error getting stats: {str(e)}')
            return core_engine_pb2.GetStatsResponse()
import uvicorn
from fastapi import FastAPI
from gateway.services.engine_client import CoreEngineService
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("SemLog Server is starting up...")
    
#     grpc_manager

#     yield
    
#     print("SemLog Server is shutting down...")
#     await app.state.engine_channel.close()

app = FastAPI(title="SemLog: Semantic Log Compressor")
# @app.on_event("shutdown")
# async def shutdown_event():
#     stub_manager.close()

# @app.post("/v1/ingest")
# async def ingest_log(request):
#     """
#     Log Ingesting entrypoint. 
#     Accepts logs from ANY source (CLI, Kafka, Code).
#     """
#     # print("Received ingest log request..."+ request)
#     return CoreEngineService().post_ingest_log(request)
    
@app.get("/stats")
async def stats():
    """
    Stats entrypoint. 
    Returns stats from the core engine.
    """
    return CoreEngineService().get_stats()
   

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
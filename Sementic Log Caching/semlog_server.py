import uvicorn
import re
import time
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict
import chromadb
# from fastembed import TextEmbedding
from chromadb.utils import embedding_functions
app = FastAPI(title="SemLog: Semantic Log Compressor")


# class LightWeightEmbeddingFunction:
#     def __init__(self):
#         # Download a quantized model (~20MB) automatically
#         self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

#     def __call__(self, input):
#         # generating embeddings
#         embeddings_generator = self.model.embed(input)
#         # converting numpy arrays to lists for chromadb compatibility
#         return [e.toList() for e in embeddings_generator]

# print("⚡ Loading Lightweight ONNX Model...")
# emb_fn = LightWeightEmbeddingFunction()

# # Initializing Vector DB

# chroma_client = chromadb.Client()
# log_collection = chroma_client.create_collection(
#     name="log_patterns",
#     embedding_function=emb_fn,
#     metadata={"hnsw:space": "cosine"}
# )

print("🧠 Loading AI Model... (This takes a moment)")
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 2. Initialize Vector DB (In-Memory for this demo)
chroma_client = chromadb.Client()
log_collection = chroma_client.create_collection(
    name="log_patterns",
    embedding_function=emb_fn,
    metadata={"hnsw:space": "cosine"}
)

# Helper Function for LOG MASKING
def mask_log(log_text: str) -> str:
    """
    Pre-processes logs to remove dynamic noise.
    This helps the model to focus on the *structure* of the error.
    """
    # Replace IPs
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP_ADDR>', log_text)
    # Replace Times (HH:MM:SS)
    text = re.sub(r'\d{2}:\d{2}:\d{2}', '<TIME>', text)
    # Replace Integers (like User IDs, Error Codes)
    text = re.sub(r'\b\d+\b', '<NUM>', text)
    # Replace Hex codes (Memory addresses)
    text = re.sub(r'0x[0-9a-fA-F]+', '<HEX>', text)
    return text
    
    
# DATA MODELS
class LogEntry(BaseModel):
    service_name: str
    timestamp: str
    message: str

class LogStats(BaseModel):
    action: str
    semantic_id: str
    compression_ratio: str
    
# API ENDPOINTS

@app.post("/ingest", response_model=LogStats)
async def ingest_log(entry: LogEntry):
    """
    Receives a raw log, masks it, checks for semantic duplicates, and stores it.
    """
    # Masking the log to get its "Skeleton"
    masked_message = mask_log(entry.message)
    
    # Querying Vector DB for this Skeleton
    results = log_collection.query(
        query_texts=[masked_message],
        n_results=1
    )

    # Checking Similarity (Threshold 0.1 means very similar)
    if results['documents'] and results['documents'][0] and results['distances'][0][0] < 0.1:
        
        # DEDUPLICATION EVENT
        existing_id = results['ids'][0][0]
        current_count = results['metadatas'][0][0]['count']
        
        # Updating the counter (Upsert)
        log_collection.update(
            ids=[existing_id],
            metadatas=[{"count": current_count + 1, "example": masked_message}]
        )
        
        return {
            "action": "COMPRESSED",
            "semantic_id": existing_id,
            "compression_ratio": "High (Incremented Counter)"
        }

    else:
        # NEW PATTERN EVENT ---
        new_id = f"pattern_{int(time.time()*1000)}"
        
        log_collection.add(
            documents=[masked_message],
            metadatas=[{"count": 1, "example": entry.message}],
            ids=[new_id]
        )
        
        return {
            "action": "INDEXED_NEW",
            "semantic_id": new_id,
            "compression_ratio": "None (New Pattern Found)"
        }


@app.get("/stats")
def get_stats():
    """Returns the total logs vs unique patterns."""
    data = log_collection.get()
    total_patterns = len(data['ids'])
    
    total_logs_ingested = 0
    patterns = []
    
    for meta, doc in zip(data['metadatas'], data['documents']):
        count = meta['count']
        total_logs_ingested += count
        patterns.append({"pattern": doc, "occurrence_count": count})
        
    return {
        "unique_semantic_patterns": total_patterns,
        "total_logs_absorbed": total_logs_ingested,
        "compression_rate": f"{round((1 - (total_patterns/total_logs_ingested))*100, 1)}%" if total_logs_ingested > 0 else "0%",
        "top_patterns": sorted(patterns, key=lambda x: x['occurrence_count'], reverse=True)
    }
    
    
if __name__ == "__main__":
    print("🚀 SemLog Engine starting on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
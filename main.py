import time
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

import chromadb
from chromadb.utils import embedding_functions

print("Loading model")

emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = "all-MiniLM-L6-v2"
)


#In-memory vector database setup

chroma_client = chromadb.Client()

cache_collection = chroma_client.create_collection(
    name = "semantic_cache",
    embedding_function= emb_fn,
    metadata = {"hnsw:space": "cosine"}
)



#API 

app = FastAPI(title="Semantic Agent")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    data: Dict[str, Any]
    source: str
    latency_ms: float
    similarity_score: Optional[float] = None
    
    
def regular_database_fetch(query_text: str) -> Dict[str, Any]:
    """
    Simulationg a heavy SQL/GraphQL query that takes time 2.0 seconds.
    API upstream
    
    """
    time.sleep(2.0)
    
    if "price" in query_text.lower() and "iphone" in query_text.lower():
        return {"product": "iphone 15", "price": 999, "currency": "USD"}
    elif "weather" in query_text.lower():
        return {"location": "Austin, TX", "temperature": "72F", "condition": "Sunny"}
    elif "ceo" in query_text.lower():
        return {"company": "MobuCorp", "ceo": "Nirmal", "founded": 2025}
    else:
        return {"error": "Data not found in legacy DB", "query_echo": query_text}
        

#Agent Implementation endpoint

@app.post("/query", response_model=QueryResponse)
async def semantic_gateway(request: QueryRequest):
    start_time = time.time()
    
    
    #Checking Vector Cache
    results = cache_collection.query(
        query_texts = [request.query],
        n_results = 1
    )
    
    #if match found or if it is close enough meaning distance < 0.2 means similarity > 0.8


    print(f"Cache query results:::::::::::::::::::::::::::::::: {results}")
    
    if results['documents'] and results['documents'][0] and results['distances'][0][0] < 0.25:
        #cache hit
        
        cached_response_str = results['metadatas'][0][0]['response']
        import json
        cached_data = json.loads(cached_response_str)
        
        elapsed = (time.time() - start_time) * 1000
        return {
            "data": cached_data,
            "source": "SEMANTIC CACHE HIT",
            "latency_ms": round(elapsed, 2),
            "similarity_score": round(1 - results['distances'][0][0], 2)
        }
        
    
    #if cache miss call backend
    
    print(f"Cache miss for: '{request.query}'. Fetching from backend...")
    
    live_data =  regular_database_fetch(request.query)
    
    
    #update cache
    import json
    cache_collection.add(
        documents=[request.query],
        metadatas=[{"response": json.dumps(live_data)}],
        ids = [str(hash(request.query))] 
    )
    
    elapsed = (time.time() - start_time) * 1000
    return {
        "data" : live_data,
        "source" : "Backend (cache Miss)",
        "latency_ms" : round(elapsed, 2)
    }
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
           
        
     
    
    

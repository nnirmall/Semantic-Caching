import re
import json
import time
import chromadb
from chromadb.utils import embedding_functions



class LogEngine:
    def __init__(self):
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name="logs", 
            embedding_function=self.emb_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def mask(self, data: dict) -> str:
        # Simplified universal masker
        text = str(data.get("message") or data.get("msg") or json.dumps(data))
        text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>', text)
        text = re.sub(r'\d+', '<NUM>', text)
        return text

    def process(self, payload: dict):
        masked = self.mask(payload)
        results = self.collection.query(query_texts=[masked], n_results=1)

        if results['documents'] and results['documents'][0] and results['distances'][0][0] < 0.1:
            # Update Existing
            id = results['ids'][0][0]
            count = results['metadatas'][0][0]['count']
            self.collection.update(ids=[id], metadatas=[{"count": count + 1}])
            return {"action": "COMPRESSED", 
                    "semantic_id": id,
                     "compression_ratio": "High (Incremented Counter)"
                    }
        else:
            # Create New
            id = f"log_{int(time.time()*1000)}"
            self.collection.add(
                ids=[id], 
                documents=[masked], 
                metadatas=[{"count": 1}]
            )
            return {"action": "NEW_PATTERN", 
                    "semantic_id": id,
                    "compression_ratio": "None (New Pattern Found)"}

    def get_stats(self):
        data = self.collection.get()
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
        
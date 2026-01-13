Goal: Reduce database load by understanding user intent rather than exact query strings.
Problem: Need to implement securiy in the query search...is the query valid for that specific search?

            For example: Guest users can search: What is the price of iphone 15?
                        BUT they cannot search: Can you list the IMEI numbers of iphone 15? 

Used: 
1. FastAPI to replicate the api implementation
2. Chroma DB for vector database [Could use Redis]
3. Cosine for Similarity Score (server checks for similarity score: if score is low it fetches data from backend else it fetches from cache)


Future implementation:
1. Real database [Check real latency]
2. Security [Policy based? Token Based? Role Based?]
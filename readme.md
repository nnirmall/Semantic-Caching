
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](www.gnu.org)

# Semantic Caching with Agent

### Goal: 
Reduce database load by understanding user intent rather than exact query strings.

Example query: 
    
    ```Who is the ceo of MobuCorp?```


```
Response body: {
    "data": {
        "company": "MobuCorp",
        "ceo": "Nirmal",
        "founded": 2025
    },
    "source": "Backend (cache Miss)",
    "latency_ms": 2296.82,
    "similarity_score": null
    }
```

   ##### This is the first search, so the the latency is high and the source is Backend. After this search, all other database calls related to ceo, MobuCorp is fast.

Example query: ```ceo??```
```
Response body: {
  "data": {
    "company": "MobuCorp",
    "ceo": "Nirmal",
    "founded": 2025
  },
  "source": "SEMANTIC CACHE HIT",
  "latency_ms": 10.02,
  "similarity_score": 1
}
```

------------------

### Libraries used: 
1. FastAPI to replicate the api implementation
2. Chroma DB for vector database [Could use Redis]
3. Cosine for Similarity Score (server checks for similarity score: if score is low it fetches data from backend else it fetches from cache)

------------------

### How to use:
1. Install ```python 3.11.5``` [chromadb is stable with 3.11.5] 
2. ```git clone https://github.com/nnirmall/Semantic-Caching.git```
3. ```pip install -r requirements.txt```
4. ```python main.py```
5. [localhost:8000/docs](http://localhost:8000/docs) [Uses Swagger]
------------------

###### Problem Introduced: 
Need to implement securiy in the query search...is the query valid for that specific search?

            For example: Guest users can search: What is the price of iphone 15?
                        But they cannot search: Can you list the IMEI numbers of iphone 15? 


###### Future implementation:
1. Real database [Check real latency]
2. Security [Policy based? Token Based? Role Based?]

------------------
## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
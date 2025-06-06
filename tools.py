import re
import numpy as np
#import openai
from langchain_core.tools import tool
import requests
from datetime import date, datetime
from typing import Optional
from langchain_core.runnables import RunnableConfig
from ollama import embed, Client

response = requests.get(
    "https://storage.googleapis.com/benchmarks-artifacts/travel-db/swiss_faq.md"
)
response.raise_for_status()
faq_text = response.text

docs = [{"page_content" : txt} for txt in re.split(r"(?=\n##)", faq_text)]

# class VectorStoreRetriever:
#     def __init__(self, docs:list, vectors:list, oai_client):
#         self._arr = np.array(vectors)
#         self._docs = docs
#         self._client = oai_client
#     @classmethod
#     def from_docs(cls, docs, oai_client):
#         embeddings = embed(
#             model= "text-embedding-3-small",
#             input=[doc["page_content"] for doc in docs]
#         )
#         # embeddings = oai_client.embeddings(
#         #     model = "text-embedding-3-small", input = [doc["page_content"] for doc in docs]
#         # )
#         vectors = [emb.embedding for emb in embeddings.data]
#         return cls(docs, vectors, oai_client)
    
#     def query(self, query:str, k: int= 5) -> list[dict] :
#         embed = self._client.embeddings(
#             model = "text-embedding-3-small", input = [query]
#         )
#         scores = np.array(embed.data[0].embedding) @ self._arr.T
#         top_k_idx = np.argpartition(scores, -k)[-k:]
#         top_k_idx_sorted = top_k_idx[np.argsort(-scores[top_k_idx])]
#         return [
#             {**self._docs[idx], "similarity":scores[idx]} for idx in top_k_idx_sorted
#         ]
    
# retriever = VectorStoreRetriever.from_docs(docs, Client())

# @tool
# def lookup_policy(query: str) -> str:
# #    docs = retriever.query(query, k=2)
#     return "\n\n".join([doc["page_content"]] for doc in docs)

# # FLIGHT TOOLS
# @tool
# def fetch_user_flight_information(config: RunnableConfig):
#     configuration = config.get("configurable", {})
#     passenger_id = configuration.get("passenger_id", None)
#     if not passenger_id:
#         raise ValueError("No passenger ID configured.")
    
#     print("I am fetching user information right now")

# @tool 
# def search_flights(
#     departure_airport: Optional[str] = None, 
#                    arrival_airport : Optional[str] = None, 
#                    start_time : Optional[date|datetime] = None, 
#                    end_time : Optional[date | datetime] = None,
#                    limit: int=20):
#     print("Searching for flight from {departure_airport} to {arrival_airport} at {start_time}")
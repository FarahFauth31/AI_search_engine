from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import traceback

class SortingSourcesService:
    """Giving scores to sources using cos similarity scores."""
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def sort_sources(self, query: str, search_results: List[dict]):
        relevant_docs = []
        try:
            query_embedding = self.embedding_model.encode(query)
            for res in search_results:
                content = res.get("content") if res else None
                if not content:
                    continue

                result_embedding = self.embedding_model.encode(content)
                similarity = float(np.dot(query_embedding, result_embedding)/(np.linalg.norm(query_embedding)*np.linalg.norm(result_embedding))) #cosine similarity
                res['similarity_score'] = similarity
                if similarity > 0.4:
                    relevant_docs.append(res)
            
            return sorted(relevant_docs, key=lambda x: x['similarity_score'], reverse=True)
        
        except Exception as e:
            print("Unexpected error in Sorting Sources Service occurred:")
            traceback.print_exc()
            return []
        
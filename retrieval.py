import faiss
import numpy as np
from rank_bm25 import BM25Okapi

class HybridRetriever:
    def __init__(self, doc_store):
        self.doc_store = doc_store
        self.documents = doc_store.get_documents()
        self.embeddings = doc_store.get_embeddings()
        self.bm25 = BM25Okapi([doc.split() for doc in self.documents])
        self._build_faiss()

    def _build_faiss(self):
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings).astype("float32"))

    def retrieve(self, query_embedding, query_text, k=5):
        D, I = self.index.search(
            np.array([query_embedding]).astype("float32"), k
        )
        dense_docs = [self.documents[i] for i in I[0]]

        bm25_scores = self.bm25.get_scores(query_text.split())
        top_bm25 = np.argsort(bm25_scores)[-k:]
        sparse_docs = [self.documents[i] for i in top_bm25]

        combined = list(set(dense_docs + sparse_docs))
        return combined[:k]

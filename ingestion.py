from sentence_transformers import SentenceTransformer
import numpy as np

class DocumentStore:
    def __init__(self, embedding_model):
        self.model = SentenceTransformer(embedding_model)
        self.documents = []
        self.embeddings = None

    def add_documents(self, docs):
        self.documents.extend(docs)
        embeddings = self.model.encode(docs)
        self.embeddings = (
            embeddings if self.embeddings is None
            else np.vstack([self.embeddings, embeddings])
        )

    def get_embeddings(self):
        return self.embeddings

    def get_documents(self):
        return self.documents

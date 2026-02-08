import openai
from config import MODEL_NAME
from utils import count_tokens

class RAGPipeline:
    def __init__(self, retriever, embedding_model):
        self.retriever = retriever
        self.embedding_model = embedding_model

    def generate(self, query):
        query_embedding = self.embedding_model.encode(query)
        contexts = self.retriever.retrieve(query_embedding, query)

        prompt = f"""
Use the following context to answer:

{contexts}

Question: {query}
Answer:
"""

        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )

        answer = response.choices[0].message["content"]
        tokens = count_tokens(prompt + answer)

        return {
            "answer": answer,
            "contexts": contexts,
            "tokens_used": tokens,
        }

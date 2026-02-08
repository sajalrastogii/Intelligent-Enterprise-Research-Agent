def recall_at_k(retrieved_docs, ground_truth_docs):
    hits = sum(1 for doc in retrieved_docs if doc in ground_truth_docs)
    return hits / len(ground_truth_docs)

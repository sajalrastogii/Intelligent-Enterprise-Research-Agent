import json

def evaluate_recall(retrieved, ground_truth):
    hits = sum(1 for r in retrieved if r in ground_truth)
    return hits / len(ground_truth)

def run_regression_tests(test_cases):
    results = []
    for case in test_cases:
        score = evaluate_recall(case["retrieved"], case["ground_truth"])
        results.append(score)
    return results

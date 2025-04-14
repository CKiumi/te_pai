import numpy as np
from te_pai.sampling import sample_from_prob


def test_sample_from_prob_benchmark(benchmark):
    np.random.seed(0)
    raw = np.random.rand(1000, 100, 3)
    probs = raw / raw.sum(axis=2, keepdims=True)
    # Warm-up JIT
    sample_from_prob(probs)
    _ = benchmark(sample_from_prob, probs)

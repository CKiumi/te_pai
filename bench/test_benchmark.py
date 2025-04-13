import numpy as np
from te_pai.hamil import Hamiltonian
import pytest


@pytest.mark.benchmark
def test_spin_chain_benchmark(benchmark):
    n = 6
    freqs = np.ones(n)
    benchmark(lambda: Hamiltonian.spin_chain_hamil(n, freqs))

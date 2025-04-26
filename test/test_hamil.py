import numpy as np

from te_pai.hamil import Hamiltonian


def test_spin_chain_hamil_structure():
    nqubits = 4
    freqs = np.ones(nqubits)
    hamil = Hamiltonian.spin_chain_hamil(nqubits, freqs)
    assert len(hamil.terms) == 16

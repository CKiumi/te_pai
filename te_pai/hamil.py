from dataclasses import dataclass
from itertools import product
import numpy as np
from scipy import integrate
from typing import Callable, List, Tuple
from itertools import product


@dataclass
class Hamiltonian:
    nqubits: int
    terms: List[Tuple[str, List[int], Callable[[float], float]]]

    def __post_init__(self):
        print("The number of qubit:" + str(self.nqubits))
        print("Number of terms in the Hamiltonian:" + str(len(self.terms)))

    @staticmethod
    def spin_chain_hamil(n, freqs):
        def J(t):
            return np.cos(20 * t * np.pi)

        terms = [
            (gate, [k, (k + 1) % n], J)
            for k, gate in product(range(n), ["XX", "YY", "ZZ"])
        ]
        terms += [("Z", [k], lambda t, k=k: freqs[k]) for k in range(n)]
        return Hamiltonian(n, terms)

    @staticmethod
    def trsns_ising(n):
        terms = [("ZZ", [k, (k + 1) % n], lambda t: 1) for k in range(n)]
        terms += [("X", [k], lambda t: 0.2) for k in range(n)]
        return Hamiltonian(n, terms)

    def get_term(self, t):
        return [(term[0], term[1], term[2](t)) for term in self.terms]

    def coefs(self, t: float):
        return [term[2](t) for term in self.terms]

    def l1_norm(self, T: float):
        fn = lambda t: np.linalg.norm(self.coefs(t), 1)
        return integrate.quad(fn, 0, T, limit=100)[0]

    def __len__(self):
        return len(self.terms)

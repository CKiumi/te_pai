from dataclasses import dataclass

import numpy as np
from scipy.stats import binom

from .backend import Simulator


@dataclass
class Trotter:
    def __init__(self, hamil, numQs, T, N, n_snap):
        (self.nq, self.n_snap, self.T, self.N) = (numQs, n_snap, T, N)
        self.L = len(hamil)
        steps = np.linspace(0, T, N + 1)
        self.terms = [hamil.get_term(t) for t in steps]

    def get_lie_PDF(self, points=1000):
        sn = 1000
        x = np.linspace(0, sn, points, dtype=int)
        pdf = binom.pmf(x, sn, self.run()[-1])
        data = [[2 * x / sn - 1, sn / 2 * val] for x, val in zip(x, pdf, strict=False)]
        return zip(*data, strict=False)

    def run(self, err=None):
        gates_arr = []
        n = int(self.N / self.n_snap)
        for i in range(self.N):
            if i % n == 0:
                gates_arr.append([])
            gates_arr[-1] += [
                (pauli, 2 * coef * self.T / self.N, ind)
                for (pauli, ind, coef) in self.terms[i]
            ]
        return Simulator("qulacs").get_probs(self.nq, gates_arr, self.n_snap, err=err)

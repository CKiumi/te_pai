from . import pai, sampling, simulator
from functools import partial
from dataclasses import dataclass
import numpy as np
import multiprocessing as mp
from dataclasses import dataclass
import numpy as np
from scipy.stats import binom
import os
import pandas as pd


@dataclass
class Trotter:

    def __init__(self, hamil, numQs, T, N, n_snap):
        (self.nq, self.n_snap, self.T, self.N) = (numQs, n_snap, T, N)
        self.L = len(hamil)
        steps = np.linspace(0, T, N)
        self.terms = [hamil.get_term(t) for t in steps]

    def get_lie_PDF(self, points=1000, exact=True):
        sn = 1000
        x = np.linspace(0, sn, points, dtype=int)
        pdf = binom.pmf(x, sn, self.lie_trotter(exact)[10])
        data = [[2 * x / sn - 1, sn / 2 * val] for x, val in zip(x, pdf)]
        return zip(*data)

    def lie_trotter(self, err=None):
        noisy = "_noisy" if err is not None else ""
        filename = f"data/lie/lie{self.N}_snap{noisy}_step{self.n_snap}.csv"
        gates_arr = []
        if not os.path.exists(filename):
            n = int(self.N / self.n_snap)
            for i in range(self.N):
                if i % n == 0:
                    gates_arr.append([])
                gates_arr[-1] += [
                    (pauli, 2 * coef * self.T / self.N, ind)
                    for (pauli, ind, coef) in self.terms[i]
                ]
            res = simulator.get_probs(self.nq, gates_arr, self.n_snap, err=err)
            pd.DataFrame(res).to_csv(filename, index=False)
            return res
        else:
            data = pd.read_csv(filename).values
            return data[:, 0]

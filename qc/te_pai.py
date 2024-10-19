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
class TE_PAI:

    def __init__(self, hamil, numQs, Δ, T, N):
        (self.nq, self.Δ, self.T, self.N) = (numQs, Δ, T, N)
        self.L = len(hamil)
        steps = np.linspace(0, T, N)
        angles = [[2 * np.abs(coef) * T / N for coef in hamil.coefs(t)] for t in steps]
        self.gamma = np.prod([pai.gamma(angles[j], self.Δ) for j in N])
        self.probs = [pai.prob_list(angles[i], Δ) for i in range(N)]
        self.terms = [hamil.get_term(t) for t in steps]
        self.overhead = np.exp(2 * hamil.l1_norm(T) * np.tan(Δ / 2))
        self.expected_num_gates = ((3 - np.cos(Δ)) / np.sin(Δ)) * hamil.l1_norm(T)
        self.rea_expect_num_gates = 0
        for prob in self.probs:
            for p in prob:
                self.rea_expect_num_gates += 1 - p[0]

    # Main Algorithm for TE_PAI
    def run_te_pai(self, num_circuits, err=None):
        res = []
        index = sampling.batch_sampling(np.array(self.probs), num_circuits)
        res += mp.Pool(mp.cpu_count()).map(partial(self.gen_rand_cir, err=err), index)
        print(res)
        return np.array(res).transpose(1, 0, 2)

    def gen_rand_cir(self, index, err=None):
        (gates, sign) = ([], 1)
        for i, inde in enumerate(index):
            for j, val in inde:
                (pauli, ind, coef) = self.terms[i][j]
                if val == 3:
                    sign *= -1
                    gates[-1].append((pauli, np.pi, ind))
                else:
                    gates[-1].append((pauli, np.sign(coef) * self.Δ, ind))
        return (sign, gates)

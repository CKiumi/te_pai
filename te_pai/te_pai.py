import multiprocessing as mp
from dataclasses import dataclass
from functools import partial

import numpy as np

from . import pai, sampling
from .backend import Simulator


@dataclass
class TE_PAI:
    def __init__(self, hamil, numQs, Δ, T, N, n_snap, simulator="qulacs"):
        (self.nq, self.n_snap, self.Δ, self.T, self.N) = (numQs, n_snap, Δ, T, N)
        self.simulator = simulator
        self.L = len(hamil)
        steps = np.linspace(0, T, N)
        angles = [[2 * np.abs(coef) * T / N for coef in hamil.coefs(t)] for t in steps]
        n = int(N / n_snap)
        self.gam_list = [1] + [
            np.prod([pai.gamma(angles[j], self.Δ) for j in range((i + 1) * n)])
            for i in range(n_snap)
        ]
        self.gamma = self.gam_list[-1] if N > 0 else 0
        self.probs = [pai.prob_list(angles[i], Δ) for i in range(N)]
        self.terms = [hamil.get_term(t) for t in steps]
        self.overhead = np.exp(2 * hamil.l1_norm(T) * np.tan(Δ / 2))
        self.expected_num_gates = ((3 - np.cos(Δ)) / np.sin(Δ)) * hamil.l1_norm(T)
        self.rea_expect_num_gates = 0
        self.rea_var_num_gates = 0
        for prob in self.probs:
            for p in prob:
                self.rea_expect_num_gates += 1 - p[0]
                self.rea_var_num_gates += p[0] * (1 - p[0])

    def sample_num_gates(self, n):
        res = sampling.batch_sampling(np.array(self.probs), n)
        return [sum(len(r) for r in re) for re in res]

    # Main Algorithm for TE_PAI
    def run_te_pai(self, num_circuits, obs, err=None):
        res = []
        index = sampling.batch_sampling(np.array(self.probs), num_circuits)
        res += mp.Pool(mp.cpu_count()).map(
            partial(self.gen_rand_cir, obs=obs, err=err), index
        )
        return np.array(res).transpose(1, 0, 2)

    def gen_rand_cir(self, index, obs, err=None):
        (gates_arr, sign, sign_list, n) = ([], 1, [], int(self.N / self.n_snap))
        for i, inde in enumerate(index):
            if i % n == 0:
                gates_arr.append([])
                sign_list.append(sign)
            for j, val in inde:
                (pauli, ind, coef) = self.terms[i][j]
                if val == 3:
                    sign *= -1
                    gates_arr[-1].append((pauli, np.pi, ind))
                else:
                    gates_arr[-1].append((pauli, np.sign(coef) * self.Δ, ind))
        sign_list.append(sign)
        data = Simulator("qulacs").get_probs(self.nq, gates_arr, obs, err)
        return np.array(
            [(sign_list[i] * self.gam_list[i], data[i]) for i in range(self.n_snap + 1)]
        )  # type: ignore

from . import pai, sampling, simulator
from functools import partial
from dataclasses import dataclass
import numpy as np
from qiskit import QuantumCircuit
import multiprocessing as mp
import time
from dataclasses import dataclass
import numpy as np
from scipy.stats import binom
import os
import pandas as pd


@dataclass
class Trotter:

    def __init__(self, hamil, numQs, Δ, T, N, n_snap):
        (self.nq, self.n_snap, self.Δ, self.T, self.N) = (numQs, n_snap, Δ, T, N)
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
        for prob in self.probs:
            for p in prob:
                self.rea_expect_num_gates += 1 - p[0]

    def sample_num_gates(self, n):
        res = sampling.batch_sampling(np.array(self.probs), n)
        return [sum(len(r) for r in re) for re in res]

    def get_lie_PDF(self, points=1000, exact=True):
        sn = 1000
        x = np.linspace(0, sn, points, dtype=int)
        pdf = binom.pmf(x, sn, self.lie_trotter(exact)[10])
        data = [[2 * x / sn - 1, sn / 2 * val] for x, val in zip(x, pdf)]
        return zip(*data)

    def gen_rand_cir(self, index, err=None):
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
        data = simulator.get_probs(self.nq, gates_arr, self.n_snap, err)
        return np.array([(sign_list[i] * self.gam_list[i], data[i]) for i in range(self.n_snap + 1)])  # type: ignore

    def lie_trotter(self, exact, err=None):
        N = self.N if exact else int(np.ceil(self.expected_num_gates / self.L))
        noisy = "_noisy" if err is not None else ""
        filename = f"data/lie/lie{N}_snap{noisy}_step{self.n_snap}.csv"
        gates_arr = []
        if not os.path.exists(filename):
            n = int(N / self.n_snap)
            for i in range(N):
                if i % n == 0:
                    gates_arr.append([])
                gates_arr[-1] += [
                    (pauli, 2 * coef * self.T / N, ind)
                    for (pauli, ind, coef) in self.terms[i]
                ]
            res = simulator.get_probs(self.nq, gates_arr, self.n_snap, err=err)
            pd.DataFrame(res).to_csv(filename, index=False)
            return res
        else:
            data = pd.read_csv(filename).values
            return data[:, 0]

    def get_single_rand_cir(self):
        index = sampling.batch_sampling(np.array(self.probs), 1000)
        cor_index = index[0]
        for indexi in index:
            for inde in indexi:
                for j, val in inde:
                    if val == 3 and sum(len(r) for r in indexi) < sum(
                        len(r) for r in cor_index
                    ):
                        cor_index = indexi
        circ = QuantumCircuit(self.nq)
        for i, inde in enumerate(cor_index):
            for j, val in inde:
                (pauli, ind, coef) = self.terms[i][j]
                if val == 3:
                    circ.append(simulator.rgate(pauli, np.pi), ind)
                else:
                    circ.append(simulator.rgate(pauli, np.sign(coef) * self.Δ), ind)
        circ.draw(output="mpl", fold=30).savefig(  # type: ignore
            "fig/quantum_circuit.pdf", bbox_inches="tight"
        )
        return circ

    def run(self, num_circuits, err=None):
        filename = (
            lambda i: f"data/pai_snap{'_noisy' if err is not None else ''}{str(i)}.csv"
        )
        if not os.path.exists(filename(0)):
            res = []
            start = time.time()
            index = sampling.batch_sampling(np.array(self.probs), num_circuits)
            end = time.time()
            print("sampling time:", end - start)
            start = time.time()
            res += mp.Pool(mp.cpu_count()).map(
                partial(self.gen_rand_cir, err=err), index
            )
            end = time.time()
            res = np.array(res).transpose(1, 0, 2)
            print("time:", end - start)
            for i in range(self.n_snap + 1):
                pd.DataFrame(res[i]).to_csv(filename(i), index=False)
            return res
        else:
            return [pd.read_csv(filename(i)).values for i in range(self.n_snap + 1)]

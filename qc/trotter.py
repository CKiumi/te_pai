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
    def __init__(self, hamil, numQs, T, N):
        (self.nq, self.T, self.N) = (numQs, T, N)
        self.L = len(hamil)
        self.terms = [hamil.get_term(t) for t in np.linspace(0, T, N)]

    def run(self):
        gates = []
        for i in range(self.N):
            gates += [
                (pauli, 2 * coef * self.T / self.N, ind)
                for (pauli, ind, coef) in self.terms[i]
            ]
        return simulator.get_expectation_value(self.nq, gates)

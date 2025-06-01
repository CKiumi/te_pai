from .. import Observable
from . import qiskit, qulacs


class Simulator:
    backend: str

    def __init__(self, backend: str):
        self.backend = backend

    def get_probs(self, nq, gates_arr, obs: Observable, err=None):
        if self.backend == "qulacs":
            return qulacs.get_probs(nq, gates_arr, obs.to_qulacs(), err)
        elif self.backend == "qiskit":
            return qiskit.get_probs(nq, gates_arr, obs.to_qiskit(), err)
        else:
            raise RuntimeError("Unsupported backend")

from . import qiskit, qulacs


class Simulator:
    backend: str

    def __init__(self, backend: str):
        self.backend = backend

    def get_probs(self, nq, gates_arr, n_snap, err=None):
        if self.backend == "qulacs":
            return qulacs.get_probs(nq, gates_arr)
        elif self.backend == "qiskit":
            return qiskit.get_probs(nq, gates_arr, n_snap, err)
        else:
            raise RuntimeError("Unsupported backend")

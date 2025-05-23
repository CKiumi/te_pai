import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import RXGate, RXXGate, RYYGate, RZGate, RZZGate
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


def rgate(pauli, r):
    return {
        "X": RXGate(r),
        "Z": RZGate(r),
        "XX": RXXGate(r),
        "YY": RYYGate(r),
        "ZZ": RZZGate(r),
    }[pauli]


def save_x_sv(circ: QuantumCircuit, id):
    circ.save_expectation_value(SparsePauliOp(["X"]), [0], str(id))  # type: ignore


def get_probs(nq, gates_arr, n_snap, err=None):
    circ = QuantumCircuit(nq)
    circ.h(range(nq))
    save_x_sv(circ, 0)
    for i, gates in enumerate(gates_arr):
        for pauli, coef, qubits in gates:
            circ.append(rgate(pauli, coef), qubits)
        save_x_sv(circ, i + 1)
    if err is None:
        sim = AerSimulator(method="statevector")
        data = sim.run(transpile(circ, sim)).result().data()
        # Avoid prob > 1 < 0 due to numerical errors
        return [np.clip((data[str(i)] + 1) / 2, 0, 1) for i in range(n_snap + 1)]  # type: ignore
    else:
        nm = NoiseModel()
        nm.add_all_qubit_quantum_error(depolarizing_error(err[0], 1), ["x", "z"])
        nm.add_all_qubit_quantum_error(
            depolarizing_error(err[1], 2), ["rzz", "ryy", "rxx"]
        )
        sim = AerSimulator(method="density_matrix", noise_model=nm)
        data = sim.run(transpile(circ, sim)).result().data()
        # Avoid prob > 1 < 0 due to numerical errors
        return [np.clip((data[str(i)] + 1) / 2, 0, 1) for i in range(n_snap + 1)]  # type: ignore

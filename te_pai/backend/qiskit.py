import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import RXGate, RXXGate, RYYGate, RZGate, RZZGate
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


def get_probs(nq, gates_arr, obs, err=None):
    circ = QuantumCircuit(nq)
    circ.h(range(nq))
    circ.save_expectation_value(obs, range(nq), str(0))  # type: ignore
    for i, gates in enumerate(gates_arr):
        for pauli, coef, qubits in gates:
            circ.append(rgate(pauli, coef), qubits)
        circ.save_expectation_value(obs, range(nq), str(i + 1))  # type: ignore
    if err is None:
        sim = AerSimulator(method="statevector")
        data = sim.run(transpile(circ, sim)).result().data()
        # Avoid prob > 1 < 0 due to numerical errors
        return [
            np.clip((data[str(i)] + 1) / 2, 0, 1) for i in range(len(gates_arr) + 1)
        ]  # type: ignore
    else:
        nm = NoiseModel()
        nm.add_all_qubit_quantum_error(depolarizing_error(err[0], 1), ["x", "z"])
        nm.add_all_qubit_quantum_error(
            depolarizing_error(err[1], 2), ["rzz", "ryy", "rxx"]
        )
        sim = AerSimulator(method="density_matrix", noise_model=nm)
        data = sim.run(transpile(circ, sim)).result().data()
        # Avoid prob > 1 < 0 due to numerical errors
        return [
            np.clip((data[str(i)] + 1) / 2, 0, 1) for i in range(len(gates_arr) + 1)
        ]  # type: ignore

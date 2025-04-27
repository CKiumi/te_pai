import numpy as np
from qulacs import Observable, QuantumCircuit, QuantumState
from qulacs.gate import RX, RZ, PauliRotation


def rgate(q, pauli, r):
    if len(q) == 1:
        return {"X": RX(q[0], r), "Z": RZ(q[0], r)}[pauli]
    else:
        return {
            "XX": PauliRotation(q, [1, 1], r),
            "YY": PauliRotation(q, [2, 2], r),
            "ZZ": PauliRotation(q, [3, 3], r),
        }[pauli]


def save_x_sv(state: QuantumState):
    obs = Observable(1)
    obs.add_operator(1.0, "X 0")
    return obs.get_expectation_value(state)


def get_probs(nq, gates_arr):
    state = QuantumState(nq)
    circ = QuantumCircuit(nq)
    for i in range(nq):
        circ.add_H_gate(i)
    probs = []
    circ.update_quantum_state(state)
    probs.append(np.clip((save_x_sv(state) + 1) / 2, 0, 1))
    for _, gates in enumerate(gates_arr):
        circ = QuantumCircuit(nq)
        for pauli, coef, qubits in gates:
            circ.add_gate(rgate(qubits, pauli, coef))
        circ.update_quantum_state(state)
        probs.append(np.clip((save_x_sv(state) + 1) / 2, 0, 1))
    return probs

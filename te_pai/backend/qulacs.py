import numpy as np
from qulacs import DensityMatrix, QuantumCircuit, QuantumState
from qulacs.gate import (
    RX,
    RZ,
    DepolarizingNoise,
    PauliRotation,
    TwoQubitDepolarizingNoise,
)


def rgate(q, pauli, r):
    if len(q) == 1:
        return {"X": RX(q[0], -r), "Z": RZ(q[0], -r)}[pauli]
    else:
        return {
            "XX": PauliRotation(q, [1, 1], -r),
            "YY": PauliRotation(q, [2, 2], -r),
            "ZZ": PauliRotation(q, [3, 3], -r),
        }[pauli]


def get_probs(nq, gates_arr, obs, err=None):
    state = QuantumState(nq) if err is None else DensityMatrix(nq)
    probs = []
    circ = QuantumCircuit(nq)
    for i in range(nq):
        circ.add_H_gate(i)
    circ.update_quantum_state(state)
    probs.append(np.clip((obs.get_expectation_value(state) + 1) / 2, 0, 1))
    for _, gates in enumerate(gates_arr):
        circ = QuantumCircuit(nq)
        for pauli, coef, qubits in gates:
            circ.add_gate(rgate(qubits, pauli, coef))
            if err is not None:
                if len(qubits) == 1:
                    circ.add_gate(DepolarizingNoise(qubits[0], err[0]))
                else:
                    circ.add_gate(
                        TwoQubitDepolarizingNoise(qubits[0], qubits[1], err[1])
                    )
        circ.update_quantum_state(state)
        probs.append(np.clip((obs.get_expectation_value(state) + 1) / 2, 0, 1))
    return probs

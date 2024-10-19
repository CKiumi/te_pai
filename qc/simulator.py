from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import RXXGate, RYYGate, RZZGate, RZGate, RXGate


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


def single_shot(nq, gates):
    circ = QuantumCircuit(nq, 1)
    circ.h(range(nq))
    for pauli, coef, qubits in gates:
        circ.append(rgate(pauli, coef), qubits)
    circ.h(0)
    circ.measure(0, 0)
    sim = AerSimulator(method="statevector")
    counts = sim.run(circ, shots=1).result().get_counts()
    res = int(list(counts.keys())[0])  # type: ignore
    return 1 - 2 * res


def get_expectation_value(nq, gates):
    circ = QuantumCircuit(nq)
    circ.h(range(nq))
    for pauli, coef, qubits in gates:
        circ.append(rgate(pauli, coef), qubits)
    circ.save_expectation_value(SparsePauliOp(["X"]), [0], "0")  # type: ignore
    sim = AerSimulator(method="statevector")
    data = sim.run(transpile(circ, sim)).result().data()
    return data["0"]  # type: ignore

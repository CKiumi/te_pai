import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qulacs import GeneralQuantumOperator


class Observable:
    def __init__(
        self, num_qubits: int, terms: list[tuple[float, list[tuple[str, int]]]]
    ):
        """
        Args:
            num_qubits: total number of qubits in the system
            terms: list of tuples like (coeff, [("X", 0), ("Y", 1)])
        """
        self.num_qubits = num_qubits
        self.terms = terms  # list of (coefficient, pauli_ops)

    def __repr__(self):
        return "\n".join(
            [
                f"{coef} * " + " ".join(f"{p}{i}" for p, i in ops)
                for coef, ops in self.terms
            ]
        )

    def to_qiskit(self) -> SparsePauliOp:
        """
        Convert to Qiskit's SparsePauliOp
        """
        pauli_labels = []
        coeffs = []

        for coef, ops in self.terms:
            label = ["I"] * self.num_qubits
            for p, i in ops:
                # Qiskit uses little-endian: qubit 0 is rightmost
                label[self.num_qubits - i - 1] = p
            pauli_labels.append("".join(label))
            coeffs.append(coef)

        return SparsePauliOp(pauli_labels, np.array(coeffs, dtype=complex))

    def to_qulacs(self) -> GeneralQuantumOperator:
        qop = GeneralQuantumOperator(self.num_qubits)
        for coef, ops in self.terms:
            pauli_str = " ".join(f"{p} {i}" for p, i in ops)
            qop.add_operator(coef, pauli_str)
        return qop

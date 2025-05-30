from qiskit.quantum_info import SparsePauliOp
from qulacs import GeneralQuantumOperator

from te_pai.observable import Observable


def test_custom_observable():
    obs = Observable(3, [(0.5, [("X", 0), ("Y", 1)]), (1.2, [("Z", 2)])])
    qiskit_res = SparsePauliOp.from_list(
        [
            ("IYX", 0.5),
            ("ZII", 1.2),
        ]
    )
    expected_op = GeneralQuantumOperator(3)
    expected_op.add_operator(0.5, "X 0 Y 1")
    expected_op.add_operator(1.2, "Z 2")
    assert obs.to_qiskit() == qiskit_res
    assert str(obs.to_qulacs()) == str(expected_op)

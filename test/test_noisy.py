import numpy as np

from te_pai import Observable
from te_pai.backend import Simulator

nq = 3
gates_arr = [
    [
        ("Z", np.pi / 4, [0]),
        ("X", np.pi / 6, [1]),
        ("XX", np.pi / 4, [0, 1]),
        ("YY", np.pi / 3, [1, 2 % nq]),
        ("ZZ", np.pi / 5, [2 % nq, 3 % nq]),
    ],
    [
        ("X", np.pi / 7, [1]),
        ("Z", np.pi / 6, [2 % nq]),
        ("XX", np.pi / 2, [0, 2 % nq]),
        ("YY", np.pi / 8, [1, 3 % nq]),
    ],
    [
        ("Z", np.pi / 9, [0]),
        ("X", np.pi / 4, [1]),
        ("XX", np.pi / 3, [0, 1]),
        ("ZZ", np.pi / 6, [2 % nq, 0]),
    ],
]

obs = Observable(nq, [(1, [("Y", 0)])])


def test_backends():
    probs1 = Simulator("qulacs").get_probs(nq, gates_arr, obs, None)
    probs2 = Simulator("qiskit").get_probs(nq, gates_arr, obs, None)
    assert np.allclose(probs1, probs2)


def test_backends_noisy():
    probs1 = Simulator("qulacs").get_probs(nq, gates_arr, obs, [0.01, 0.1])
    probs2 = Simulator("qiskit").get_probs(nq, gates_arr, obs, [0.01, 0.1])
    diffs = [np.abs(p1 - p2) for p1, p2 in zip(probs1, probs2, strict=False)]
    assert all(diff < 0.1 for diff in diffs), f"Differences too large: {diffs}"

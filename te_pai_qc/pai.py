import numpy as np


def prob_list(angles, Δ):
    probs = [abc(θ, (1 if θ >= 0 else -1) * Δ) for θ in angles]
    return [list(np.abs(probs) / np.sum(np.abs(probs))) for probs in probs]


def abc(θ, Δ):
    a = (1 + np.cos(θ) - (np.cos(Δ) + 1) / np.sin(Δ) * np.sin(θ)) / 2
    b = np.sin(θ) / np.sin(Δ)
    c = (1 - np.cos(θ) - np.sin(θ) * np.tan(Δ / 2)) / 2
    return np.array([a, b, c])


def gamma(angles, Δ):
    gam = [
        (np.cos((np.sign(θ) * Δ / 2) - θ)) / np.cos(np.sign(θ) * Δ / 2) for θ in angles
    ]
    return np.prod(np.array(gam))

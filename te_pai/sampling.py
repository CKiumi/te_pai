from numba import jit
import numpy as np
import multiprocessing as mp
from scipy.stats import binom


@jit(nopython=True)
def custom_random_choice(prob):
    r = np.random.random()
    cum_prob = 0.0
    for idx in range(len(prob)):
        cum_prob += prob[idx]
        if r < cum_prob:
            return idx + 1


@jit(nopython=True)
def sample_from_prob(probs):
    res = []
    for i in range(probs.shape[0]):
        res2 = []
        for j in range(probs.shape[1]):
            val = custom_random_choice(probs[i][j])
            if val != 1:
                res2.append((j, val))
        res.append(res2)
    return res


def batch_sampling(probs, batch_size):
    return mp.Pool(mp.cpu_count()).map(sample_from_prob, [probs] * batch_size)


def resample(res):
    s = np.concatenate([c * (2 * binom.rvs(1, p, size=100) - 1) for (c, p) in res])
    choices = np.reshape(s[np.random.choice(len(s), 1000 * 10000)], (10000, 1000))
    return np.mean(choices, axis=1)
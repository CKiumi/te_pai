import time

import numpy as np

from te_pai.hamil import Hamiltonian
from te_pai.sampling import resample
from te_pai.te_pai import TE_PAI
from te_pai.trotter import Trotter

if __name__ == "__main__":
    start = time.time()
    # Parameters for the example
    numQs = 7  # Number of qubits
    Δ = np.pi / (2**6)  # Delta parameter
    T = 1  # Total evolution time
    N = 2000  # Number of Trotter steps
    n_snapshot = 10  # Number of snapshots
    np.random.seed(42)
    rng = np.random.default_rng(0)
    freqs = rng.uniform(-1, 1, size=numQs)
    # Initialize Hamiltonian and Trotter simulation
    # Assuming a spin chain Hamiltonian constructor
    hamil = Hamiltonian.spin_chain_hamil(numQs, freqs, 20)
    te_pai = TE_PAI(hamil, numQs, Δ, T, N, n_snapshot)
    # Print expected number of gates and overhead
    print("Expected number of gates:", te_pai.expected_num_gates)
    print("Measurement overhead:", te_pai.overhead)

    # Run the TE-PAI simulation and resample the results
    res = [resample(data) for data in te_pai.run_te_pai(1000)]
    end = time.time()
    print("Time taken:", end - start)
    # Compute mean and standard deviation for the resampled data
    mean, std = zip(*[(np.mean(y), np.std(y)) for y in res], strict=False)

    print("Means of TE-PAI result:", [round(float(x), 3) for x in mean])
    print("Standard deviations of TE-PAI result:", [round(float(x), 3) for x in std])
    # Use Lie Trotter to run the simulation
    trotter = Trotter(hamil, numQs, T, N, n_snapshot)
    res = [2 * prob - 1 for prob in trotter.run()]
    mean, std = zip(*[(np.mean(y), np.std(y)) for y in res], strict=False)
    print("Means of Trotter result:", [round(float(x), 3) for x in mean])

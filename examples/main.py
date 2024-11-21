from te_pai.hamil import Hamiltonian
from te_pai.trotter import Trotter
from te_pai.te_pai import TE_PAI
from te_pai.sampling import resample
import numpy as np

if __name__ == "__main__":
    # Parameters for the example
    numQs = 7  # Number of qubits
    Δ = np.pi / (2**6)  # Delta parameter
    T = 1  # Total evolution time
    N = 2000  # Number of Trotter steps
    n_snapshot = 10  # Number of snapshots
    rng = np.random.default_rng(0)
    freqs = rng.uniform(-1, 1, size=numQs)
    # Initialize Hamiltonian and Trotter simulation
    # Assuming a spin chain Hamiltonian constructor
    hamil = Hamiltonian.spin_chain_hamil(numQs, freqs)
    te_pai = TE_PAI(hamil, numQs, Δ, T, N, n_snapshot)

    # Print expected number of gates and overhead
    print("Expected number of gates:", te_pai.expected_num_gates)
    print("Measurement overhead:", te_pai.overhead)

    # Run the TE-PAI simulation and resample the results
    res = [resample(data) for data in te_pai.run_te_pai(10000)]
    # Compute mean and standard deviation for the resampled data
    mean, std = zip(*[(np.mean(y), np.std(y)) for y in res])

    print("Means of TE-PAI result:", mean)
    print("Standard deviations of TE-PAI result:", std)

    # Use Lie Trotter to run the simulation
    trotter = Trotter(hamil, numQs, T, N, n_snapshot)
    res = [2 * prob - 1 for prob in trotter.run()]
    mean, std = zip(*[(np.mean(y), np.std(y)) for y in res])
    print("Means of Trotter result:", mean)

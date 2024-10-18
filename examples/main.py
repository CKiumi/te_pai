from te_pai.hamil import Hamiltonian
from te_pai.trotter import Trotter
from te_pai.sampling import resample
import numpy as np

if __name__ == "__main__":
    # Parameters for the example
    numQs = 7  # Number of qubits
    Δ = np.pi / (2**6)  # Delta parameter
    T = 1  # Total evolution time
    N = 2000  # Number of Trotter steps
    n_snapshot = 10  # Number of snapshots
    freqs = np.random.uniform(-1, 1, size=numQs)  # Random frequencies for spin chain

    # Initialize Hamiltonian and Trotter simulation
    # Assuming a spin chain Hamiltonian constructor
    hamil = Hamiltonian.spin_chain_hamil(numQs, freqs)
    trotter = Trotter(hamil, numQs, Δ, T, N, n_snapshot)

    # Print expected number of gates and overhead
    print("Expected number of gates:", trotter.expected_num_gates)
    print("Measurement overhead:", trotter.overhead)

    # Run the Trotter simulation and resample the results
    res = [resample(data) for data in trotter.run_te_pai(100)]

    # Compute mean and standard deviation for the resampled data
    mean, std = zip(*[(np.mean(y), np.std(y)) for y in res])

    print("Means of resampled data:", mean)
    print("Standard deviations of resampled data:", std)

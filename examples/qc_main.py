from qc.hamil import Hamiltonian
from qc.te_pai import TE_PAI
import numpy as np

if __name__ == "__main__":
    # Parameters for the example
    numQs = 7  # Number of qubits
    Δ = np.pi / (2**6)  # Delta parameter
    T = 1  # Total evolution time
    N = 2000  # Number of Trotter steps
    freqs = np.random.uniform(-1, 1, size=numQs)  # Random frequencies for spin chain

    # Initialize Hamiltonian and Trotter simulation
    # Assuming a spin chain Hamiltonian constructor
    hamil = Hamiltonian.spin_chain_hamil(numQs, freqs)
    trotter = TE_PAI(hamil, numQs, Δ, T, N)

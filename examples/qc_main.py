from qc.hamil import Hamiltonian
from qc.te_pai import TE_PAI
from qc.trotter import Trotter
import numpy as np

if __name__ == "__main__":
    # Parameters for the example
    numQs = 7  # Number of qubits
    Δ = np.pi / (2**6)  # Delta parameter
    T = 1  # Total evolution time
    N = 2000  # Number of Trotter steps
    rng = np.random.default_rng(0)
    freqs = rng.uniform(-1, 1, size=numQs)  # Random frequencies for spin chain

    # Initialize Hamiltonian and Trotter simulation
    # Assuming a spin chain Hamiltonian constructor
    hamil = Hamiltonian.spin_chain_hamil(numQs, freqs)
    te_pai = TE_PAI(hamil, numQs, Δ, T, N)
    res1 = te_pai.run_te_pai(10000)

    # use Lie Trotter to run the simulation
    trotter = Trotter(hamil, numQs, T, N)
    res2 = trotter.run()

    # The two results should be similar
    print(res1, res2)

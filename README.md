# TE_PAI

## Features

- Implements **PAI-based exact Trotter simulation** for quantum circuits, based on the paper "TE-PAI: Exact Time Evolution by Sampling Random Circuits" [📄 arXiv:2410.16850](https://arxiv.org/abs/2410.16850).

---

## 🚀 Run Examples

To run the included example (`examples/main.py`) using [📚 Poetry](https://python-poetry.org/), follow these steps:

1. **Install dependencies:**

   ```bash
   poetry install
   ```

2. **Run the example script:**

   ```bash
   poetry run python examples/main.py
   ```

---

## 📦 Installation

### Install with `pip`

1. Install in **editable** mode (recommended for development):

   ```bash
   pip install -e .
   ```

2. Or regular installation:
   ```bash
   pip install .
   ```

## 🧪 Usage

Once installed, you can use the package in Python scripts or notebooks like so:

```python
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
    hamil = Hamiltonian.spin_chain_hamil(numQs, freqs)
    te_pai = TE_PAI(hamil, numQs, Δ, T, N, n_snapshot)

    # Print expected number of gates and overhead
    print("Expected number of gates:", te_pai.expected_num_gates)
    print("Measurement overhead:", te_pai.overhead)

    # Run the TE-PAI simulation and resample the results
    res = [resample(data) for data in te_pai.run_te_pai(10000)]
    mean, std = zip(*[(np.mean(y), np.std(y)) for y in res])

    print("Means of TE-PAI result:", mean)
    print("Standard deviations of TE-PAI result:", std)

    # Use Lie Trotter to run the simulation
    trotter = Trotter(hamil, numQs, T, N, n_snapshot)
    res = [2 * prob - 1 for prob in trotter.run()]
    mean, std = zip(*[(np.mean(y), np.std(y)) for y in res])
    print("Means of Trotter result:", mean)
```

## 🧪 Testing with `pytest`

This project uses [`pytest`](https://docs.pytest.org/) for unit testing. All test files are located in the `tests/` directory.

### ✅ Running Tests

If you're using [Poetry](https://python-poetry.org/):

```bash
poetry install
poetry run pytest -s
```

### ✅ Running Benchmarks

If you're using [Poetry](https://python-poetry.org/):

```bash
poetry install
poetry run pytest test/benchmark.py
```

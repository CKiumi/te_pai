# TE_PAI

## Features

- Implement PAI based exact trotter simulation

## Installation

### Local Installation

To install `te_pai` locally from the source, follow these steps:

1. Navigate to the project directory:

   ```bash
   cd te_pai
   ```

2. Install the package using `pip` in **editable** mode (recommended for development purposes):

   ```bash
   pip install -e .
   ```

   - The `-e` flag installs the package in "editable" mode, allowing you to make changes to the source code without reinstalling the package.

3. (Optional) If you prefer to install without the `-e` flag for a regular installation:
   ```bash
   pip install .
   ```

## Usage

Once installed, you can use the package in your Python scripts or notebooks.

```python
from te_pai import Hamiltonian, Trotter, plot

# Example: Initialize a Hamiltonian and perform Trotterization
nq = 5  # Number of qubits
hamil = Hamiltonian.spin_chain_hamil(nq)
trotter = Trotter(hamil, nq, delta=np.pi / 4, time=1.0, steps=10, order=2)
res = [resample(data) for data in trotter.run(10000)]
mean, std = zip(*[(np.mean(y), np.std(y)) for y in y3])
print(mean, std)
```

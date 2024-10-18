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
(numQs, Δ, T, N, n_snapshot) = (7, np.pi / (2**6), 1, 2000, 10)
hamil = Hamiltonian.spin_chain_hamil(numQs, freqs)
trotter = Trotter(hamil, numQs, Δ, T, N, n_snapshot)
print(trotter.expected_num_gates)
print(trotter.overhead)
res = [resample(data) for data in trotter.run_te_pai(100)]
mean, std = zip(*[(np.mean(y), np.std(y)) for y in res])
# mean[-1] stores the mean value at T=1.
print(mean[-1], std[-1])
```

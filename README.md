# TE_PAI

## Features

- Implements **PAI-based exact Trotter simulation** for quantum circuits, based on the paper "TE-PAI: Exact Time Evolution by Sampling Random Circuits" [📄 arXiv:2410.16850](https://arxiv.org/abs/2410.16850).

---

## 🚀 Run Examples

To run the included example (`examples/main.py`) using **uv**, follow these steps:

1. **Sync dependencies:**

   ```bash
   uv sync
   ```

2. **Run the example script:**

   ```bash
   uv run python examples/main.py
   ```

([github.com](https://github.com/astral-sh/uv/issues/10813?utm_source=chatgpt.com))

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

### Development mode with **uv**

To install the package in editable mode and manage dependencies with **uv**:

```bash
uv tool install . -e
```

---

## 🧪 Testing with `pytest`

All test files are located in the `tests/` directory.

1. **Sync dependencies (including any extras):**

   ```bash
   uv sync --all-extras
   ```

2. **Run tests:**

   ```bash
   uv run pytest -s
   ```

### ✅ Running Benchmarks

```bash
uv run pytest test/benchmark.py
```

from setuptools import setup, find_packages

setup(
    name="te_pai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.26.4",
        "scipy>=1.13.1",
        "qiskit>=1.1.0",
        "qiskit_aer>=0.14.1",
    ],
    description="Python implementaion of TE-PAI",
    license="MIT",
    python_requires=">=3.6",
)

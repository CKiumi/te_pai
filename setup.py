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
    author="Chusei Kiumi",
    author_email="c.kiumi.qiqb@osaka-u.ac.jp",
    description="Python implementaion of TE-PAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

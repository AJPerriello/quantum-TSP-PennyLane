# quantum-TSP-PennyLane
NP-Complete Traveling Salesman Program Quantum Approach

# Quantum Travelling Salesperson Problem (TSP) using PennyLane

A quantum optimization repository implementing Variational Quantum Algorithms (VQA) / Quantum Approximate Optimization Algorithm (QAOA) to solve the Travelling Salesperson Problem using PennyLane.

---

## 📌 Overview

The Travelling Salesperson Problem (TSP) is an NP-hard combinatorial optimization problem. This project models the TSP graph as a quadratic unconstrained binary optimization (QUBO) problem and maps its cost Hamiltonian onto quantum circuits using **PennyLane**.

### Key Features
* **Graph Formulation:** Encodes distance matrices and visit-order constraints into a Ising / QUBO cost Hamiltonian.
* **Variational Circuits:** Implements parameterized quantum circuits (QAOA / VQE ansatzes) using PennyLane state preparation and gate operations.
* **Classical-Quantum Optimization:** Employs gradient-based or derivative-free classical optimizers (e.g., Adam, COBYLA) to train variational parameters.
* **Cross-Platform Compatibility:** Fully configured for isolated Python execution on macOS and Windows environments.

---

## 📁 Repository Structure

```text
quantum-TSP-PennyLane/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── graph_utils.py       # Distance matrix and graph generation helpers
│   ├── hamiltonian.py         # Construction of cost and mixer Hamiltonians
│   └── circuits.py            # PennyLane quantum nodes and ansatz definitions
├── notebooks/
│   └── tsp_exploration.ipynb  # Interactive experiments and parameter sweeps
└── main.py                    # Optimization loop and convergence plotting

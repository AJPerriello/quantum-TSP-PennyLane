# Quantum TSP: Theoretical Foundations & Concepts

This document provides a detailed theoretical overview of how the Travelling Salesperson Problem (TSP) is mapped to quantum hardware using PennyLane, Quadratic Unconstrained Binary Optimization (QUBO), and Variational Quantum Algorithms (VQE & QAOA).

---

## 1. Graph Representation & Distance Matrix

The Travelling Salesperson Problem (TSP) considers $N$ cities modeled as nodes in a complete graph. The spatial locations are defined in 2D Euclidean space $(x, y)$, and the pairwise distances between city $i$ and city $j$ form an $N \times N$ symmetric distance matrix $D$:

$$D_{i, j} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$$

* **Symmetry:** $D_{i, j} = D_{j, i}$
* **Zero Diagonal:** $D_{i, i} = 0$ (a city has zero distance to itself)

---

## 2. QUBO Formulation

To solve combinatorial optimization problems on quantum computers, we frame the classical cost and constraints into a **Quadratic Unconstrained Binary Optimization (QUBO)** model.

### 2.1 Binary Decision Encoding
We use an $N^2$ binary encoding $x_{i, t} \in \{0, 1\}$ where:

$$x_{i, t} = \begin{cases} 1 & \text{if city } i \text{ is visited at step } t \\ 0 & \text{otherwise} \end{cases}$$

For an $N$-city graph, the state vector is represented by $N^2$ binary decision variables (or $N^2$ qubits).

### 2.2 Objective Function (Route Length)
The total tour distance is calculated by summing distances between sequential time steps, wrapping back from time step $N-1$ to time step $0$:

$$H_{\text{cost}} = \sum_{i=0}^{N-1} \sum_{j=0}^{N-1} \sum_{t=0}^{N-1} D_{i, j} \cdot x_{i, t} \cdot x_{j, (t+1) \pmod N}$$

### 2.3 Constraint Penalties
To guarantee a valid physical TSP tour, two hard constraints are added as quadratic penalties scaled by a penalty weight $A$ (where $A > \max(D_{i, j})$):

1. **City Constraint:** Every city $i$ must be visited exactly once across all time steps:
   $$P_{\text{city}} = A \sum_{i=0}^{N-1} \left(1 - \sum_{t=0}^{N-1} x_{i, t}\right)^2$$

2. **Time Constraint:** Every time step $t$ must contain exactly one visited city:
   $$P_{\text{time}} = A \sum_{t=0}^{N-1} \left(1 - \sum_{i=0}^{N-1} x_{i, t}\right)^2$$

### 2.4 Complete QUBO Matrix
Combining the objective function and penalty constraints yields the full QUBO matrix $Q$:

$$H_{\text{QUBO}} = x^T Q x = H_{\text{cost}} + P_{\text{city}} + P_{\text{time}}$$

---

## 3. Mapping to Quantum Operators (Ising Spin Glasses)

Quantum computers evaluate quantum states using Pauli spin operators rather than classical binary values. We translate classical binary variables $x_{i, t} \in \{0, 1\}$ into quantum spin operators $Z_{i, t} \in \{+1, -1\}$ using the substitution:

$$x_{i, t} = \frac{I - Z_{i, t}}{2}$$

where $I$ is the $2 \times 2$ Identity matrix and $Z_{i, t}$ is the Pauli-$Z$ operator acting on qubit $k = i \cdot N + t$.

### Operator Expansions:
* **Linear Terms:** $x_i \to \frac{1}{2}(I - Z_i)$
* **Quadratic Cross Terms:** $x_i x_j \to \frac{1}{4}(I - Z_i - Z_j + Z_i \otimes Z_j)$

After expanding $x^T Q x$ and collecting like terms, the resulting cost operator is expressed in PennyLane as a sum of Pauli tensor products:

$$H_C = \sum_{k} c_k \hat{O}_k \quad \text{where } \hat{O}_k \in \{I, Z_i, Z_i Z_j\}$$

---

## 4. Variational Algorithms: VQE vs. QAOA

Both algorithms use a hybrid quantum-classical feedback loop: the quantum processor evaluates the expectation value of $H_C$, while a classical optimizer updates circuit parameters to minimize energy.

   ┌────────────────────────────────────────┐
   │     Quantum Hardware / Simulator       │
   │  Prepare State |ψ(θ)⟩ ──> Measure ⟨H_C⟩│
   └───────────────────┬────────────────────┘
                       │ Expectation Value
                       ▼
   ┌────────────────────────────────────────┐
   │           Classical Optimizer          │
   │   Compute Gradient ──> Update Params   │
   └───────────────────┬────────────────────┘
                       │ Parameter Angles (θ)
                       ▼
                  (Loop Back)

### 4.1 Variational Quantum Eigensolver (VQE)
* **Goal:** Find the lowest eigenvalue (ground state) of a target Hamiltonian $H_C$.
* **Circuit Design:** Employs parameterized rotation gates (e.g., $RY(\theta)$, $RZ(\theta)$) and entangling gates (CNOT) in heuristic layers.
* **Variational Principle:** $\langle \psi(\vec{\theta}) | H_C | \psi(\vec{\theta}) \rangle \ge E_0$. Minimizing the expectation value brings the state closer to the optimal tour solution.

### 4.2 Quantum Approximate Optimization Algorithm (QAOA)
* **Goal:** Solve combinatorial problems using time evolution derived directly from the problem structure.
* **Ansatz Structure:** For $p$ layers, QAOA alternates time evolution under the Cost Hamiltonian ($H_C$) and a Mixer Hamiltonian ($H_B = \sum_k X_k$):

$$|\psi(\vec{\gamma}, \vec{\beta})\rangle = \prod_{l=1}^{p} e^{-i \beta_l H_B} e^{-i \gamma_l H_C} |+\rangle^{\otimes N^2}$$

* **Cost Layer ($e^{-i \gamma H_C}$):** Applies phase shifts proportional to the TSP tour cost and penalties.
* **Mixer Layer ($e^{-i \beta H_B}$):** Rotates qubits around the X-axis to enable quantum tunneling between state configurations.
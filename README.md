# Quantum Options Pricer: Iterative Amplitude Estimation (IAE)

A professional-grade implementation of **Quantum Amplitude Estimation** for pricing European Call options. This project replaces traditional, computationally expensive Monte Carlo simulations with a quantum algorithm providing a **quadratic speedup** in convergence.

## 📌 Project Overview
Traditional derivatives pricing (like Black-Scholes) often struggles with complex path-dependency or non-standard distributions. This engine utilizes **Qiskit 1.x** to:
1.  **Model Uncertainty:** Map a Log-Normal distribution of asset prices into quantum superposition.
2.  **Quantum Logic:** Execute a piecewise linear payoff function using ancilla-assisted quantum arithmetic.
3.  **Algorithmic Estimation:** Apply **Iterative Amplitude Estimation (IAE)** to find the expected value (option price) without the need for high-depth Grover Operators, making it more suitable for Near-term Intermediate-Scale Quantum (NISQ) devices.

## 🛠 Tech Stack
* **Language:** Python 3.12+
* **Quantum SDK:** Qiskit 1.0+ (Latest 2026 Standards)
* **Algorithms:** `qiskit-algorithms` (IAE), `qiskit-finance`
* **Simulation:** `qiskit-aer` (Statevector Simulation)

## 🏗 Architecture
The repository is organized following clean-code principles for modular quantitative software:

* `src/qae_pricer.py`: **The Core Engine.** Encapsulates the `QuantumEuropeanCall` class, handling circuit construction, `EstimationProblem` mapping, and IAE execution.
* `main.py`: **The Entry Point.** Defines market parameters (Spot, Strike, Volatility, T) and triggers the quantum simulation.
* `.venv/`: **Isolated Environment.** Optimized for the Qiskit 1.x ecosystem.

## 🚀 Getting Started

### 1. Environment Setup
Clone the repository and initialize the virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
```

### Install Dependencies
```bash
pip install qiskit qiskit-finance qiskit-aer qiskit-algorithms numpy
```

### Usage
Configure your market parameters in main.py and run:
```bash
python main.py
```

## ⚖️ Key Technical Features
* **Dynamic Domain Mapping:** Automatically scales the quantum "sandbox" to ensure strike prices remain within the circuit's field of view, even at low time-to-maturity.
* **Ancilla Management:** Dynamically allocates "scratchpad" qubits to handle the linear rotations required for the option's hockey-stick payoff.
* **Post-Processing:** Implements automated rescaling and inverse-probability mapping to convert quantum amplitudes back into USD values.

## 📈 Financial Analysis (Case Study: RGTI)
In the included demo, the engine is tuned to model a high-volatility tech equity (**Rigetti Computing**).
* **Scenario:** Pricing an $18.00 Strike Call with high IV (85%).
* **Quantum Resolution:** Demonstrates high-fidelity pricing (up to 7-qubit discretization) to accurately capture Theta decay as the contract approaches expiration.

---
### Future Roadmap
- [ ] **Greeks Calculation:** Implementing Delta and Gamma via quantum finite difference methods.
- [ ] **Asian Options:** Expanding to path-dependent pricing using Quantum Random Walks.
- [ ] **Hardware Deployment:** Transitioning from `Aer` simulators to IBM Quantum hardware primitives.

---
*Developed as a demonstration of Quantum Computational Finance.*
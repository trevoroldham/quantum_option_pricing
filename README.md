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
* `app.py`: **User Interface** Streamlit web application for simplified user experience
## 🚀 Getting Started

### 1. Environment Setup
Clone the repository and initialize the virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🛠 CLI Arguments & Usage

The pricing engine can be configured via the terminal using the following flags:

### Required Arguments
* **`--spot`**: The current market price of the underlying asset (e.g., `13.50`).
* **`--strike`**: The strike price specified in the option contract (e.g., `18.00`).

### Market Parameters
* **`--type`**: The type of option contract. Choices are `call` or `put`. (Default: `call`).
* **`--days`**: The number of days remaining until the option's expiration. (Default: `1.0`).
* **`--vol`**: The annualized implied volatility of the underlying asset, expressed as a decimal (e.g., `0.85` for 85%). (Default: `0.85`).
* **`--rate`**: The annualized risk-free interest rate (e.g., `0.045` for 4.5%). (Default: `0.045`).

### Quantum Algorithmic Settings
* **`--qubits`**: The number of qubits used to represent the price distribution. Increasing this increases the discretization resolution ($2^n$ bins). (Default: `5`).
* **`--error`**: The target error tolerance ($\epsilon$) for the Iterative Amplitude Estimation (IAE) algorithm. (Default: `0.01`).
* **`--alpha`**: The significance level ($\alpha$) for the confidence interval (e.g., `0.05` for a 95% confidence level). (Default: `0.05`).

### Example Usage
```bash
python3 main.py --spot 13.50 --strike 18.00 --days 30 --vol 0.85 --qubits 8 --error 0.001
```

## ⚖️ Key Technical Features
* **Dynamic Domain Mapping:** Automatically scales the quantum "sandbox" to ensure strike prices remain within the circuit's field of view, even at low time-to-maturity.
* **Ancilla Management:** Dynamically allocates "scratchpad" qubits to handle the linear rotations required for the option's hockey-stick payoff.
* **Post-Processing:** Implements automated rescaling and inverse-probability mapping to convert quantum amplitudes back into USD values.

---
### Future Roadmap
- [ ] **Greeks Calculation:** Implementing Delta and Gamma via quantum finite difference methods.
- [ ] **Asian Options:** Expanding to path-dependent pricing using Quantum Random Walks.
- [ ] **Hardware Deployment:** Transitioning from `Aer` simulators to IBM Quantum hardware primitives.

---
*Developed as a demonstration of Quantum Computational Finance.*
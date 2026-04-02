### The Assignment: Discrete Portfolio Optimization via VQE

A boutique quantitative hedge fund wants to rebalance a high-yield tech portfolio containing four assets (e.g., AAPL, MSFT, GOOGL, TSLA). Standard classical solvers are failing because the fund requires the assets to be bought in strictly discrete, integer-based "lots" (e.g., 0%, 25%, 50%, or 75% of total capital), and there are harsh penalty fees if the portfolio exceeds a specific risk threshold.

Your objective is to build a Variational Quantum Eigensolver (VQE) that calculates the absolute optimal capital allocation for these four assets.

The Technical Clues (Architecture Constraints)
To build this successfully, you will need to piece together specific quantum and classical components:

The Encoding: You cannot use a 1-to-1 qubit mapping. Because we need four possible allocation weights (0, 25, 50, 75) for each asset, you must use 2 qubits per asset. Four assets means you will need an 8-qubit circuit.

The Cost Function: You will need to construct a QUBO (Quadratic Unconstrained Binary Optimization) matrix using historical stock data (expected returns and the covariance matrix).

The Ansatz (Quantum Circuit): Because the assets are highly correlated (e.g., if AAPL drops, MSFT probably drops), your quantum circuit needs strong entanglement. A heuristic hardware-efficient ansatz like RealAmplitudes or EfficientSU2 is the standard play here.

The Classical Optimizer: Since quantum simulators (and real quantum hardware) introduce noise, you need a classical optimizer that doesn't rely on perfect gradients. COBYLA (Constrained Optimization BY Linear Approximations) or SPSA (Simultaneous Perturbation Stochastic Approximation) are your best targets.

The Deliverables (Desired Output)
When a recruiter or senior engineer runs your Python script, the terminal should output three distinct things:

The Classical Baseline: The script should first run a brute-force classical algorithm (like NumPy's MinimumEigensolver) to calculate the mathematically perfect answer. This establishes the ground truth.

The VQE Convergence: A printed log (or a matplotlib graph) showing the VQE algorithm's cost function decreasing over 100-200 iterations as the classical optimizer tweaks the quantum circuit parameters.

The Translated Bitstring: The final raw output from the VQE will be an 8-bit string (e.g., 01_11_00_10). Your code must automatically translate that abstract math into a human-readable financial directive:

AAPL: 25%

MSFT: 75%

GOOGL: 0%

TSLA: 50%

To kick this off, we need to choose our tech stack. Do you want to write this assignment using IBM's Qiskit, or would you prefer Xanadu's PennyLane?
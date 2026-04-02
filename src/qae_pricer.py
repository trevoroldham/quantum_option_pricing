import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit_finance.circuit.library import LogNormalDistribution
from qiskit_algorithms import IterativeAmplitudeEstimation, EstimationProblem
from qiskit.primitives import StatevectorSampler as Sampler

class QuantumEuropeanCall:
    def __init__(self, spot_price, strike_price, volatility, risk_free_rate, maturity_years, num_qubits=3):
        self.S0 = spot_price
        self.K = strike_price
        self.vol = volatility
        self.r = risk_free_rate
        self.T = maturity_years
        self.num_qubits = num_qubits
        
        # 1. Distribution Math
        self.mu = ((self.r - 0.5 * self.vol**2) * self.T + np.log(self.S0))
        self.sigma = self.vol * np.sqrt(self.T)
        self.mean = np.exp(self.mu + self.sigma**2 / 2)
        self.variance = (np.exp(self.sigma**2) - 1) * np.exp(2 * self.mu + self.sigma**2)
        self.stddev = np.sqrt(self.variance)
        
        # 2. Dynamic Bounds
        self.low = np.min([self.S0 * 0.5, self.K * 0.8])
        self.high = np.max([self.S0 * 1.5, self.K * 1.2])

    def calculate_price(self, target_error=0.01, confidence=0.05):
        # Build components
        uncertainty_model = LogNormalDistribution(
            self.num_qubits, mu=self.mu, sigma=self.sigma**2, bounds=(self.low, self.high)
        )

        # We set rescaling to 0.1 to be safe; we must undo this later
        c_rescale = 0.1 
        payoff_function = LinearAmplitudeFunction(
            self.num_qubits,
            slope=[0,1],
            offset=[0,0],
            domain=(self.low, self.high),
            image=(0, self.high - self.K),
            breakpoints=[self.low, self.K],
            rescaling_factor=c_rescale
        )

        # The 'objective' qubit is always the FIRST qubit after the state qubits
        # in the LinearAmplitudeFunction's internal logic.
        total_qubits = payoff_function.num_qubits
        obj_qubit_index = self.num_qubits 

        objective_circuit = QuantumCircuit(total_qubits)
        objective_circuit.append(uncertainty_model, range(self.num_qubits))
        objective_circuit.append(payoff_function, range(total_qubits))

        problem = EstimationProblem(
            state_preparation=objective_circuit,
            objective_qubits=[obj_qubit_index],
            post_processing=payoff_function.post_processing # THIS IS THE KEY
        )

        iae = IterativeAmplitudeEstimation(
            epsilon_target=target_error, 
            alpha=confidence, 
            sampler=Sampler()
        )
        
        result = iae.estimate(problem)
        
        # result.estimation_processed handles the c_rescale and domain mapping
        return result.estimation_processed
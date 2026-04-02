import numpy as np
from src.qae_pricer import QuantumEuropeanCall

def run_quantum_demo():
    # --- 1. Define Market Parameters ---
    # Based on your RGTI position: Strike $18.00, Spot ~$15.60
    market_params = {
        "spot_price": 15.60,
        "strike_price": 18.00,
        "volatility": 0.85,      # 85% Annualized IV
        "risk_free_rate": 0.045,  # 4.5% Treasury Yield
        "maturity_years": 7/365, # 11 days to April 2nd
        "num_qubits": 7         # Higher qubits = higher precision (but slower)
    }
    
    print("====================================================")
    print("   QUANTUM AMPLITUDE ESTIMATION: OPTIONS PRICER     ")
    print("====================================================")
    print(f"Target Asset: RGTI (Simulated)")
    print(f"Spot Price:   ${market_params['spot_price']:.2f}")
    print(f"Strike Price: ${market_params['strike_price']:.2f}")
    print(f"Volatility:   {market_params['volatility']*100:.1f}%")
    print("----------------------------------------------------")

    try:
        # 2. Initialize the Quantum Engine
        pricer = QuantumEuropeanCall(**market_params)
        
        # 3. Calculate the Price
        # target_error: the 'epsilon' of the QAE algorithm
        print("Running Quantum Iterative Amplitude Estimation...")
        quantum_price = pricer.calculate_price(target_error=0.005)
        
        print("----------------------------------------------------")
        print(f"QUANTUM ESTIMATED VALUE: ${quantum_price:.4f}")
        print("====================================================")
        
    except Exception as e:
        print(f"\n[ERROR] Execution failed: {e}")
        print("Ensure all qiskit packages are installed in your venv.")

if __name__ == "__main__":
    run_quantum_demo()
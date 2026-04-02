import argparse
from src.qae_pricer import QuantumEuropeanCall

def main():
    # 1. Initialize the Argument Parser
    parser = argparse.ArgumentParser(
        description="Quantum European Call Pricer via Iterative Amplitude Estimation"
    )

    # 2. Add Required Arguments (Spot and Strike)
    parser.add_argument('--spot', type=float, required=True, 
                        help='Current spot price of the underlying asset (e.g., 13.50)')
    parser.add_argument('--strike', type=float, required=True, 
                        help='Strike price of the option contract (e.g., 18.00)')
    
    # 3. Add Optional Arguments with Defaults
    parser.add_argument('--days', type=float, default=1.0, 
                        help='Days until expiration (default: 1.0)')
    parser.add_argument('--vol', type=float, default=0.85, 
                        help='Annualized implied volatility (default: 0.85)')
    parser.add_argument('--rate', type=float, default=0.045, 
                        help='Risk-free interest rate (default: 0.045)')
    parser.add_argument('--qubits', type=int, default=5, 
                        help='Number of state qubits for price resolution (default: 5)')
    parser.add_argument('--error', type=float, default=0.01, 
                        help='Target error tolerance for IAE (default: 0.01)')

    # 4. Parse the inputs from the terminal
    args = parser.parse_args()

    # Convert days to fractional years for the math engine
    maturity_years = args.days / 365.0

    print("\n" + "="*50)
    print(" ⚛️  QUANTUM OPTIONS PRICING ENGINE ⚛️ ")
    print("="*50)
    print(f"Spot Price:   ${args.spot:.2f}")
    print(f"Strike Price: ${args.strike:.2f}")
    print(f"DTE:          {args.days} days")
    print(f"Volatility:   {args.vol * 100:.1f}%")
    print(f"Resolution:   {args.qubits} Qubits ({2**args.qubits} bins)")
    print("-" * 50)
    print("Initializing quantum circuit and executing IAE...\n")

    # 5. Initialize the Pricing Class
    pricer = QuantumEuropeanCall(
        spot_price=args.spot,
        strike_price=args.strike,
        volatility=args.vol,
        risk_free_rate=args.rate,
        maturity_years=maturity_years,
        num_qubits=args.qubits
    )

    # 6. Run the calculation
    price = pricer.calculate_price(target_error=args.error)
    
    print("="*50)
    print(f"✅ ESTIMATED PREMIUM: ${price:.4f}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
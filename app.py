import streamlit as st
from src.qae_pricer import QuantumEuropeanOption
import plotly.graph_objects as go
import scipy.stats as stats
import numpy as np

# ==========================================
# PLOTLY FUNCTIONS
# ==========================================
def plot_quantum_discretization(S0, K, r, vol, T, num_qubits):
    # 1. Math Setup
    mu = (r - 0.5 * vol**2) * T + np.log(S0)
    sigma = vol * np.sqrt(T)
    
    # Dynamic bounds matching your qae_pricer.py
    low = np.maximum(1e-4, np.exp(mu - 3 * sigma))
    high = np.exp(mu + 3 * sigma)
    
    # 2. Continuous Log-Normal Curve
    x_continuous = np.linspace(low, high, 1000)
    pdf_continuous = stats.lognorm.pdf(x_continuous, s=sigma, scale=np.exp(mu))
    
    # 3. Discrete Quantum Bins
    num_bins = 2**num_qubits
    x_discrete = np.linspace(low, high, num_bins)
    pdf_discrete = stats.lognorm.pdf(x_discrete, s=sigma, scale=np.exp(mu))
    
    # 4. Build the Plotly Figure
    fig = go.Figure()
    
    # Add Discrete Bins (Bar Chart)
    fig.add_trace(go.Bar(
        x=x_discrete, 
        y=pdf_discrete, 
        name=f'Quantum States ({num_bins} bins)',
        opacity=0.6,
        marker_color='#1f77b4'
    ))
    
    # Add Continuous Curve (Line Chart)
    fig.add_trace(go.Scatter(
        x=x_continuous, 
        y=pdf_continuous, 
        mode='lines', 
        name='Continuous Black-Scholes PDF',
        line=dict(color='#ff7f0e', width=3)
    ))
    
    # Add Strike Price Line
    fig.add_vline(
        x=K, 
        line_dash="dash", 
        line_color="red", 
        annotation_text=f"Strike Price (${K})", 
        annotation_position="top right"
    )
    
    # 5. Format Layout for Dark Theme
    fig.update_layout(
        title='Log-Normal Distribution vs. Quantum Discretization',
        xaxis_title='Underlying Asset Price ($)',
        yaxis_title='Probability Density',
        template='plotly_dark',
        hovermode='x unified',
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    
    return fig
# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Quantum Options Pricer",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SIDEBAR: PARAMETER INPUTS
# ==========================================
st.sidebar.header("⚙️ Market Parameters")

# Contract Specifications
option_type = st.sidebar.selectbox("Option Type", options=["Call", "Put"]).lower()
spot_price = st.sidebar.number_input("Spot Price ($)", min_value=0.01, value=13.50, step=0.50)
strike_price = st.sidebar.number_input("Strike Price ($)", min_value=0.01, value=18.00, step=0.50)
days_to_expiration = st.sidebar.number_input("Days to Expiration", min_value=1.0, value=30.0, step=1.0)

st.sidebar.divider()

# Market Dynamics
volatility = st.sidebar.slider("Implied Volatility (IV)", min_value=0.01, max_value=3.00, value=0.85, step=0.01)
risk_free_rate = st.sidebar.number_input("Risk-Free Rate", min_value=0.00, value=0.045, step=0.005, format="%.3f")

st.sidebar.divider()

# Quantum Hardware/Algorithm Settings
st.sidebar.header("⚛️ Quantum Settings")
num_qubits = st.sidebar.slider("Qubit Resolution", min_value=3, max_value=10, value=5, help="Higher qubits = exponentially higher circuit depth but better precision.")
target_error = st.sidebar.number_input("Target Error (ε)", min_value=0.0001, max_value=0.1, value=0.01, step=0.001, format="%.4f")
confidence = st.sidebar.number_input("Significance Level (α)", min_value=0.01, max_value=0.1, value=0.05, step=0.01)

# ==========================================
# MAIN DASHBOARD AREA
# ==========================================
st.title("⚛️ Quantum Options Pricing Engine")
st.markdown("""
This engine utilizes **Iterative Amplitude Estimation (IAE)** to calculate European option premiums. 
Adjust the parameters in the sidebar to simulate pricing under different market regimes and quantum resolutions.
""")

# Display current configuration summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("Spot", f"${spot_price:.2f}")
col2.metric("Strike", f"${strike_price:.2f}")
col3.metric("DTE", f"{days_to_expiration}")
col4.metric("IV", f"{volatility*100:.1f}%")

st.divider()

# Execution Trigger
if st.button("Calculate Quantum Price", type="primary", use_container_width=True):
    # Convert days to years for the math engine
    maturity_years = days_to_expiration / 365.0
    
    with st.spinner(f"Transpiling circuit for {num_qubits} qubits and executing IAE..."):
        try:
            # Initialize your existing core engine
            pricer = QuantumEuropeanOption(
                spot_price=spot_price,
                strike_price=strike_price,
                volatility=volatility,
                risk_free_rate=risk_free_rate,
                maturity_years=maturity_years,
                num_qubits=num_qubits,
                option_type=option_type
            )
            
            # Execute the algorithm
            price = pricer.calculate_price(target_error=target_error, confidence=confidence)
            
            # Display Results
            st.success("Quantum Estimation Complete!")
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-top: 20px;">
                <h2 style="color: #31333F; margin: 0;">Estimated Premium</h2>
                <h1 style="color: #1f77b4; margin: 10px 0; font-size: 48px;">${price:.4f}</h1>
                <p style="color: #7f8c8d; margin: 0; font-style: italic;">Calculated using {num_qubits} state qubits ({2**num_qubits} discrete bins)</p>
            </div>
            """, unsafe_allow_html=True)

            st.plotly_chart(plot_quantum_discretization(spot_price, strike_price, risk_free_rate, volatility, maturity_years, num_qubits), use_container_width=True)
            
        except Exception as e:
            st.error(f"An error occurred during quantum execution: {str(e)}")
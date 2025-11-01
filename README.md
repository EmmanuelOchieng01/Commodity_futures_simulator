#  Commodity Futures Simulator

A powerful Monte Carlo-based hedging simulator for farmers and exporters to optimize their commodity risk management strategies.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

##  Features

- **Real Historical Data**: Uses actual commodity prices (2010-2024)
- **Monte Carlo Simulation**: 10,000+ scenario simulations for risk analysis
- **Multiple Commodities**: Corn, Wheat, Soybeans, Coffee, Cotton
- **Advanced Hedging Strategies**: 
  - No Hedge (full exposure)
  - Full Hedge (100% coverage)
  - Partial Hedge (50% coverage)
  - Dynamic Hedge (adaptive strategy)
- **Interactive Visualizations**: Real-time charts and risk metrics
- **Risk Metrics**: VaR, Expected Shortfall, Sharpe Ratio, Max Drawdown

##  Quick Start
##Follow these steps to get the Commodity Futures Simulator running locally:

### Installation

```bash
# Clone the repository
git clone https://github.com/EmmanuelOchieng01/commodity-futures-simulator.git
cd commodity-futures-simulator

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000` in your browser.

##  How It Works

1. **Select Commodity**: Choose from 5 major agricultural commodities
2. **Set Parameters**: 
   - Expected production volume
   - Current spot price
   - Time horizon
   - Hedging strategy
3. **Run Simulation**: Monte Carlo engine generates 10,000 price scenarios
4. **Analyze Results**: View probability distributions, risk metrics, and optimal strategies

##  Technical Implementation

### Monte Carlo Simulation
- Geometric Brownian Motion (GBM) for price modeling
- Volatility calculated from historical data
- Correlation-aware multi-period simulation

### Hedging Strategies
- **Full Hedge**: Lock in futures price, eliminate price risk
- **Partial Hedge**: 50% coverage, balance risk/reward
- **Dynamic Hedge**: Adjusts coverage based on market conditions

### Risk Metrics
- **Value at Risk (VaR)**: 95% confidence worst-case scenario
- **Expected Shortfall**: Average loss beyond VaR
- **Sharpe Ratio**: Risk-adjusted return metric
- **Maximum Drawdown**: Largest peak-to-trough decline

##  Use Cases

### For Farmers
- Hedge against falling crop prices
- Plan production based on risk tolerance
- Compare hedging strategies before harvest

### For Exporters
- Lock in favorable exchange rates via commodity futures
- Manage supply chain price volatility
- Optimize procurement timing

### For Portfolio Managers
- Commodity portfolio diversification
- Risk assessment for agricultural investments
- Scenario analysis for market stress testing

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Simulation**: NumPy, Pandas
- **Visualization**: Plotly.js
- **Frontend**: HTML5, CSS3, JavaScript
- **Data**: Historical commodity prices (2010-2024)

##  Project Structure

```
commodity_futures_simulator/
├── app.py                 # Flask application
├── src/
│   ├── simulator.py       # Monte Carlo engine
│   ├── data_loader.py     # Historical data handler
│   └── strategies.py      # Hedging strategies
├── data/
│   └── commodity_prices.csv
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── requirements.txt
```

##  Skills Demonstrated

- Financial modeling and derivatives pricing
- Monte Carlo simulation techniques
- Risk management and portfolio optimization
- Data visualization and interactive dashboards
- Full-stack web development
- Statistical analysis and probability theory

##  License

MIT License - feel free to use for learning and portfolio purposes.

##  Contributing

Contributions welcome! Please open an issue or submit a PR.

##  Contact

For questions or opportunities: officialimanuel01@gmail.com

---

**Note**: This is a simulation tool for educational purposes. Always consult with financial professionals for actual hedging decisions.

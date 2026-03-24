# Commodity Futures Simulator

A Monte Carlo simulation tool that helps farmers and exporters understand and compare hedging strategies for commodity price risk. Built with Flask, NumPy, and Plotly.

---

## What it does

You select a commodity, enter your volume and time horizon, choose a hedging strategy, and the simulator runs 10,000 price scenarios using Geometric Brownian Motion. It returns a full risk report showing expected revenue, worst-case outcomes, and how each strategy performs across all simulated scenarios.

---

## Hedging strategies explained

**No Hedge** — Your revenue moves entirely with the market. If prices rise you gain, if they fall you lose. Highest risk, highest potential reward.

**Full Hedge** — You lock in the current futures price for 100% of your volume before the harvest. Revenue is fixed regardless of what the market does. Eliminates price uncertainty.

**Partial Hedge** — You hedge 50% of your volume at the futures price and leave the other 50% exposed to the market. A middle ground between protection and upside opportunity.

**Dynamic Hedge** — The hedge ratio adjusts based on price movements. When prices fall the system increases coverage to protect revenue. When prices rise it reduces coverage to capture the upside.

---

## Risk metrics explained

**Value at Risk (VaR 95%)** — The minimum revenue you can expect in the worst 5% of scenarios. If VaR is $40,000 it means there is a 5% chance your revenue falls below $40,000.

**Expected Shortfall** — The average revenue across all scenarios that fall below the VaR threshold. A more conservative measure of tail risk.

**Sharpe Ratio** — Risk-adjusted return. Higher is better. Compares expected return against volatility.

**Max Drawdown** — The largest peak-to-trough decline across simulated scenarios.

---

## Commodities available

Corn, Wheat, Soybeans, Coffee, Cotton — with realistic historical volatility calibrated from 2010–2024 price data.

---
## System screenshots 
# Home screen 

<img width="715" height="835" alt="Screenshot From 2026-03-24 12-49-49" src="https://github.com/user-attachments/assets/d2accf86-3752-4501-89b4-b8ead5776eaf" />
# Full Hedge 
<img width="1300" height="763" alt="Screenshot From 2026-03-24 12-50-33" src="https://github.com/user-attachments/assets/c5dba650-aad9-4b46-aad5-5d9939b8d6c8" />
# Hedges Comparison Full Hedge , Partial , Dynamic and No Hedge 
<img width="1330" height="595" alt="Screenshot From 2026-03-24 12-50-58" src="https://github.com/user-attachments/assets/71020d81-53c0-4047-8184-be0c13405345" />


## Launch Procedure

Requirements: Python 3.8+

```bash
git clone https://github.com/EmmanuelOchieng01/Commodity_futures_simulator
cd Commodity_futures_simulator
pip install -r requirements.txt
python app.py
```

Open your browser at **http://localhost:5000**

---

## How to use it

1. Select a commodity from the dropdown — current price and volatility are shown automatically
2. Enter the volume you want to hedge and your time horizon in months
3. Choose a hedging strategy
4. Set the number of simulations (10,000 is the default, higher is more accurate but slower)
5. Click **Run Simulation**
6. Review the revenue distribution chart, key metrics, and full risk report

---

## Project structure

```
├── app.py                      # Flask server and API endpoints
├── requirements.txt
├── src/
│   ├── simulator.py            # Monte Carlo engine (GBM price simulation)
│   ├── data_loader.py          # Commodity data and historical prices
│   └── strategies.py           # Hedging strategy definitions
├── templates/
│   └── index.html              # Main dashboard
└── static/
    └── style.css               # UI styling
```

---

## Tech stack

**Backend** — Python, Flask, NumPy, SciPy

**Frontend** — HTML, CSS, JavaScript, Plotly.js

**Simulation** — Geometric Brownian Motion, Monte Carlo methods

---

## Author

**Emmanuel Ochieng**
GitHub: https://github.com/EmmanuelOchieng01

---

*For educational and portfolio purposes. Not financial advice. Always consult a professional before making hedging decisions.*

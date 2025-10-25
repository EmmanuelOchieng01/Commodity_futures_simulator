"""
Flask application for Commodity Futures Simulator
Provides REST API and web interface for hedging simulations
"""

from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from simulator import CommoditySimulator
from data_loader import DataLoader
import json

app = Flask(__name__)

# Initialize data loader
data_loader = DataLoader()

@app.route('/')
def index():
    """Render main application page"""
    return render_template('index.html')

@app.route('/api/commodities')
def get_commodities():
    """Get list of available commodities with current prices"""
    commodities = data_loader.get_commodities_info()
    return jsonify(commodities)

@app.route('/api/simulate', methods=['POST'])
def simulate():
    """
    Run Monte Carlo simulation for hedging strategy

    Expected JSON payload:
    {
        "commodity": "CORN",
        "volume": 10000,
        "spot_price": 4.50,
        "time_horizon": 6,
        "strategy": "full_hedge",
        "simulations": 10000
    }
    """
    try:
        data = request.json

        # Validate inputs
        commodity = data.get('commodity', 'CORN')
        volume = float(data.get('volume', 10000))
        spot_price = float(data.get('spot_price', 0))
        time_horizon = int(data.get('time_horizon', 6))
        strategy = data.get('strategy', 'no_hedge')
        n_simulations = int(data.get('simulations', 10000))

        # Initialize simulator
        simulator = CommoditySimulator(
            commodity=commodity,
            data_loader=data_loader
        )

        # Run simulation
        results = simulator.run_simulation(
            volume=volume,
            spot_price=spot_price,
            time_horizon=time_horizon,
            strategy=strategy,
            n_simulations=n_simulations
        )

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/historical/<commodity>')
def get_historical(commodity):
    """Get historical prices for a commodity"""
    try:
        prices = data_loader.get_historical_prices(commodity)
        return jsonify({
            'dates': prices.index.strftime('%Y-%m-%d').tolist(),
            'prices': prices.values.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 Starting Commodity Futures Simulator...")
    print("📊 Loading historical data...")
    print("✓ Server ready at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

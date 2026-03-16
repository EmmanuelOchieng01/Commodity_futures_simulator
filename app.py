"""
Flask application for Commodity Futures Simulator
"""
from flask import Flask, render_template, request, jsonify
import sys
import json
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))
from simulator import CommoditySimulator
from data_loader import DataLoader

app = Flask(__name__)
data_loader = DataLoader()

class NumpyEncoder(json.JSONEncoder):
    """Converts numpy types to native Python types for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, np.integer):   return int(obj)
        if isinstance(obj, np.floating):  return float(obj)
        if isinstance(obj, np.ndarray):   return obj.tolist()
        if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)): return 0.0
        return super().default(obj)

def clean(obj):
    """Recursively clean all numpy types and bad floats from a dict/list."""
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean(v) for v in obj]
    if isinstance(obj, np.integer):  return int(obj)
    if isinstance(obj, np.floating): return float(obj)
    if isinstance(obj, np.ndarray):  return obj.tolist()
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)): return 0.0
    return obj

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/commodities')
def get_commodities():
    return jsonify(data_loader.get_commodities_info())

@app.route('/api/simulate', methods=['POST'])
def simulate():
    try:
        data        = request.json
        commodity   = data.get('commodity', 'CORN')
        volume      = float(data.get('volume', 10000))
        spot_price  = float(data.get('spot_price', 0))
        time_horizon= int(data.get('time_horizon', 6))
        strategy    = data.get('strategy', 'no_hedge')
        n_sims      = int(data.get('simulations', 10000))

        simulator = CommoditySimulator(commodity=commodity, data_loader=data_loader)
        results   = simulator.run_simulation(
            volume=volume, spot_price=spot_price,
            time_horizon=time_horizon, strategy=strategy,
            n_simulations=n_sims
        )
        return app.response_class(
            response=json.dumps(clean(results), cls=NumpyEncoder),
            status=200, mimetype='application/json'
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/api/historical/<commodity>')
def get_historical(commodity):
    try:
        prices = data_loader.get_historical_prices(commodity)
        return jsonify({
            'dates':  prices.index.strftime('%Y-%m-%d').tolist(),
            'prices': [float(p) for p in prices.values]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/compare', methods=['POST'])
def compare_strategies():
    """Run all 4 strategies and return side-by-side metrics for comparison."""
    try:
        data         = request.json
        commodity    = data.get('commodity', 'CORN')
        volume       = float(data.get('volume', 10000))
        spot_price   = float(data.get('spot_price', 0))
        time_horizon = int(data.get('time_horizon', 6))
        n_sims       = int(data.get('simulations', 5000))

        strategies = ['no_hedge', 'full_hedge', 'partial_hedge', 'dynamic_hedge']
        comparison = {}
        for s in strategies:
            simulator = CommoditySimulator(commodity=commodity, data_loader=data_loader)
            r = simulator.run_simulation(
                volume=volume, spot_price=spot_price,
                time_horizon=time_horizon, strategy=s,
                n_simulations=n_sims
            )
            comparison[s] = clean(r['metrics'])
        return app.response_class(
            response=json.dumps(comparison, cls=NumpyEncoder),
            status=200, mimetype='application/json'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("Starting Commodity Futures Simulator...")
    print("Server ready at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

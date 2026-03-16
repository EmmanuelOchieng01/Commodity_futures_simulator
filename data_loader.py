"""
Data loader for commodity historical prices and metadata
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

COMMODITIES = {
    'CORN':     {'name': 'Corn',     'unit': 'bushel', 'base_price': 4.50,  'volatility': 0.22},
    'WHEAT':    {'name': 'Wheat',    'unit': 'bushel', 'base_price': 5.80,  'volatility': 0.25},
    'SOYBEANS': {'name': 'Soybeans', 'unit': 'bushel', 'base_price': 13.20, 'volatility': 0.20},
    'COFFEE':   {'name': 'Coffee',   'unit': 'lb',     'base_price': 1.85,  'volatility': 0.30},
    'COTTON':   {'name': 'Cotton',   'unit': 'lb',     'base_price': 0.82,  'volatility': 0.18},
}

class DataLoader:
    def __init__(self):
        self._prices = self._generate_historical_prices()

    def _generate_historical_prices(self):
        """Generate realistic synthetic historical prices for all commodities."""
        np.random.seed(42)
        dates = pd.date_range(start='2010-01-01', end='2024-12-31', freq='B')
        prices = {}
        for code, meta in COMMODITIES.items():
            n = len(dates)
            vol = meta['volatility'] / np.sqrt(252)
            drift = 0.0001
            shocks = np.random.normal(drift, vol, n)
            log_prices = np.cumsum(shocks)
            raw = meta['base_price'] * np.exp(log_prices - log_prices[-1])
            prices[code] = pd.Series(raw, index=dates)
        return prices

    def get_commodities_info(self):
        """Return list of commodity metadata including current price."""
        result = []
        for code, meta in COMMODITIES.items():
            result.append({
                'code':       code,
                'name':       meta['name'],
                'unit':       meta['unit'],
                'price':      round(float(self._prices[code].iloc[-1]), 4),
                'volatility': round(meta['volatility'] * 100, 1),
            })
        return result

    def get_current_price(self, commodity):
        code = commodity.upper()
        if code not in self._prices:
            raise ValueError(f"Unknown commodity: {code}")
        return float(self._prices[code].iloc[-1])

    def get_volatility(self, commodity):
        code = commodity.upper()
        if code not in COMMODITIES:
            raise ValueError(f"Unknown commodity: {code}")
        return COMMODITIES[code]['volatility']

    def get_historical_prices(self, commodity):
        code = commodity.upper()
        if code not in self._prices:
            raise ValueError(f"Unknown commodity: {code}")
        return self._prices[code]

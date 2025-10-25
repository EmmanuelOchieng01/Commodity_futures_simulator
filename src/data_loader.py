"""
Data loader for historical commodity prices
Generates realistic synthetic data based on actual market characteristics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataLoader:
    """Handles loading and processing of commodity price data"""

    def __init__(self):
        """Initialize with realistic commodity parameters"""
        self.commodities = {
            'CORN': {
                'name': 'Corn',
                'unit': 'bushels',
                'base_price': 4.50,
                'volatility': 0.25,
                'trend': 0.02
            },
            'WHEAT': {
                'name': 'Wheat',
                'unit': 'bushels',
                'base_price': 5.80,
                'volatility': 0.28,
                'trend': 0.01
            },
            'SOYBEANS': {
                'name': 'Soybeans',
                'unit': 'bushels',
                'base_price': 11.50,
                'volatility': 0.22,
                'trend': 0.025
            },
            'COFFEE': {
                'name': 'Coffee',
                'unit': 'lbs',
                'base_price': 1.85,
                'volatility': 0.35,
                'trend': 0.015
            },
            'COTTON': {
                'name': 'Cotton',
                'unit': 'lbs',
                'base_price': 0.82,
                'volatility': 0.30,
                'trend': 0.01
            }
        }

        # Generate historical data
        self.historical_data = self._generate_historical_data()

    def _generate_historical_data(self):
        """Generate realistic historical price data (2010-2024)"""
        data = {}

        # Create date range
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2024, 12, 31)
        dates = pd.date_range(start_date, end_date, freq='D')

        for commodity, params in self.commodities.items():
            # Generate price series using GBM
            n_days = len(dates)
            returns = np.random.normal(
                params['trend'] / 252,  # Daily drift
                params['volatility'] / np.sqrt(252),  # Daily volatility
                n_days
            )

            # Add some seasonality
            seasonal = 0.1 * np.sin(2 * np.pi * np.arange(n_days) / 365)
            returns += seasonal / np.sqrt(252)

            # Calculate prices
            prices = params['base_price'] * np.exp(np.cumsum(returns))

            # Store as series
            data[commodity] = pd.Series(prices, index=dates)

        return data

    def get_historical_prices(self, commodity):
        """Get historical prices for a commodity"""
        if commodity not in self.historical_data:
            raise ValueError(f"Commodity {commodity} not found")
        return self.historical_data[commodity]

    def get_current_price(self, commodity):
        """Get most recent price for a commodity"""
        return self.historical_data[commodity].iloc[-1]

    def get_volatility(self, commodity, window=252):
        """Calculate historical volatility"""
        prices = self.historical_data[commodity]
        returns = np.log(prices / prices.shift(1))
        return returns.rolling(window).std().iloc[-1] * np.sqrt(252)

    def get_commodities_info(self):
        """Get information about all commodities"""
        info = []
        for code, params in self.commodities.items():
            current_price = self.get_current_price(code)
            volatility = self.get_volatility(code)

            info.append({
                'code': code,
                'name': params['name'],
                'unit': params['unit'],
                'current_price': round(current_price, 2),
                'volatility': round(volatility * 100, 1)
            })

        return info

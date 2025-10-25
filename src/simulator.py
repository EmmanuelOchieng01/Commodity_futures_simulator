"""
Monte Carlo simulator for commodity futures hedging
Implements various hedging strategies and risk metrics
"""

import numpy as np
from scipy import stats

class CommoditySimulator:
    """Simulates commodity price movements and hedging outcomes"""

    def __init__(self, commodity, data_loader):
        """
        Initialize simulator

        Args:
            commodity: Commodity code (e.g., 'CORN')
            data_loader: DataLoader instance with historical data
        """
        self.commodity = commodity
        self.data_loader = data_loader
        self.current_price = data_loader.get_current_price(commodity)
        self.volatility = data_loader.get_volatility(commodity)

    def simulate_prices(self, spot_price, time_horizon, n_simulations):
        """
        Simulate future commodity prices using Geometric Brownian Motion

        Args:
            spot_price: Current spot price
            time_horizon: Months into the future
            n_simulations: Number of Monte Carlo simulations

        Returns:
            Array of simulated final prices (n_simulations,)
        """
        dt = time_horizon / 12  # Convert months to years
        drift = 0.02  # Assumed expected return

        # Generate random shocks
        z = np.random.standard_normal(n_simulations)

        # GBM formula
        final_prices = spot_price * np.exp(
            (drift - 0.5 * self.volatility**2) * dt + 
            self.volatility * np.sqrt(dt) * z
        )

        return final_prices

    def calculate_pnl(self, volume, spot_price, futures_price, final_prices, strategy):
        """
        Calculate P&L for each simulation under given strategy

        Args:
            volume: Quantity to hedge
            spot_price: Initial spot price
            futures_price: Futures contract price (equals spot_price)
            final_prices: Simulated final prices
            strategy: Hedging strategy name

        Returns:
            Array of P&L values
        """
        # Unhedged revenue
        unhedged_revenue = volume * final_prices

        if strategy == 'no_hedge':
            return unhedged_revenue

        elif strategy == 'full_hedge':
            # Lock in futures price for entire volume
            hedged_revenue = volume * futures_price
            return np.full_like(final_prices, hedged_revenue)

        elif strategy == 'partial_hedge':
            # Hedge 50% of volume
            hedge_ratio = 0.5
            hedged_volume = volume * hedge_ratio
            unhedged_volume = volume * (1 - hedge_ratio)

            hedged_revenue = hedged_volume * futures_price
            unhedged_revenue = unhedged_volume * final_prices

            return hedged_revenue + unhedged_revenue

        elif strategy == 'dynamic_hedge':
            # Adjust hedge ratio based on price movement
            # More hedging if prices fall, less if they rise
            hedge_ratios = np.clip(
                0.5 + 0.5 * (futures_price - final_prices) / futures_price,
                0, 1
            )

            hedged_revenue = volume * hedge_ratios * futures_price
            unhedged_revenue = volume * (1 - hedge_ratios) * final_prices

            return hedged_revenue + unhedged_revenue

        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def calculate_risk_metrics(self, pnl):
        """
        Calculate comprehensive risk metrics

        Args:
            pnl: Array of P&L values

        Returns:
            Dictionary of risk metrics
        """
        mean_pnl = np.mean(pnl)
        std_pnl = np.std(pnl)

        # Value at Risk (95% confidence)
        var_95 = np.percentile(pnl, 5)

        # Expected Shortfall (average of worst 5%)
        es_95 = np.mean(pnl[pnl <= var_95])

        # Sharpe Ratio (assuming risk-free rate of 3%)
        risk_free_rate = 0.03
        sharpe_ratio = (mean_pnl / mean_pnl - risk_free_rate) / (std_pnl / mean_pnl) if std_pnl > 0 else 0

        # Max drawdown
        cummax = np.maximum.accumulate(np.sort(pnl)[::-1])
        drawdown = (cummax - np.sort(pnl)[::-1]) / cummax
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0

        return {
            'mean': float(mean_pnl),
            'std': float(std_pnl),
            'min': float(np.min(pnl)),
            'max': float(np.max(pnl)),
            'var_95': float(var_95),
            'es_95': float(es_95),
            'sharpe_ratio': float(sharpe_ratio),
            'max_drawdown': float(max_drawdown * 100),
            'percentile_5': float(np.percentile(pnl, 5)),
            'percentile_25': float(np.percentile(pnl, 25)),
            'percentile_50': float(np.percentile(pnl, 50)),
            'percentile_75': float(np.percentile(pnl, 75)),
            'percentile_95': float(np.percentile(pnl, 95))
        }

    def run_simulation(self, volume, spot_price, time_horizon, strategy, n_simulations=10000):
        """
        Run complete Monte Carlo simulation

        Args:
            volume: Quantity to hedge
            spot_price: Current spot price (0 means use current market price)
            time_horizon: Months into the future
            strategy: Hedging strategy
            n_simulations: Number of simulations

        Returns:
            Dictionary with simulation results
        """
        # Use current market price if spot_price is 0
        if spot_price == 0:
            spot_price = self.current_price

        # Simulate future prices
        final_prices = self.simulate_prices(spot_price, time_horizon, n_simulations)

        # Calculate P&L for strategy
        futures_price = spot_price  # Simplified: futures = spot
        pnl = self.calculate_pnl(volume, spot_price, futures_price, final_prices, strategy)

        # Calculate risk metrics
        metrics = self.calculate_risk_metrics(pnl)

        # Create histogram data
        hist, bin_edges = np.histogram(pnl, bins=50)
        histogram = {
            'counts': hist.tolist(),
            'bins': bin_edges.tolist()
        }

        # Price distribution
        price_hist, price_bins = np.histogram(final_prices, bins=50)
        price_distribution = {
            'counts': price_hist.tolist(),
            'bins': price_bins.tolist()
        }

        return {
            'strategy': strategy,
            'commodity': self.commodity,
            'spot_price': float(spot_price),
            'volume': float(volume),
            'time_horizon': time_horizon,
            'n_simulations': n_simulations,
            'metrics': metrics,
            'histogram': histogram,
            'price_distribution': price_distribution,
            'sample_scenarios': {
                'best_case': float(np.max(pnl)),
                'worst_case': float(np.min(pnl)),
                'median': float(np.median(pnl))
            }
        }

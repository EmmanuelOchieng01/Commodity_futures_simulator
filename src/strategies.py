"""
Hedging strategy implementations
Defines different approaches to commodity risk management
"""

class HedgingStrategy:
    """Base class for hedging strategies"""

    @staticmethod
    def get_strategy_info():
        """Return information about all available strategies"""
        return {
            'no_hedge': {
                'name': 'No Hedge',
                'description': 'Full exposure to price movements. Maximum risk and reward.',
                'risk_level': 'High',
                'complexity': 'Simple'
            },
            'full_hedge': {
                'name': 'Full Hedge',
                'description': 'Lock in futures price for entire volume. Eliminates price risk.',
                'risk_level': 'Low',
                'complexity': 'Simple'
            },
            'partial_hedge': {
                'name': 'Partial Hedge (50%)',
                'description': 'Hedge half the volume. Balance between risk and opportunity.',
                'risk_level': 'Medium',
                'complexity': 'Simple'
            },
            'dynamic_hedge': {
                'name': 'Dynamic Hedge',
                'description': 'Adjust hedge ratio based on price movements. Adaptive strategy.',
                'risk_level': 'Medium',
                'complexity': 'Advanced'
            }
        }

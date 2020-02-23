class Option:
    def __init__(self, typ: str, strike: float, maturity: float, price: float):
        assert typ in ['C', 'P'], 'Must enter C or P.'
        self.type = typ
        self.strike = strike
        self.maturity = maturity
        self.price = price

    def get_payoff_function(self):
        if self.type == 'C':
            def func(spot):
                return max(spot - self.strike, 0)
            return func
        else:
            def func(spot):
                return max(self.strike - spot, 0)
            return func


def create_synthetic(call: Option, put: Option, long_or_short: str):
    assert call.type == 'C', 'First argument not a call.'
    assert put.type == 'P', 'Second argument not a put.'
    assert call.strike == put.strike, 'Strikes must be the same.'
    assert long_or_short in ['long', 'short'], 'Must be long or short'

    def func(x):
        if long_or_short == 'long':
            return call.get_payoff_function()(x) - put.get_payoff_function()(x)
        else:
            return -call.get_payoff_function()(x) + put.get_payoff_function()(x)

    price = call.price - put.price
    long_or_short_at = call.strike

    if long_or_short == 'long':
        return func, long_or_short_at, price
    else:
        return func, long_or_short_at, -price


def find_synthetic_arbitrage(call: Option, put: Option, spot: float):
    assert call.strike == put.strike

    synthetic_long_pnl = (spot - call.strike) - call.price + put.price
    synthetic_short_pnl = call.strike - spot - put.price + call.price

    if synthetic_long_pnl > 0:
        print(f'Buy C{call.strike} at {call.price} and sell P{put.strike} at {put.price}',
              ' for a riskless profit of {synthetic_long_pnl}.')
    elif synthetic_short_pnl > 0:
        print(f'Buy P{put.strike} at {put.price} and sell C{call.strike} at {call.price}',
              f' for a riskless profit of {synthetic_short_pnl}')

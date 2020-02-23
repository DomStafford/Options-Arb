from Option import Option


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


def check_synthetic_arbitrage(call: Option, put: Option, spot: float):
    assert call.strike == put.strike

    synthetic_long_pnl = (spot - call.strike) - call.price + put.price

    if synthetic_long_pnl > 0:
        print(f'Buy C{call.strike} at {call.price}, sell P{put.strike} at {put.price}, and sell the stock at {spot}.',
              f' Riskless profit of {synthetic_long_pnl:.3f}.')
    elif synthetic_long_pnl < 0:
        print(f'Buy P{put.strike} at {put.price}, sell C{call.strike} at {call.price}, and buy the stock at {spot}.',
              f' Riskless profit of {-synthetic_long_pnl:.3f}')


def find_synthetic_arbitrage(options_df, spot: float):
    for _, row in options_df.iterrows():
        call = Option(typ='C', strike=row['K'], price=row['C'], maturity=1)
        put = Option(typ='P', strike=row['K'], price=row['P'], maturity=1)
        check_synthetic_arbitrage(call, put, spot)

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
import ipysheet
import pandas as pd

from ArbitrageStrategies.SyntheticArbitrage import find_synthetic_arbitrage


def options_sheet_to_df(options_sheet):
    options_df = ipysheet.to_dataframe(options_sheet)
    options_df.columns = options_df.iloc[0]
    options_df = options_df[1:]
    for col in ['C', 'K', 'P']:
        options_df[col] = pd.to_numeric(options_df[col])
    options_df = options_df[options_df.K != 0]
    return options_df


def options_input():
    options_sheet = ipysheet.sheet(rows=10, columns=3, column_headers=False)
    cell1 = ipysheet.cell(0, 0, 'C')
    cell2 = ipysheet.cell(0, 1, 'K')
    cell2 = ipysheet.cell(0, 2, 'P')
    for row in range(1, options_sheet.rows):
        for col in range(0, options_sheet.columns):
            ipysheet.cell(row, col, value=0.0, numeric_format='0.00')
    return options_sheet


class Market:

    def __init__(self, options_sheet: ipysheet.Sheet, spot: float, rate: float):
        self.options = options_sheet_to_df(options_sheet)
        self.spot = spot
        self.rate = rate

    def find_arb(self):
        find_synthetic_arbitrage(self.options, self.spot)


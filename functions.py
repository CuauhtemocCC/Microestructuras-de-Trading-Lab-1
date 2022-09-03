
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import yfinance as yf
data = yf.download("AAPL", start="2020-01-01", end="2022-07-30")
precios = data["Adj Close"]
import pandas as pd
print(data)
print(precios)
# precios.loc[dates], donde dates = lista de fechas seleccionadas
# precios.loc["2020-01-31":"2021-01-31"]





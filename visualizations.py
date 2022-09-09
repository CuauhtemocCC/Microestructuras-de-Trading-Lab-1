
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Inversion de Capital por estrategia activa y pasiva                                                        -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: CuauhtemocCC                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/CuauhtemocCC/Microestructuras-de-Trading-Lab-1                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import plotly.express as px
import data as dt

def pie_chart(base_pesos,columna_ticker,columna_valores):
    chart = px.pie(base_pesos,values=columna_valores,names=base_pesos[columna_ticker],title="Portfolio Composition", 
       template="simple_white")
    return chart

def bar_chart(base_pesos,columna_ticker,columna_valores):
    chart = px.bar(base_pesos,x=base_pesos[columna_valores],y=base_pesos[columna_ticker],title="Portfolio Composition", 
       template="simple_white")
    return chart

def desempeño_lineal(base,columna):
    chart = px.line(base[columna],title="Portfolio Behavior")
    return chart

def doble_linea(base1,base2,columna):
    chart = px.line(x=base1["Timestamp"],y=[base1[columna],base2[columna]],title="Comparation")
    return chart

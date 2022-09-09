
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
import yfinance as yf
import functions as fn 
import numpy as np
#import plotly.express as px

# PARA INVERSION PASIVA

data = pd.read_csv("files/NAFTRAC_20200131.csv",skiprows=2)

dates = ["2021-01-29","2021-02-26","2021-03-31","2021-04-30","2021-05-31","2021-06-30",
        "2021-07-30","2021-08-31","2021-09-30","2021-10-26","2021-11-30","2021-12-31",
        "2022-01-26","2022-02-28","2022-03-31","2022-04-29","2022-05-31","2022-06-30",
        "2022-07-29"]

pesos = data.iloc[:-1,0:4:3]
pesos2 = data.iloc[:-1,0:4:3]

Tickers = pesos["Ticker"].map(fn.clean_tickers)
pesos["Ticker"] = pesos["Ticker"].map(fn.clean_tickers)

pesos = pesos[(pesos["Ticker"]!="KOFUBL.MX") & (pesos["Ticker"]!="BSMXB.MX") & (pesos["Ticker"]!="MXN.MX")]

pesos["Peso (%)"] = pesos["Peso (%)"]/100

pesos.sort_values(by="Ticker",inplace=True)

vector_pesos = pesos.iloc[:,1].to_numpy()
vector_tickers = pesos.iloc[:,0].to_list()

info = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start="2021-01-01", end="2022-07-30",interval="1d")

prices = info["Adj Close"]
prices2 = prices.drop(["BSMXB.MX",'KOFUBL.MX'],axis=1)

df = prices2.loc[dates]
df2 = df.T

Base = pd.DataFrame({"Symbols":vector_tickers,
                    "Pesos":vector_pesos,
                    "Precio":df2["2021-01-29"]})

Base["Postura"] = Base["Pesos"]*969000
Base["Titulos"] = round(Base["Postura"]/Base["Precio"],0)
Base["Precio"] = round(Base["Precio"],2)

inv_pas = [{"Timestamp":dates[0],"Capital":969000.0}]
for i in range(18):
    Base["Precio"] = round(df2.iloc[:,i+1],2)
    Base["Postura"] = Base["Precio"]*Base["Titulos"]
    
    inv_pas.append({"Timestamp":dates[i+1],"Capital":round(Base["Postura"].sum(),0)})

inv_pas_df = pd.DataFrame(inv_pas)

inv_pas_df["Yield"] = inv_pas_df["Capital"].pct_change().fillna(0).round(6)
inv_pas_df["Yield"] = inv_pas_df["Yield"]*100
inv_pas_df["Acum Yield"] = inv_pas_df["Yield"].cumsum()
#print(inv_pas_df)

# DATOS PARA PORTAFOLIO EFICIENTE

pesos.sort_values(by="Ticker",inplace=True)

info2 = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start="2020-01-01", end="2021-01-01",interval="1d")
prices3 = info2["Adj Close"].fillna(0)
prices3 = prices3.drop(["BSMXB.MX",'KOFUBL.MX'],axis=1)

R = np.log(prices3/prices3.shift(1))
u_R = R.mean()
s_R = R.cov()
rf = 0.0429/252

E_portfolio = fn.portfolio(u_R,rf,s_R)
e_pesos = E_portfolio.tolist()
pesos["Pesos Eficientes"] =  e_pesos
pesos["Pesos Eficientes"] = pesos["Pesos Eficientes"]*100
pesos_noceros = pesos[pesos["Pesos Eficientes"]!=0]

# DATOS PARA ACTIVA

info3 = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start="2021-01-01", end="2022-07-31",interval="1d")
prices5 = info3["Close"].fillna(0)
prices5 = prices5.drop(["BSMXB.MX",'KOFUBL.MX'],axis=1)

rend_act = prices5.pct_change().dropna()
dates_act = ["2021-01-29","2021-02-26","2021-03-31","2021-04-30","2021-05-31","2021-06-30",
        "2021-07-30","2021-08-31","2021-09-30","2021-10-26","2021-11-30","2021-12-31",
        "2022-01-26","2022-02-28","2022-03-31","2022-04-29","2022-05-31","2022-06-30",
        "2022-07-29"]

rend_matrix = rend_act.loc[dates_act]
rend_matrixT = rend_matrix.T
prices_matrix = prices5.loc[dates_act]
prices_matrixT = prices_matrix.T

vector_pesos = pesos.iloc[:,2].to_numpy()
vector_tickers = pesos.iloc[:,0].to_list()

cash = 31000
Base_a = pd.DataFrame({"Symbols":vector_tickers,
                    "Pesos":vector_pesos,
                    "Precio":prices_matrixT["2021-01-29"]})
Base_a["Pesos"] = Base_a["Pesos"]/100
Base_a["Postura"] = Base_a["Pesos"]*969000
Base_a["Titulos"] = round(Base_a["Postura"]/Base_a["Precio"],0)
Base_a["Precio"] = round(Base_a["Precio"],2)

Base_a["Precios_Nuevos"] = np.zeros(33)
Base_a["Titulos_Nuevos"] = np.zeros(33)
Base_a["Diferencial_Tit"] = np.zeros(33)
Base_a["Diferencial_Cash"] = np.zeros(33)
Base_a["Comision"] = np.zeros(33)
Base_a["Pesos_Nuevos"] = np.zeros(33)
Base_a["Titulos de Compra"] = np.zeros(33)
#print(Base_a)

operaciones = [{"Timestamp":dates_act[0],"Titulos Compra":0,"Comision":0}]
inv_act = [{"Timestamp":dates_act[0],"Capital":969000.0}]
cash = 31000
    
for j in range(18):
    if cash > 0:
        Base_a["Precios_Nuevos"] = round(prices_matrixT.iloc[:,j+1],2)
        for i in range(33):
            if (Base_a.iloc[i,5]/Base_a.iloc[i,2])-1 <= -0.05:
                Base_a.iloc[i,6] = round(Base_a.iloc[i,4]*0.975,0)
                Base_a.iloc[i,7] = round(Base_a.iloc[i,6]-Base_a.iloc[i,4],0)
                Base_a.iloc[i,8] = round(Base_a.iloc[i,7]*Base_a.iloc[i,2],0)
                Base_a.iloc[i,8] = Base_a.iloc[i,8]*-1

            elif (Base_a.iloc[i,5]/Base_a.iloc[i,2])-1 >= 0.05:
                Base_a.iloc[i,6] = round(Base_a.iloc[i,4]*1.025,0)
                Base_a.iloc[i,7] = round(Base_a.iloc[i,6]-Base_a.iloc[i,4],0)
                Base_a.iloc[i,8] = round(Base_a.iloc[i,7]*Base_a.iloc[i,2],0)
                Base_a.iloc[i,8] = Base_a.iloc[i,8]*-1

            else:
                Base_a.iloc[i,6] = round(Base_a.iloc[i,4],0)
                Base_a.iloc[i,7] = round(Base_a.iloc[i,6]-Base_a.iloc[i,4],0)
                Base_a.iloc[i,8] = round(Base_a.iloc[i,7]*Base_a.iloc[i,2],0)
                Base_a.iloc[i,8] = Base_a.iloc[i,8]*-1

            if Base_a.iloc[i,8] < 0 and Base_a.iloc[i,7] > 0:
                Base_a.iloc[i,9] = Base_a.iloc[i,8]*-0.00125

            if Base_a.iloc[i,7] > 0:
                Base_a.iloc[i,11] = Base_a.iloc[i,7]
            else:
                Base_a.iloc[i,11] = 0


        Base_a["Precio"] = round(prices_matrixT.iloc[:,j+1],2)
            #Base["Rend"] = round(rend_matrixT.iloc[:,j+1],6)
        Base_a["Titulos"] = Base_a["Titulos_Nuevos"]
        Base_a["Postura"] = Base_a["Precio"]*Base_a["Titulos"]
        Base_a["Pesos_Nuevos"] = Base_a["Postura"]/Base_a["Postura"].sum()
        Base_a["Pesos"] = Base_a["Pesos_Nuevos"]

        cash = cash - Base_a["Comision"].sum()
        cash = cash + Base_a["Diferencial_Cash"].sum()

        inv_act.append({"Timestamp":dates_act[j+1],"Capital":round(Base_a["Postura"].sum(),0)})
        operaciones.append({"Timestamp":dates_act[j+1],"Titulos Compra":Base_a["Titulos de Compra"].sum(),
                            "Comision":round(Base_a["Comision"].sum(),4)})

        Base_a["Titulos_Nuevos"] = np.zeros(33)
        Base_a["Diferencial_Tit"] = np.zeros(33)
        Base_a["Diferencial_Cash"] = np.zeros(33)
        Base_a["Comision"] = np.zeros(33)

inv_act_df = pd.DataFrame(inv_act)
inv_act_df["Yield"] = inv_act_df["Capital"].pct_change().fillna(0).round(6)
inv_act_df["Yield"] = inv_act_df["Yield"]*100
inv_act_df["Acum Yield"] = inv_act_df["Yield"].cumsum()

pesos_noceros2 = Base_a[Base_a["Pesos_Nuevos"]!=0]
#print(inv_act_df)

# TABLA DE OPERACIONES

operaciones_df = pd.DataFrame(operaciones)
operaciones_df["Titulos Totales"] = operaciones_df["Titulos Compra"].cumsum()
operaciones_df["Comision Acum"] = operaciones_df["Comision"].cumsum()
operaciones_df = operaciones_df[["Timestamp","Titulos Totales","Titulos Compra","Comision","Comision Acum"]]
#print(operaciones_df)

# MEDIDAS DE DESEMPEÑO

rfa = 4.29
sharpe_act = (inv_act_df["Yield"].mean() - rfa)/inv_act_df["Yield"].std()
sharpe_pas = (inv_pas_df["Yield"].mean() - rfa)/inv_pas_df["Yield"].std()
rend_m_a = inv_act_df["Yield"].mean()
rend_m_p = inv_pas_df["Yield"].mean()
acumrend_a = inv_act_df["Acum Yield"].iloc[-1]
acumrend_p = inv_pas_df["Acum Yield"].iloc[-1]

tabla_des = pd.DataFrame({"Medida":["rend_m","rend_c","sharpe"]})
tabla_des["Descripcion"] = ["Rend Mensual Promedio","Rend Acumulado Mensual","Indice de Sharpe"]
tabla_des["Inv Pasiva"] = [rend_m_p,acumrend_p,sharpe_pas]
tabla_des["Inv Activa"] = [rend_m_a,acumrend_a,sharpe_act]
#print(tabla_des)
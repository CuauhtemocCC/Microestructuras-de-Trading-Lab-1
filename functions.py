
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Inversion de Capital por estrategia activa y pasiva                                                        -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: CuauhtemocCC                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/CuauhtemocCC/Microestructuras-de-Trading-Lab-1                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import numpy as np
from scipy.optimize import minimize

varianza = lambda w,Sigma: w.T.dot(Sigma.dot(w))
rend = lambda w, r: w.dot(r)
rs = lambda w,Eind,rf,Sigma: -(rend(w,Eind)-rf)/ varianza(w,Sigma)**0.5

def clean_tickers(word):
    try:
        word = "".join(w for w in word if w not in "*")
    except:
        pass
    
    word = word.replace(".","-")    
    word = word+".MX"   
    return word

def portfolio(Eind,rf,Sigma):
    n=len(Eind)
    w0=np.ones(n)/n
    bnds=((0,None),)*n
    cons = {"type":"eq","fun":lambda w:w.sum()-1}
    emv = minimize(fun = rs,x0=w0,args= (Eind,rf,Sigma),bounds=bnds,
                   constraints=cons,tol=1e-10)
    
    return np.round(emv.x,4)





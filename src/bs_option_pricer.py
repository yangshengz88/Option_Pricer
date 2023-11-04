from math import log,e
from scipy import stats
from datetime import date
import numpy as np

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import yfinance as yf




def black_scholes_merton():
  
    '''
    Function that estimates the value of a call or put option using the Black Scholes Merton Model.
    
    Parameters
    ----------
    option_type: call or put
    stock_price: Spot market value of the underlying asset
    strike_price: Strike price of the options contract
    rate: Risk free rate
    time: Time to expiration for the options contract
    volatility: Volatility of the asset
    dividend: Dividend yield of the asset, with a default value set to zero

    Returns
    -------
    Returns the estimated option value of the contract
    '''
    option_type =option_type_combobox.get() 
    stock_price = yf.Ticker(e_ticker.get().upper()).history()['Close'].iloc[-1]
    strike_price= float(e_strike_price.get())
    rate= float(e_rate.get())
    time = float(e_time_to_expir.get())
    volatility = float(e_vol.get())
    dividend= float(e_div.get())

    d1 = (log(stock_price/strike_price) + (rate - dividend + volatility**2/2) * time)/(volatility * time**.5)
    d2 = d1 - volatility * time**.5
    try:
        if option_type =="CALL":
           option_price = stats.norm.cdf(d1) * stock_price*e**(-dividend*time) - stats.norm.cdf(d2)*strike_price*e**(-rate*time)
        elif option_type=="PUT":
           option_price = stats.norm.cdf(-d2)*strike_price*e**(-rate * time) - stats.norm.cdf(-d1) * stock_price*e**(-dividend*time)
        option_price = str(np.round(option_price,6))
        output_list.insert(tk.END, "Option Price:   " +option_price)
    except:
        messagebox.showinfo(title='Error', text ="Make sure all fileds are filled")


def greeks():
  
    '''
    Function that estimates the delta of a call or put option using the Black Scholes Merton Model. 
    
    '''
    option_type =option_type_combobox.get() 
    stock_price = yf.Ticker(e_ticker.get().upper()).history()['Close'].iloc[-1]
    strike_price= float(e_strike_price.get())
    rate= float(e_rate.get())
    time = float(e_time_to_expir.get())
    volatility = float(e_vol.get())
    dividend= float(e_div.get())
    d1 = (log(stock_price/strike_price) + (rate - dividend + volatility**2/2) * time)/(volatility * time**.5)
    d2 = d1 - volatility * time**.5
    try:
        if option_type =="CALL":
           option_delta = stats.norm.cdf(d1) * e**(-dividend*time)
           option_gamma= (stats.norm.pdf(d1)* e**(-dividend *time))/(stock_price* volatility*time **.5)
           option_theta= -stock_price* stats.norm.pdf(d1)*volatility*e**(-dividend * time)*0.5*time**(-0.5) + dividend * stock_price * stats.norm.cdf(d1) * e**(-dividend*time) - rate * strike_price * e**(-rate*time) * stats.norm.cdf(d2)
           option_vega = stock_price*time**0.5 * stats.norm.pdf(d1)*e**(-dividend*time)
           option_rho = strike_price*time*e**(-rate*time)*stats.norm.cdf(d2)
        
        elif option_type=="PUT":
           option_delta = (stats.norm.cdf(d1) -1) * e**(-dividend*time)
           option_gamma= (stats.norm.pdf(d1)* e**(-dividend *time))/(stock_price* volatility*time **.5)
           option_theta= -stock_price* stats.norm.pdf(d1)*volatility*e**(-dividend * time)*0.5*time**(-0.5) - dividend * stock_price * stats.norm.cdf(-d1) * e**(-dividend*time) + rate * strike_price * e**(-rate*time) * stats.norm.cdf(-d2)
           option_vega = stock_price*time**0.5 * stats.norm.pdf(d1)*e**(-dividend*time)
           option_rho = -strike_price*time*e**(-rate*time)*stats.norm.cdf(-d2)


        option_delta = str(np.round(option_delta,6))
        output_list.insert(tk.END, "Delta:               " +option_delta)
        option_gamma =str(np.round(option_gamma,6))
        output_list.insert(tk.END, "Gamma:           " +option_gamma)
        option_theta = str(np.round(option_theta,6))
        output_list.insert(tk.END, "Theta:              " +option_theta)
        option_vega = str(np.round(option_vega,6))
        output_list.insert(tk.END, "Vega:               " +option_vega)
        option_rho =str(np.round(option_rho,6))
        output_list.insert(tk.END, "Rho:                " +option_rho)
        

    except:
        messagebox.showinfo(title='Error', text ="Make sure all fileds are filled")

def stock_price():
    temp = yf.Ticker(e_ticker.get().upper()).history()['Close'].iloc[-1]
    live_stock_price.set(np.round(temp,6))


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


root = tk.Tk()
root.geometry("350x500")
root.title("European Option Pricer")
live_stock_price = tk.StringVar()

output_list= tk.Listbox(root, height =8,width= 42)



# set up the parameters to calculate the option price using BS model
ticker = tk.Label(root, text="Stock Symbol", font=('Arial', 10))
ticker.place(x=20, y =30)

spot_price = tk.Label(root, text="Spot Price", font=('Arial', 10))
spot_price.place(x=20, y =60)

option_type = tk.Label(root, text="Option Type", font=('Arial', 10))
option_type.place(x=20, y =90)

strike_price = tk.Label(root, text="Strike Price", font=('Arial', 10))
strike_price.place(x=20, y =120)

rate = tk.Label(root, text="Risk Free Rate", font=('Arial', 10))
rate.place(x=20, y =150)

time_to_expir = tk.Label(root, text="Time (in Years)", font=('Arial', 10))
time_to_expir.place(x=20, y =180)

vol = tk.Label(root, text="Volatility", font=('Arial', 10))
vol.place(x=20, y =210)

div = tk.Label(root, text="Dividend Yield", font=('Arial', 10))
div.place(x=20, y =240)





e_ticker = tk.Entry()
e_ticker.place(x=150, y=30)

btn1 = tk.Button(root, text= "Get", font= ("Arial", 10), command=stock_price)
btn1.place(x=270, y =30)

e_spot_price = tk.Label(root ,textvariable=live_stock_price, font=('Arial', 10))
e_spot_price.place(x=150, y =60)

option_type_combobox = ttk.Combobox(root, values=['CALL', 'PUT'])
option_type_combobox.place(x=150, y=90)

e_strike_price = tk.Entry()
e_strike_price.place(x=150, y=120)

e_rate = tk.Entry()
e_rate.place(x=150, y=150)

e_time_to_expir = tk.Entry()
e_time_to_expir.place(x=150, y=180)

e_vol = tk.Entry()
e_vol.place(x=150, y=210)

e_div = tk.Entry()
e_div.place(x=150, y=240)

calculate = tk.Button(root, text="Calculate", font=('Arial', 10), bg='white', command= combine_funcs(black_scholes_merton, greeks))
calculate.place(x=150, y=270)




#display output 
results = tk.Label(root, text ="Results: ", font=('Arial', 12))
results.place(x=20, y=315)
output_list.place(x=20, y =340)




root.mainloop()
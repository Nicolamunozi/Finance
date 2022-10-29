"""
This has be done using:
https://medium.com/the-financial-journal/the-million-dollar-algorithm-straight-from-wall-street-3f88a62e3e0a

I needed money, so I wrote an algorithm. 
"""
#------------------Imports-----------------#

import numpy as np
import pandas as pd
import yfinance as yf

#---------------Constants-------------#

article_symbol = "BTC-USD"


#-----------------Clases-----------------#


class GetData(object):
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ticker = yf.Tickers(self.symbol)
        self.data = yf.download(tickers=(self.symbol),
                                period="1y", interval="1d",
                                group_by="ticker",
                                auto_adjust=True,
                                prepost=False)
        self.df = pd.DataFrame(self.data)

    def find_z(self):
        mean = self.df["Close"].mean()
        z_from_mean = float(
            (self.df["Close"].tail(1)-mean)/np.std(self.df["Close"]))
        return z_from_mean, self.df["Close"].tail(1)

    def company_info(self):

        ticker = yf.Ticker(self.symbol)
        self.info = ticker.info
        self.analyst = ticker.recommendations
        self.sustainability = ticker.sustainability
        self.major_holders = ticker.major_holders
        self.institutional_holders = ticker.institutional_holders
        return {"info": self.info,
                "analyst": self.analyst,
                "sustainability": self.sustainability,
                "major_holders": self.major_holders,
                "institutional_holders": self.institutional_holders}


#---------------Functions-----------#


def what_to_do(value):
    if value > 2.5:
        do = "Overbought alarm: Sell"
    elif value < -2.5:
        do = "Oversell alarm: Buy"
    else:
        do = "Normal Rank. Keep"
    return do

#-------------Tests--------------#

#bitcoin_data = GetData(article_symbol)
# BTC = GetData(article_symbol)
# BTC.find_z()

#----------Scripting-------------#


sym = input("Enter the symbol code: ")
sym_data = GetData(sym)
z, tail = sym_data.find_z()
do = what_to_do(z)
z = round(z, 2)

# Main Info
print(f"{sym}\n{tail}\n{do}\nValue represents {z} standard deviations")


# Additional Info.

additional_info = input(
    f"(This may take several time) Do you want additional info?(y/n)\n")
if additional_info == "y":
    info_dict = sym_data.company_info()
    print(
        f"{info_dict['info']['longName']}\n{info_dict['info']['sector']}\nFull time employee {info_dict['info']['fullTimeEmployees']}\n{info_dict['info']['longBusinessSummary']}\n {info_dict['info']['website']}\n {info_dict['info']['country']}\n {info_dict['info']['city']}")

   # Secondary Info.
    if do != "Normal Rank. Keep":
        print(
            f"{info_dict['major_holders']}\n{info_dict['institutional_holders']}\n{info_dict['sustainability']}")

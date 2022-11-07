import pandas as pd
from yahoo_fin import stock_info as si

# this is comming from: https://medium.com/gitconnected/how-to-get-all-stock-symbols-a73925c16a1b


def main():
    '''This is the main function in the article. Yet without any changes'''

    #------------Main Stocks exchanges in the US ---------------#

    df1 = pd.DataFrame(si.tickers_sp500())
    df2 = pd.DataFrame(si.tickers_nasdaq())
    df3 = pd.DataFrame(si.tickers_dow())
    df4 = pd.DataFrame(si.tickers_other())

    #------------ Each data frame to a list and then to a set ---------#

    sym1 = set(symbol for symbol in df1[0].values.tolist())
    sym2 = set(symbol for symbol in df2[0].values.tolist())
    sym3 = set(symbol for symbol in df3[0].values.tolist())
    sym4 = set(symbol for symbol in df4[0].values.tolist())

    #--Merging all different sets and symbols ----------#

    symbols = set.union(sym1, sym2, sym3, sym4)

    #------- identifying junk stocks ----- #

    my_list = ['W', 'R', 'P', 'Q']

    """
    W means there are outstanding warrants. We don’t want those.

    R means there is some kind of “rights” issue. Again, not wanted.

    P means “First Preferred Issue”. Preferred stocks are a separate entity.

    Q means bankruptcy. We don’t want those, either.
    """
    #-------control sets --------------#

    del_set = set()
    sav_set = set()
    for symbol in symbols:
        if len(symbol) > 4 and symbol[-1] in my_list:
            del_set.add(symbol)
        else:
            sav_set.add(symbol)

    print(f'Removed {len( del_set )} unqualified stock symbols...')
    print(f'There are {len( sav_set )} qualified stock symbols...')


if __name__ == "__main__":

    main()

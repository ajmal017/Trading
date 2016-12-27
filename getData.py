# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:57:54 2016

@author: Ratnadeepb
"""

from pandas import DataFrame;
import datetime;
import pandas as pd;
import quandl;

def getStockData(name, start, end='Today'):
    """
    Get the stock's OHLC data for the period in question.
    @Input:
        name:
            String or array of strings.
            The stocks whose data is to be downloaded
        start:
            String for the date since when the data is to be downloaded
        end:
            String for the date till when the data is to be downloaded.
            Default - Today
    @Output:
        data:
            A Pandas DataFrame containing the adjusted OHLC and Volume
            information.
            If there are any problem getting the data then partial or no data
            may be returned. The method is not atomic and it is up to the user
            to verify the data.
            Eg. print(getStockData(name, start, end).empty)
            And print(getStockData(name, start, end).columns.levels[0])
    """
    
    assert(isinstance(start, str));
    assert(isinstance(end, str));
    
    with open("myQuandlAuthToken.txt", 'r') as authtoken:
        token = authtoken.readline();
        
    if end == 'Today':
        end = datetime.date.today();
    
    data = DataFrame();
    last = None;
    
    try:
        if isinstance(name, str):
            ticker = "WIKI/" + name;
            data = quandl.get(ticker, start_date=start, end_date=end, 
            authtoken=token);
            data.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Ex-Dividend',
                   'Split Ratio'], axis=1, inplace=True)
            print("Downloaded data for {} between {} and {}".format(name, 
                  start, end));
        else:
            # There is a much easier way of getting data on multiple tickers
            # from Quandl. But I found it easier to control the columns this
            # way.
            for nm in name:
                last = nm;
                ticker = "WIKI/" + nm;
                temp = quandl.get(ticker, start_date=start, end_date=end, 
                                  authtoken=token);
                temp.drop(['Open', 'High', 'Low', 'Close', 'Volume',
                           'Ex-Dividend', 'Split Ratio'], axis=1, inplace=True)
                
                # Create a 2 level column where the first column identifies
                # the stock
                arr = [nm] * len(temp.columns);
                tuples = list(zip(arr, temp.columns));
                cols = pd.MultiIndex.from_tuples(tuples);
                temp.columns = cols;
                
                # Create the final DataFrame
                if data.empty:
                    data = temp;
                    print("Downloaded data for {} between {} and {}"
                          .format(nm, start, end));
                else:
                    dataTemp = pd.concat([data, temp], axis=1);
                    data = dataTemp;
                    print("Downloaded data for {} between {} and {}"
                          .format(nm, start, end));
    except:
        # Remember it failed to fetch data for last and whatever is left 
        # after last
        print("We failed to get data on the last {} stocks on your list."
              .format(len(name) - name.index(last)));
        print("The data is incomplete.");
    return data;
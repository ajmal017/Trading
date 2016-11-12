# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 16:40:05 2016

@author: Ratnadeepb
"""

import pandas as pd
import datetime

### Used if data is to be downloaded from Yahoo Finance
from pandas_datareader.data import DataReader

### Used in data is to be downloaded from Quandl
import quandl

def checkDate(filename):
    """
    INPUT
        @filename: The full path + name of the file from which the last date
        has to be fetched. This has to be either a CSV or an Excel file only.
    OUTPUT
        Returns the date after the last date in the file if the file exists
        Otherwise returns Null
    """
    ### The input must be a string
    if not isinstance(filename, str):
        print("The input type is not expected.")
    
    ### The file must be a csv or excel
    if filename[-3:] == 'csv':
        try:
            check = pd.read_csv(filename)
        ### Pandas' read_csv() function returns OSError if file is not found
        except OSError:
            return 'Null'
    elif filename[-4:] == 'xlsx':
        try:
            check = pd.read_excel(filename)
        ### Pandas' read_excel() function returns FileNotFoundError if file is
        ### not found
        except FileNotFoundError:
            return 'Null'
    ### Return 'Null' if the file is neither csv nor xlsx
    else:
        return 'Null'

    return datetime.date.strftime(datetime.datetime.strptime(check['Date']\
    [check.shape[0] - 1], '%Y-%m-%d')+datetime.timedelta(1), '%Y-%m-%d')


def downloadData(string):
    """
    INPUT
        @string: Source of data - Quandl or Yahoo
    OUTPUT
        The master security sheet is opened and data for the mentioned securties
        are downloaded from the mentioned source.
        The columns in the master sheet are:
        Country, Ticker, Staging and Dest
        
        For Quandl the dataFolder is D:\Personal\Projects\SecData\Quandl
        For Yahoo Finance: D:\Personal\Projects\SecData\Yahoo_Finance
    """
    
    ### The input must be string
    if not isinstance(string, str):
        print("The input type is not expected.")

    ### Read in the master sheet    
    masterFolder = "D:\\Trading\\Rawdata\\"
    ### My_Watch is the name of the sheet I want to read
    master = pd.read_excel(masterFolder+'Master_Sheet.xlsx', 'My_Watch')
    
    ### This is where the securities are stored
    dataFolder = "D:\\Trading\\Rawdata\\Securities\\"
    
    ### The input must be Quandl or Yahoo
    if string == 'Quandl':
        with open("D:\\Trading\\myQuandlAuthToken.txt", 'r') as authToken:
            auth = authToken.readline()
        
        ### i is the row count of the DataFrame master
        ### ticker is the name of the ticker
        ### Country is which country the ticker is registered
        for i, name, country, filename in zip(range(master.shape[0]), \
        master['Ticker'], master['Country'], master['Staging']):
            
            if country == 'USA':
                ticker = 'EOD/'+name
            else:
                ticker = 'XNSE/'+name
                
            ### Declare the path where it is to be stored
            ### Example: D:\Personal\Projects\SecData\Quandl\India
            path = dataFolder+country+"\\"+string+"\\"
            
            ### Set the date since when the data is to be downloaded
            lastDate = checkDate(path+filename)
            
            ### If the file does not exist then we want to download data
            ### for the last 5 years
            if lastDate == 'Null':
                end = datetime.date.today()
                lastDate = end.replace(year=end.year - 5)
            
            ### Download the data
            temp = quandl.get(ticker, authtoken=auth, start_date=lastDate)
            ### Save it to the Staging file
            temp.to_csv(path+filename+".csv")
    
    elif string == 'Yahoo':
        for i, name, country, filename in zip(range(master.shape[0]), \
        master['Ticker'], master['Country'], master['Staging']):
            
            ### The Indian stocks in Yahoo are listed with the suffix .NS
            if country == 'India':
                ticker = name+".NS"
            else:
                ticker = name
            
            ### Declare the path where it is to be stored
            ### Example: D:\Personal\Projects\SecData\Quandl\India
            path = dataFolder+country+"\\"+string+"\\"
            
            ### Set the date since when the data is to be downloaded
            lastDate = checkDate(path+filename)
            
            ### If the file does not exist then we want to download data
            ### for the last 5 years
            if lastDate == 'Null':
                end = datetime.date.today()
                lastDate = end.replace(year=end.year - 5)

            ### Download the data
            temp = DataReader(ticker, 'yahoo', start=lastDate)
            
            ### Save the data to the staging file
            temp.to_csv(path+filename+".csv")
    
    else:
        print("We can download data from the following only:")
        print("1. Quandl")
        print("2. Yahoo")
# Trading

This codebase is targeted at anyone who wants to use Python and Data Analysis to trade equities. As time progresses the codebase will keep growing to add more and more functionalities. The code is being released under the MIT License which basically means that you can use it for any project - commercial and otherwise - as long as you maintain the license.

Note: You need to setup your MySQL database. There are some hints on setting up the database in the creatingDB.sql file.

The code does the following:
1. First you need to create a watch list for the stocks that you want to trade in. Mine is an excel file where the sheet is called 'My_Watch'.
    The columns in the watch list are:

        +----------- +-------------- +------ +-----  +---------  +-------  +
        | Field      | Type          | Null  | Key   | Default   | Extra   |
        +-----------+:--------------:+------:+:-----:+:---------:+:-------:+ 
        | Country    | varchar(30)   | YES   | MUL   | NULL      |         |
        | Ticker     | varchar(50)   | NO    | PRI   | NULL      |         |
        | Staging    | varchar(100)  | NO    | MUL   | NULL      |         |
        | Quandl_DB  | varchar(30)   | YES   | MUL   | NULL      |         |
        +-----------+--------------  +------ +-----  +---------  +-------  +

        Country simply means which country the Ticker is valid in. Staging is the name of the csv file where the latest uploaded data is stored. And Quandl_DB points to the database in Quandl where this data can be found.
        
2. The downloadWatchList.py contains two functions - checkData() and downloadData().
    downloadData can be called as:
      downloadData('Quandl') or downloadData('Yahoo').
     This just decides where the stock data is to be downloaded from. All tickers from your watchlist are downlaoded given that the watchlist is setup correctly.
     The folder structure is hard-coded and you can change that.
     
     checkData() is used internally by downloadData() to decide the start date for downloading data. For the average user it would suffice to know that if you are downloading data for a new ticker then the last 5 years EoD would be downloaded; otherwise data since the last download will be downloaded.
     
     Pay attention to the folder structure.
     
     You may have to change the following given the particulars of your environment:
     masterFolder: This is where the master watch list is stored.
     dataFolder: This is essentially where the data will be stored.
     path: This is the actual path for the individual files.
        The path is typically like - dataFolder+country+"Quandl"
     
3. Create the two tables in your MySQL database:
    eqmasterlist and equities
    
    I have used SQLAlchemy Object Relational Mapper along with the pymysql driver.

4. Update eqmasterlist table with updateEqmasterlist.py. All you need to do is update your master sheet excel and run this program.

5. Next, to update the latest data into your MySQL database simply run the code in updateEquities.py.

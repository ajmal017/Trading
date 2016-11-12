### Update the equities table

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import pandas as pd

### Create the engine
engine = create_engine('mysql+pymysql://root:root123@localhost:3306/securities_master_db', echo = True)

### Create the session
Session = sessionmaker(bind=engine)
session = Session()

Base = automap_base()

Base.prepare(engine, reflect=True)

eqmasterlist = Base.classes.eqmasterlist
equities = Base.classes.equities

baseFolder = "D:\\Trading\\Rawdata\\Securities\\"

for instance in session.query(eqmasterlist):
    ### Setup the folder
    if instance.Country == 'USA':
        dataFolder = baseFolder + "USA\\"
        
        ### Update the Quandl data
        path = dataFolder + "Quandl\\"
        temp = pd.read_csv(path+instance.Staging+".csv")

        for i in range(temp.shape[0]):
            ### The conversions are required because MySQL can't translate
            ### numpy.float64 or numpy.int64
            session.add(equities(Ticker=instance.Ticker, 
                                 Date_E=temp.loc[i]['Date'], 
                                Open_P=float(temp.loc[i]['Adj_Open']), 
                                High=float(temp.loc[i]['Adj_High']), 
                                Low=float(temp.loc[i]['Adj_Low']), 
                                Close_P=float(temp.loc[i]['Adj_Close']),
                                Volume=int(temp.loc[i]['Adj_Volume']), 
                                Source="Quandl"))

            session.commit()
        
        ### Update the Yahoo data
        path = dataFolder + "Yahoo\\"
        temp = pd.read_csv(path+instance.Staging+".csv")

        for i in range(temp.shape[0]):
            session.add(equities(Ticker=instance.Ticker, 
                                 Date_E=temp.loc[i]['Date'],
                                Open_P=float(temp.loc[i]['Open']), 
                                High=float(temp.loc[i]['High']), 
                                Low=float(temp.loc[i]['Low']), 
                                Close_P=float(temp.loc[i]['Close']),
                                Volume=int(temp.loc[i]['Volume']), 
                                Adj_Close=float(temp.loc[i]['Adj Close']), 
                                Source="Yahoo"))

            session.commit()
    
    else:
        dataFolder = baseFolder + "India\\"
        
        ### Update the Quandl data
        path = dataFolder + "Quandl\\"
        temp = pd.read_csv(path+instance.Staging+".csv")

        for i in range(temp.shape[0]):
            session.add(equities(Ticker=instance.Ticker, 
                                 Date_E=temp.loc[i]['Date'], 
                                Open_P=float(temp.loc[i]['Open']), 
                                 High=float(temp.loc[i]['High']), 
                                Low=float(temp.loc[i]['Low']), 
                                Close_P=float(temp.loc[i]['Close']),
                                Volume=int(temp.loc[i]['Volume']), 
                                Source="Quandl"))

            session.commit()
        
        ### Update the Yahoo data
        path = dataFolder + "Yahoo\\"
        temp = pd.read_csv(path+instance.Staging+".csv")

        for i in range(temp.shape[0]):
            session.add(equities(Ticker=instance.Ticker, 
                                 Date_E=temp.loc[i]['Date'], 
                                 Open_P=float(temp.loc[i]['Open']), 
                                 High=float(temp.loc[i]['High']), 
                                 Low=float(temp.loc[i]['Low']), 
                                 Close_P=float(temp.loc[i]['Close']),
                                 Volume=int(temp.loc[i]['Volume']), 
                                 Adj_Close=float(temp.loc[i]['Adj Close']), 
                                 Source="Yahoo"))

            session.commit()
### http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html

### Update the eqmasterlist table

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

### Reflect the tables
Base.prepare(engine, reflect=True)

### Create the classes that map to the tables
eqmasterlist = Base.classes.eqmasterlist

### Add rows to eqmasterlist
masterFolder = "D:\\Trading\\Rawdata\\"
master = pd.read_excel(masterFolder+'Master_Sheet.xlsx', 'My_Watch')

for i in range(master.shape[0]):
	session.add(eqmasterlist(Country=master.loc[i]['Country'], Ticker=master.loc[i]['Ticker'], Staging=master.loc[i]['Staging'], Quandl_DB=master.loc[i]['Quandl_DB']))
	session.commit()
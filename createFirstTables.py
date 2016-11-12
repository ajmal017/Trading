### http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float

### Connect to the database
### The format is: dialect+driver://username:password@host:port/database
### Deafult format (uses mysqldb): dialect://username:password@host:port/database

engine = create_engine('mysql+pymysql://root:root123@localhost:3306/securities_master_db', echo = True)

### Set up the session
Session = sessionmaker(bind=engine)
session = Session()

### Map the class
### The Declarative system is used to map classes to table columns and instances of the classes to rows
Base = declarative_base()


class eqmasterlist(Base):
	__tablename__ = 'eqmasterlist'
	
	Country = Column(String(30), index=True)
	Ticker = Column(String(50), primary_key=True)
	Staging = Column(String(100), index=True, nullable=False)
	Quandl_DB = Column(String(30), index=True)
	
	def __repr__(self):
		return "<eqmasterlist(Country='%s', Ticker='%s', Staging='%s', Quandl_DB='%s')>" %(self.Country, self.Ticker, self.Staging, self.Quandl_DB)


class equities(Base):
	__tablename__ = 'equities'
	
	ID_T = Column(Integer, primary_key=True, autoincrement=True)
	Ticker = Column(String(50), ForeignKey('eqmasterlist.Ticker'))
	Date_E = Column(String(50))
	Open_P = Column(Float, nullable=False)
	High = Column(Float, nullable=False)
	Low = Column(Float, nullable=False)
	Close_P = Column(Float, nullable=False)
	Volume = Column(Integer, nullable=False)
	Adj_Close = Column(Float)
	Source = Column(String(20))
	
	def __repr__(self):
		return "<equities(Ticker='%s', Date_E='%s', Open_P='%f', High='%f', Low='%f', Close_P='%f', Volume='%f', Adj_Close='%s', Source='%s')>" %(self.Ticker, self.Date_E, self.Open_P, self.High, self.Low, self.Close_P, self.Volume, self.Adj_Close, self.Source)

### Creating the tables
Base.metadata.create_all(engine)
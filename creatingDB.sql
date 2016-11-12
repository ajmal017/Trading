-- Creating the database
create database securities_master_db;

-- Create the master list table
use securities_master_db;
create table EqMasterList (Country varchar(30), Ticker varchar(50) primary key, Staging varchar(100) not null, Quandl_DB varchar(30) not null);

-- Entering a row to the masterlist
insert into eqmasterlist (Country, Ticker, Staging, Dest) values('USA', 'EOD/AAPL', 'aapl-stg', 'aapl');

-- Creating the equities table
create table equities (id int(100) auto_increment primary key, Ticker varchar(50) not null, Date_E datetime not null, Open_P double not null, High double not null, Low double not null, Close_P double not null, Adj_Close double, Volume int not null);
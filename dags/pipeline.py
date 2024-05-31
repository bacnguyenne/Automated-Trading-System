# DAG object
import psycopg2.sql
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from main import MarketDataHandler

import psycopg2

import pandas as pd
import model


# with open('HOSE.txt', 'r') as f:
#     HOSE = f.read().splitlines()

# with open('/opt/airflow/dags/symbols.txt', 'r') as f:
#     HNX = f.read().splitlines()


# def getHNX(ti):
#     conn = psycopg2.connect(
#         database="postgres",
#         user='dbmasteruser',
#         password='ZinNopassword',
#         host='ls-65cbc248f7f6256b66e5d044234532bebe12d75b.cza8koy0izk1.ap-southeast-1.rds.amazonaws.com',
#         port='5432'
#     )
#     print("Connection: ", conn)
#     cur = conn.cursor()
#     cur.execute(
#         """CREATE TABLE IF NOT EXISTS market_data (
#             RType VARCHAR,
#             TradingDate DATE,
#             Time TIME,
#             Isin VARCHAR,
#             Symbol VARCHAR,
#             Ceiling FLOAT,
#             Floor FLOAT,
#             RefPrice FLOAT,
#             Open FLOAT,
#             High FLOAT,
#             Low FLOAT,
#             Close FLOAT,
#             AvgPrice FLOAT,
#             PriorVal FLOAT,
#             LastPrice FLOAT,
#             LastVol FLOAT,
#             TotalVal FLOAT,
#             TotalVol FLOAT,
#             BidPrice1 FLOAT,
#             BidPrice2 FLOAT,
#             BidPrice3 FLOAT,
#             BidPrice4 FLOAT,
#             BidPrice5 FLOAT,
#             BidPrice6 FLOAT,
#             BidPrice7 FLOAT,
#             BidPrice8 FLOAT,
#             BidPrice9 FLOAT,
#             BidPrice10 FLOAT,
#             BidVol1 FLOAT,
#             BidVol2 FLOAT,
#             BidVol3 FLOAT,
#             BidVol4 FLOAT,
#             BidVol5 FLOAT,
#             BidVol6 FLOAT,
#             BidVol7 FLOAT,
#             BidVol8 FLOAT,
#             BidVol9 FLOAT,
#             BidVol10 FLOAT,
#             AskPrice1 FLOAT,
#             AskPrice2 FLOAT,
#             AskPrice3 FLOAT,
#             AskPrice4 FLOAT,
#             AskPrice5 FLOAT,
#             AskPrice6 FLOAT,
#             AskPrice7 FLOAT,
#             AskPrice8 FLOAT,
#             AskPrice9 FLOAT,
#             AskPrice10 FLOAT,
#             AskVol1 FLOAT,
#             AskVol2 FLOAT,
#             AskVol3 FLOAT,
#             AskVol4 FLOAT,
#             AskVol5 FLOAT,
#             AskVol6 FLOAT,
#             AskVol7 FLOAT,
#             AskVol8 FLOAT,
#             AskVol9 FLOAT,
#             AskVol10 FLOAT,
#             MarketId VARCHAR,
#             Exchange VARCHAR,
#             TradingSession VARCHAR,
#             TradingStatus VARCHAR,
#             Change FLOAT,
#             RatioChange FLOAT,
#             EstMatchedPrice FLOAT,
#             Side VARCHAR,
#             CloseQtty FLOAT
#     )"""
#     )

#     for channel in HNX:
#         print("Channel: ", channel)
#         handler = MarketDataHandler(f'X:{channel}')
#         handler.main()
#         if handler.source:
#             print("Data: ", handler.source)
#             query = psycopg2.sql.SQL(
#                 """INSERT INTO market_data (
#                     RType, TradingDate, Time, Isin, Symbol, Ceiling, Floor, RefPrice, Open, High, Low, Close, 
#                     AvgPrice, PriorVal, LastPrice, LastVol, TotalVal, TotalVol, BidPrice1, BidPrice2, 
#                     BidPrice3, BidPrice4, BidPrice5, BidPrice6, BidPrice7, BidPrice8, BidPrice9, BidPrice10, 
#                     BidVol1, BidVol2, BidVol3, BidVol4, BidVol5, BidVol6, BidVol7, BidVol8, BidVol9, BidVol10, 
#                     AskPrice1, AskPrice2, AskPrice3, AskPrice4, AskPrice5, AskPrice6, AskPrice7, AskPrice8, 
#                     AskPrice9, AskPrice10, AskVol1, AskVol2, AskVol3, AskVol4, AskVol5, AskVol6, AskVol7, 
#                     AskVol8, AskVol9, AskVol10, MarketId, Exchange, TradingSession, TradingStatus, Change, 
#                     RatioChange, EstMatchedPrice, Side, CloseQtty
#                     ) VALUES (
#                         {RType}, TO_DATE({TradingDate}, 'DD/MM/YYYY'), {Time}, {Isin}, {Symbol}, {Ceiling}, {Floor}, 
#                         {RefPrice}, {Open}, {High}, {Low}, {Close}, NULLIF({AvgPrice}, 'NaN')::FLOAT, {PriorVal}, 
#                         {LastPrice}, {LastVol}, {TotalVal}, {TotalVol}, {BidPrice1}, {BidPrice2}, {BidPrice3}, 
#                         {BidPrice4}, {BidPrice5}, {BidPrice6}, {BidPrice7}, {BidPrice8}, {BidPrice9}, {BidPrice10}, 
#                         {BidVol1}, {BidVol2}, {BidVol3}, {BidVol4}, {BidVol5}, {BidVol6}, {BidVol7}, {BidVol8}, 
#                         {BidVol9}, {BidVol10}, {AskPrice1}, {AskPrice2}, {AskPrice3}, {AskPrice4}, {AskPrice5}, 
#                         {AskPrice6}, {AskPrice7}, {AskPrice8}, {AskPrice9}, {AskPrice10}, {AskVol1}, {AskVol2}, 
#                         {AskVol3}, {AskVol4}, {AskVol5}, {AskVol6}, {AskVol7}, {AskVol8}, {AskVol9}, {AskVol10}, 
#                         {MarketId}, {Exchange}, {TradingSession}, {TradingStatus}, {Change}, {RatioChange}, 
#                         {EstMatchedPrice}, {Side}, {CloseQtty}
#                     )"""
#             ).format(**{key: psycopg2.sql.Literal(value) for key, value in handler.source.items()})
#             cur.execute(query)
#             print("Data inserted")

#     conn.commit()
#     cur.close()
#     conn.close()

def predict_next_days():
    data = pd.read_csv('opt/airflow/dags/FPT.csv')
    

    

    
default_args = {
    'owner': 'TaiDuongRepo',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 13),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


# Creating DAG Object
with DAG(
    "ATS_pipeline",
    default_args=default_args,
    catchup=False,
    schedule_interval='* * * * *',
    max_active_runs=1,
) as dag:
    pass
# import ssi_fc_data
import config
import json
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fc_data.fc_md_client import MarketDataClient

import psycopg2


INSERT = f"""
	INSERT INTO stocks_real_time (
        RType, TradingDate, Time, Isin, Symbol, Ceiling, Floor, RefPrice, Open, High, Low, Close, AvgPrice, PriorVal, LastPrice, LastVol, TotalVal, TotalVol, 
        BidPrice1, BidPrice2, BidPrice3, BidPrice4, BidPrice5, BidPrice6, BidPrice7, BidPrice8, BidPrice9, BidPrice10, 
        BidVol1, BidVol2, BidVol3, BidVol4, BidVol5, BidVol6, BidVol7, BidVol8, BidVol9, BidVol10, 
        AskPrice1, AskPrice2, AskPrice3, AskPrice4, AskPrice5, AskPrice6, AskPrice7, AskPrice8, AskPrice9, AskPrice10, 
        AskVol1, AskVol2, AskVol3, AskVol4, AskVol5, AskVol6, AskVol7, AskVol8, AskVol9, AskVol10, 
        MarketId, Exchange, TradingSession, TradingStatus, Change, RatioChange, EstMatchedPrice, Side, CloseQtty
    ) VALUES (
        %s, to_date(%s, 'DD/MM/YYYY'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

def on_message(message):
	data = json.loads(message['Content'])
	print(data)
	insert_data(data)
	print('Data inserted successfully!')

def insert_data(data): 
	try:
		cursor = conn.cursor()
		cursor.execute(INSERT, list(data.values()))
		conn.commit()
		cursor.close()
		print('Data inserted successfully!')
	except psycopg2.Error as e:
		conn.rollback()
		print(f'error: {e.pgcode} - {e.pgerror}')
    

def on_error(error):
	print(error)
     
def main(channel):
	mm = MarketDataStream(config, MarketDataClient(config))
	mm.start(on_message, on_error, channel)
	message = None
	while message != "exit()":
		message = input(">> ")
		if message is not None and message != "" and message != "exit()":
			mm.swith_channel(message)


conn = psycopg2.connect(
	database="postgres",
	user=,
	password=,
	host=,
	port='5432'
)

main('X:ALL')
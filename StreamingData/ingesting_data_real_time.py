import time
import psycopg2
import json

from psycopg2.extras import execute_values
from datetime import datetime

import config
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fc_data.fc_md_client import MarketDataClient

class WebsocketPipeline():
    # name of the table
    DB_TABLE = 'stocks_real_time'

    # columns in the hypertable in the correct order
    DB_COLUMNS = ['RType', 'TradingDate', 'Time', 'Isin', 'Symbol', 'Ceiling', 'Floor', 'RefPrice', 'Open', 'High', 'Low', 'Close', 'AvgPrice', 'PriorVal', 'LastPrice', 'LastVol', 'TotalVal', 'TotalVol', 'BidPrice1', 'BidPrice2', 'BidPrice3', 'BidPrice4', 'BidPrice5', 'BidPrice6', 'BidPrice7', 'BidPrice8', 'BidPrice9', 'BidPrice10', 'BidVol1', 'BidVol2', 'BidVol3', 'BidVol4', 'BidVol5', 'BidVol6', 'BidVol7', 'BidVol8', 'BidVol9', 'BidVol10', 'AskPrice1', 'AskPrice2', 'AskPrice3', 'AskPrice4', 'AskPrice5', 'AskPrice6', 'AskPrice7', 'AskPrice8', 'AskPrice9', 'AskPrice10', 'AskVol1', 'AskVol2', 'AskVol3', 'AskVol4', 'AskVol5', 'AskVol6', 'AskVol7', 'AskVol8', 'AskVol9', 'AskVol10', 'MarketId', 'Exchange', 'TradingSession', 'TradingStatus', 'Change', 'RatioChange', 'EstMatchedPrice', 'Side', 'CloseQtty']

    # batch size for inserts
    MAX_BATCH_SIZE = 1000

    def __init__(self, conn) -> None:
        """Connect to the database web socket server and stream data into the database
        
        Args:
            conn: psycopg2 connection object
        """
        self.conn = conn
        self.current_batch = []
        self.insert_counter = 0

    def _insert_values(self, data):
        if self.conn is not None:
            cursor = self.conn.cursor()
            sql = f"""
            INSERT INTO {self.DB_TABLE} ({','.join(self.DB_COLUMNS)})
            VALUES %s;"""
            execute_values(cursor, sql, data)
            self.conn.commit()

    def _on_event(self, event):
        """This function gets called whenever there's a new data record coming back from the server
        
        Args:
            event (dict): data record"""
        event = json.loads(event['Content'])
        if event['RType'] == 'X':
            # data record
            timestamp = datetime.utcfromtimestamp(event['Time'])
            data = (event['RType'], event['TradingDate'], timestamp, event['Isin'], event['Symbol'], event['Ceiling'], event['Floor'], event['RefPrice'], event['Open'], event['High'], event['Low'], event['Close'], event['AvgPrice'], event['PriorVal'], event['LastPrice'], event['LastVol'], event['TotalVal'], event['TotalVol'], event['BidPrice1'], event['BidPrice2'], event['BidPrice3'], event['BidPrice4'], event['BidPrice5'], event['BidPrice6'], event['BidPrice7'], event['BidPrice8'], event['BidPrice9'], event['BidPrice10'], event['BidVol1'], event['BidVol2'], event['BidVol3'], event['BidVol4'], event['BidVol5'], event['BidVol6'], event['BidVol7'], event['BidVol8'], event['BidVol9'], event['BidVol10'], event['AskPrice1'], event['AskPrice2'], event['AskPrice3'], event['AskPrice4'], event['AskPrice5'], event['AskPrice6'], event['AskPrice7'], event['AskPrice8'], event['AskPrice9'], event['AskPrice10'], event['AskVol1'], event['AskVol2'], event['AskVol3'], event['AskVol4'], event['AskVol5'], event['AskVol6'], event['AskVol7'], event['AskVol8'], event['AskVol9'], event['AskVol10'], event['MarketId'], event['Exchange'], event['TradingSession'], event['TradingStatus'], event['Change'], event['RatioChange'], event['EstMatchedPrice'], event['Side'], event['CloseQtty'])

            # add new data record to batch
            self.current_batch.append(data)
            print(f"Current batch size: {len(self.current_batch)}")

            # ingest data if max batch size is reached then reset the batch
            if len(self.current_batch) == self.MAX_BATCH_SIZE:
                self._insert_values(self.current_batch)
                self.insert_counter += 1
                print(f"Batch insert #{self.insert_counter}")
                self.current_batch = []

    def _on_error(self, error):
        """This function gets called whenever there's an error coming back from the server

        Args:
            error (str): error message
        """
        print(error)

    def start(self, symbols):
        """Connect to the websocket server and start streaming real-time data into the database
        
        Args:
            symbols (list of symbols): List of stock symbols
        """
        mm = MarketDataStream(config, MarketDataClient(config))
        mm.start(self._on_event, self._on_error, symbols)
        message = None
        while message != "exit()":
            message = input(">> ")
            if message is not None and message != "" and message != "exit()":
                mm.swith_channel(message)

        
if __name__ == '__main__':
    conn = psycopg2.connect(
        database="postgres",
        user=,
        password=,
        host=,
        port='5432'
	)

    symbols = 'X:ALL'

    websocket = WebsocketPipeline(conn)
    websocket.start(symbols)
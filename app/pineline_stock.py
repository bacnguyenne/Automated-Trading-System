import os
import time
import json
import requests
import schedule
import datetime
import pytz
import config
import psycopg2
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fc_data.fc_md_client import MarketDataClient
from ssi_fc_data import fc_md_client , model

def set_access_token():
    client = fc_md_client.MarketDataClient(config)
    # print(client.access_token(model.accessToken(config.consumerID, config.consumerSecret)))
    access_token = client.access_token(model.accessToken(config.consumerID, config.consumerSecret))
    access_token = access_token['data']['accessToken']
    with open('config.py', 'r') as file:
        data = file.readlines()
        data[3] = f'access_jwt = "{access_token}"\n'
        file.close()
    with open('config.py', 'w') as file:
        file.writelines(data)
        file.close()


#get market data message
def get_market_data(message):
	print(message)


#get error
def getError(error):
	print(error)


#main function
def streaming():
	selected_channel = "ALL"
	mm = MarketDataStream(config, MarketDataClient(config))
	mm.start(get_market_data, getError, selected_channel)
	message = None
	while message != "exit()":
		message = "ALL"
		if message is not None and message != "" and message != "exit()":
			mm.swith_channel(message)

def run_streaming():
    now = datetime.datetime.now(pytz.timezone('Asia/Bangkok'))
    if now.weekday() < 5:  # Check if it's Monday (0) to Friday (4)
        current_time = now.time()
        if (datetime.time(9, 15) <= current_time <= datetime.time(11, 30)) or \
           (datetime.time(13, 0) <= current_time <= datetime.time(14, 30)):
            streaming()

def create_table():
    # Database connection parameters
    conn = psycopg2.connect(
        host="your_host",  # e.g., "localhost" or IP address
        database="your_database",
        user="your_username",
        password="your_password"
    )
    cur = conn.cursor()

    # Create table SQL query
    create_table_query = """
    CREATE TABLE IF NOT EXISTS market_data (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        data JSON NOT NULL
    );
    """

    try:
        # Execute the query
        cur.execute(create_table_query)
        conn.commit()  # Commit changes to the database
        print("Table created successfully")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close communication with the database
        cur.close()
        conn.close()

def save_to_postgres(message):
    """Save the fetched data to PostgreSQL."""
    conn = psycopg2.connect(
        host="localhost",
        database="your_database",
        user="your_user",
        password="your_password"
    )
    cur = conn.cursor()
    try:
        # Assuming message is a dictionary that can be serialized to JSON
        cur.execute("INSERT INTO market_data (timestamp, data) VALUES (%s, %s)",
                    (datetime.now(pytz.timezone('Asia/Bangkok')), Json(message)))
        conn.commit()
    except Exception as e:
        print("Failed to insert data:", e)
    finally:
        cur.close()
        conn.close()
        
def schedule_streaming():
    schedule.every().minute.do(run_streaming)
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    create_table()
    schedule_streaming()

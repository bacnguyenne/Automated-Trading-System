# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from ssi_fc_data.fc_md_stream import MarketDataStream
# from ssi_fc_data.fc_md_client import MarketDataClient
# from ssi_fc_data import fc_md_client, model
# import pytz

# default_args = {
#     'owner': 'ZinNoDag',
#     'depends_on_past': False,
#     'start_date': datetime(2024, 4, 20),
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# # Set access token and update configuration file
# def set_access_token():
#     client = fc_md_client.MarketDataClient(config)
#     access_token = client.access_token(model.accessToken(config.consumerID, config.consumerSecret))
#     access_token = access_token['data']['accessToken']
#     with open('config.py', 'r') as file:
#         data = file.readlines()
#     data[3] = f'access_jwt = "{access_token}"\n'
#     with open('config.py', 'w') as file:
#         file.writelines(data)

# # Define function to fetch market data
# def get_market_data():
#     selected_channel = "ALL"
#     mm = MarketDataStream(config, MarketDataClient(config))
#     mm.start(print, print, selected_channel)
#     message = "ALL"
#     while message != "exit()":
#         mm.switch_channel(message)
#         message = None  # You should implement exit condition or interrupt based on your need

# # Create DAG
# dag = DAG(
#     'market_data_streaming',
#     default_args=default_args,
#     description='A DAG to stream market data daily',
#     schedule_interval='0 9 * * 1-5',  # At 09:00 on every day-of-week from Monday through Friday
#     catchup=False,
# )

# # Set Access Token Task
# t1 = PythonOperator(
#     task_id='set_access_token',
#     python_callable=set_access_token,
#     dag=dag,
# )

# # Get Market Data Task
# t2 = PythonOperator(
#     task_id='get_market_data',
#     python_callable=get_market_data,
#     dag=dag,
# )

# t1 >> t2  # Define dependencies: t1 must run before t2

from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook


def get_stock_data(ti):
    """
    Get stock data from Yahoo Finance
    :param ti: Task Instance
    :return: Stock data
    """
    BASE_URL = "https://finance.yahoo.com"
    # INDEX = "NASDAQ"
    SYMBOL = "AAPL"
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    TARGET_URL = f"{BASE_URL}/quote/{SYMBOL}?.tsrc=fin-srch"

    page = requests.get(TARGET_URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')

    items = soup.find_all('li', {'class': 'svelte-tx3nkj'})
    stock_description = {}
    for item in items:
        item_label = item.find('span', {'class': 'label'}).text
        item_value = item.find('span', {'class': 'value'}).text
        print(item_label, item_value)
        stock_description[item_label] = item_value

    ti.xcom_push(key='stock_data', value=stock_description)

    return stock_description

def transform_data(ti):
    transformed_data = []
    stock_data = ti.xcom_pull(key='stock_data', task_ids='get_stock_records')
    for stock in stock_data:
        previous_close = float(stock['Previous Close'])
        open = float(stock['Open'])
        volume = float(stock['Volume'])
        avg_volume = float(stock['Avg. Volume'])

        transformed_data.append((previous_close, open, volume, avg_volume))

        ti.xcom_push(key='transformed_data', value=transformed_data)


def insert_records(ti):
    pg_hook = PostgresHook(postgres_conn_id='postgres_localhost', schema='airflow_db_connection')
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    transformed_data = ti.xcom_pull(key='transformed_data', task_ids='transform_stock_records')
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS stock_table (previous_close FLOAT, open FLOAT, volume FLOAT, avg_volume FLOAT)"
    )

    for record in transformed_data:
        cursor.execute(
            "INSERT INTO stock_table (previous_close, open, volume, avg_volume) VALUES (%s, %s, %s, %s)", record
        )

    connection.commit()
    cursor.close()
    connection.close()

# Defining the DAG
default_args = {
    'owner': 'TaiDuongRepo',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'stock_data_pipeline',
    default_args=default_args,
    description='A simple stock data pipeline',
    schedule_interval='* * * * *',
)


from datetime import datetime, timedelta

import os, json, pathlib, psycopg2
import pandas as pd

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

    print('stock_description:', stock_description)
    ti.xcom_push(key='stock_data', value=stock_description)



def transform_data(ti):
    transformed_data = []
    stock = ti.xcom_pull(key='stock_data', task_ids='get_stock_data')
    print('stock_description:', stock)
    
    previous_close = float(stock['Previous Close'])
    open = float(stock['Open'])
    volume = float(stock['Volume'].replace(',', ''))
    avg_volume = float(stock['Avg. Volume'].replace(',', ''))

    transformed_data.append((previous_close, open, volume, avg_volume))

    ti.xcom_push(key='transformed_data', value=transformed_data)
    
    print('transformed_data:', transformed_data)
        


def insert_records(ti):
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_default",
        host='host.docker.internal',
        port='5432',
        database='airflow',
        user='airflow',
        password='airflow'
    )

    # conn = psycopg2.connect(
    #     database='airflow',
    #     user='airflow',
    #     password='airflow',
    #     host='localhost',
    #     port='5432'
    # )

    connection = pg_hook.get_conn()
    print(connection)
    cursor = connection.cursor()
    # cursor = conn.cursor()
    transformed_data = ti.xcom_pull(key='transformed_data', task_ids='transform_stock_records')
    print('transform data: ',transform_data)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS stock_table (previous_close FLOAT, open FLOAT, volume FLOAT, avg_volume FLOAT)"
    )

    for record in transformed_data:
        print('record:', record)
        cursor.execute(
            "INSERT INTO stock_table (previous_close, open, volume, avg_volume) VALUES (%s, %s, %s, %s)", record
        )

    connection.commit()
    # conn.commit()
    cursor.close()
    # conn.close()
    connection.close()

def check_db():
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_default",
        host='host.docker.internal',
        port='5432',
        database='airflow',
        user='airflow',
        password='airflow'
    )

    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM stock_table"
    )

    records = cursor.fetchall()
    print('records:', records)

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
    render_template_as_native_obj=True
)


get_stock_data_task = PythonOperator(
    task_id='get_stock_data',
    python_callable=get_stock_data,
    dag=dag
)

transform_data_task = PythonOperator(
    task_id='transform_stock_records',
    python_callable=transform_data,
    dag=dag
)

insert_records_task = PythonOperator(
    task_id='insert_stock_records',
    python_callable=insert_records,
    dag=dag
)

check_db_task = PythonOperator(
    task_id='check_db',
    python_callable=check_db,
    dag=dag
)


get_stock_data_task >> transform_data_task >> insert_records_task >> check_db_task

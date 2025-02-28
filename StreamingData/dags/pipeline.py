# DAG object
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
# from main import MarketDataHandler
import psycopg2
import pandas as pd
import model


def predict_next_days():
    data = pd.read_csv('/opt/airflow/dags/FPT.csv')
    symbol = 'FPT'
    close_df= model.preprocess_data(data, symbol)
    x_train, y_train, test_data, scaler = model.create_train_test_data(close_df)
    _model = model.train_model(x_train, y_train)

    last_data = close_df.values[-30:]
    current_price = close_df.values[-1, 0]

    predictions = model.predict_next_days(_model, last_data, scaler)
    percentage_changes = model.calculate_percentage_change(predictions, current_price)

    print("Precentage Changes: ", percentage_changes)

    return symbol, close_df.index[-1], float(current_price), float(predictions[0][0]), float(predictions[1][0])


def insert_data(**kwargs):
    ti = kwargs['ti']
    symbol, date, close_price, next_day_price, next_2_day_price = ti.xcom_pull(task_ids='predict_task')

    insert_query = """
        INSERT INTO predict_price (symbol, date, close_price, next_day_price, next_2_day_price)
        VALUES (%s, %s, %s, %s, %s)
    """

    conn = psycopg2.connect(
        database="postgres",
        user=,
        password=,
        host=,
        port='5432'
    )

    print("Conncetion: ", conn)
    print("Data: ", symbol, date, close_price, next_day_price, next_2_day_price)
    cur = conn.cursor()
    try:
        cur.execute(insert_query, (symbol, date, close_price, next_day_price, next_2_day_price))
    except Exception as e:
        print("Failed to insert data:", e)
    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted successfully")
    
  
default_args = {
    'owner': 'ATS_airflow',
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
    schedule_interval='0 0 * * 1-5',
    # max_active_runs=1,
) as dag:
    predict_task = PythonOperator(
        task_id='predict_task',
        python_callable=predict_next_days
    )

    insert_task = PythonOperator(
        task_id='insert_task',
        python_callable=insert_data,
        provide_context=True
    )

    predict_task >> insert_task
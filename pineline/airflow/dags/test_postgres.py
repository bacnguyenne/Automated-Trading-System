# from airflow import DAG
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from datetime import datetime

# default_args = {
#     'owner': 'airflow',
#     'start_date': datetime(2023, 1, 1),
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# dag = DAG('test_postgres_connection',
#           default_args=default_args,
#           schedule_interval='@daily')

# task1 = PostgresOperator(
#     task_id='run_sql_query',
#     postgres_conn_id='your_connection_id',
#     sql="SELECT * FROM your_table;",
#     dag=dag,
# )

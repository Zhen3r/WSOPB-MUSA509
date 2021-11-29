from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(dag_id='addresses_pipeline',
         schedule_interval='@daily',
         start_date=datetime(2021, 11, 29),
         catchup=False) as dag:

    # EXTRACT TASKS
    downloadACS = BashOperator(
        task_id='downloadACS',
        bash_command='python ./dataPipeline/downloadACS.py',
        dag=dag)

    downloadParks = BashOperator(
        task_id='downloadParks',
        bash_command='python ./dataPipeline/downloadParks.py',
        dag=dag)

    # TRANSFORM TASKS
    transformACS = BashOperator(
        task_id='transformACS',
        bash_command='python ./dataPipeline/transformACS.py',
        dag=dag)

# DEPENDENCIES
downloadACS >> transformACS
downloadParks >> transformACS

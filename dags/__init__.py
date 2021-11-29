from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(dag_id='park_pipeline',
         schedule_interval='@daily',
         start_date=datetime(2021, 11, 29),
         catchup=False) as dag:

    # EXTRACT TASKS
    downloadACS = BashOperator(
        task_id='downloadACS',
        bash_command='/home/zhen/conda/envs/air/bin/python /home/zhen/code/musa509-final-proj/dags/dataPipeline/downloadACS.py',
        dag=dag)

    downloadParks = BashOperator(
        task_id='downloadParks',
        bash_command='/home/zhen/conda/envs/air/bin/python /home/zhen/code/musa509-final-proj/dags/dataPipeline/downloadParks.py',
        dag=dag)

    # TRANSFORM TASKS
    transformACS = BashOperator(
        task_id='transformACS',
        bash_command='/home/zhen/conda/envs/air/bin/python /home/zhen/code/musa509-final-proj/dags/dataPipeline/transformACS.py',
        dag=dag)

# DEPENDENCIES
downloadACS >> transformACS
downloadParks >> transformACS

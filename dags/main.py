from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

bash_command = "cd /home/zhen/code/musa509-final-proj && /home/zhen/conda/envs/509/bin/python -m dags.dataPipeline._"
bash_command_proxy = "cd /home/zhen/code/musa509-final-proj && proxychains /home/zhen/conda/envs/509/bin/python -m dags.dataPipeline._"

with DAG(dag_id='park_pipeline',
         schedule_interval='@daily',
         start_date=datetime(2021, 11, 29),
         catchup=False) as dag:

    # EXTRACT TASKS
    downloadACS = BashOperator(
        task_id='downloadACS',
        bash_command=bash_command_proxy.replace("_", "downloadACS"),
        dag=dag)

    downloadParks = BashOperator(
        task_id='downloadParks',
        bash_command=bash_command_proxy.replace("_", "downloadParks"),
        dag=dag)

    # TRANSFORM TASKS
    transformACS = BashOperator(
        task_id='transformACS',
        bash_command=bash_command.replace("_", "transformACS"),
        dag=dag)

    # GENERATE WEB RESOURCES
    generateSection1 = BashOperator(
        task_id='generateSection1',
        bash_command=bash_command.replace("_", "generateSection1"),
        dag=dag)

# DEPENDENCIES
downloadACS >> transformACS
downloadParks >> transformACS

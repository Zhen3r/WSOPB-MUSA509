from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime

bash_command = "cd /home/zhen/code/musa509-final-proj && /home/zhen/conda/envs/509/bin/python -m dags.dataPipeline._"
bash_command_proxy = "cd /home/zhen/code/musa509-final-proj && proxychains /home/zhen/conda/envs/509/bin/python -m dags.dataPipeline._"

with DAG(dag_id='park_pipeline',
         schedule_interval='@monthly',
         start_date=datetime(2021, 11, 29),
         catchup=False) as dag:

    # EXTRACT TASKS
    downloadACS = BashOperator(
        task_id='downloadACS',
        bash_command=bash_command_proxy.replace("_", "downloadACS"),
        trigger_rule="all_done",
        dag=dag)

    downloadParks = BashOperator(
        task_id='downloadParks',
        bash_command=bash_command_proxy.replace("_", "downloadParks"),
        trigger_rule="all_done",
        dag=dag)

    downloadCitylimits = BashOperator(
        task_id='downloadCitylimits',
        bash_command=bash_command_proxy.replace("_", "downloadCitylimits"),
        trigger_rule="all_done",
        dag=dag)

    downloadFlood = BashOperator(
        task_id='downloadFlood',
        bash_command=bash_command_proxy.replace("_", "downloadFlood"),
        trigger_rule="all_done",
        dag=dag)

    downloadLanduse = BashOperator(
        task_id='downloadLanduse',
        bash_command=bash_command_proxy.replace("_", "downloadLanduse"),
        trigger_rule="all_done",
        dag=dag)

    downloadBuildingvolume = BashOperator(
        task_id='downloadBuildingvolume',
        bash_command=bash_command_proxy.replace("_", "downloadBuildingvolume"),
        trigger_rule="all_done",
        dag=dag)

    downloadLandvalue = BashOperator(
        task_id='downloadLandvalue',
        bash_command=bash_command_proxy.replace("_", "downloadLandvalue"),
        trigger_rule="all_done",
        dag=dag)

    downloadTracts = BashOperator(
        task_id='downloadTracts',
        bash_command=bash_command.replace("_", "downloadTracts"),
        trigger_rule="all_done",
        dag=dag)

    # TRANSFORM TASKS
    transformACS = BashOperator(
        task_id='transformACS',
        bash_command=bash_command.replace("_", "transformACS"),
        trigger_rule="all_done",
        dag=dag)

    transformBuildingVolume = BashOperator(
        task_id='transformBuildingVolume',
        bash_command=bash_command.replace("_", "transformBuildingVolume"),
        trigger_rule="all_done",
        dag=dag)

    transformCost = BashOperator(
        task_id='transformCost',
        bash_command=bash_command.replace("_", "transformCost"),
        trigger_rule="all_done",
        dag=dag)

    transformFlood = BashOperator(
        task_id='transformFlood',
        bash_command=bash_command.replace("_", "transformFlood"),
        trigger_rule="all_done",
        dag=dag)

    transformIndex = BashOperator(
        task_id='transformIndex',
        bash_command=bash_command.replace("_", "transformIndex"),
        trigger_rule="all_done",
        dag=dag)

    transformLanduse = BashOperator(
        task_id='transformLanduse',
        bash_command=bash_command.replace("_", "transformLanduse"),
        trigger_rule="all_done",
        dag=dag)

    transformLandvalue = BashOperator(
        task_id='transformLandvalue',
        bash_command=bash_command.replace("_", "transformLandvalue"),
        trigger_rule="all_done",
        dag=dag)

    transformTemperature = BashOperator(
        task_id='transformTemperature',
        bash_command=bash_command.replace("_", "transformTemperature"),
        trigger_rule="all_done",
        dag=dag)

    # GENERATE WEB RESOURCES
    generateSection1 = BashOperator(
        task_id='generateSection1',
        bash_command=bash_command.replace("_", "generateSection1"),
        trigger_rule="all_done",
        dag=dag)

    generateSection2 = BashOperator(
        task_id='generateSection2',
        bash_command=bash_command.replace("_", "generateSection2"),
        trigger_rule="all_done",
        dag=dag)

    generateSection3 = BashOperator(
        task_id='generateSection3',
        bash_command=bash_command.replace("_", "generateSection3"),
        trigger_rule="all_done",
        dag=dag)

    generateSection4 = BashOperator(
        task_id='generateSection4',
        bash_command=bash_command.replace("_", "generateSection4"),
        trigger_rule="all_done",
        dag=dag)

    generateSection5 = BashOperator(
        task_id='generateSection5',
        bash_command=bash_command.replace("_", "generateSection5"),
        trigger_rule="all_done",
        dag=dag)

    generateSection0 = BashOperator(
        task_id='generateSection0',
        bash_command=bash_command.replace("_", "generateSection0"),
        trigger_rule="all_done",
        dag=dag)

# DEPENDENCIES
E = DummyOperator(task_id='wait_for_downloads')
T = DummyOperator(task_id='wait_for_transform')

[downloadACS, downloadParks, downloadBuildingvolume,
 downloadCitylimits, downloadFlood, downloadLanduse,
 downloadLandvalue, downloadTracts, ] >> E

E >> [transformACS, transformBuildingVolume, transformTemperature,
      transformFlood, transformLanduse, transformLandvalue]
[transformBuildingVolume, transformLandvalue, transformLanduse] >> transformCost
[transformACS, transformCost,
 transformFlood, transformTemperature] >> transformIndex
transformIndex >> T

T >> [generateSection0, generateSection1, generateSection2,
      generateSection3, generateSection4, generateSection5]

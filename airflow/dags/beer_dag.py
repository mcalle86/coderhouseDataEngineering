from airflow.decorators import task, dag
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(start_date=datetime(2023,11,1), schedule_interval='@daily', catchup=False)

def beer_dag():

    @task()
    def t1():
        pass

    t2 = BashOperator(
        task_id = 't2',
        bash_command='echo "Iniciando Proceso"'
    )
    t3 = DockerOperator(
        task_id = 't3',
        #imagen creaddda en el host
        image='beer:latest',
        #comunicación con docker engine de host
        docker_url="unix://var/run/docker.sock",
        #Indicación de borrado del contenedor luego de la ejecución, se comenta solo con el proposito
        #de poder comprobar si se realizó la ejecución.
        #auto_remove=True,
        network_mode="bridge",
        do_xcom_push=True,
    )
    
    t1() >> t2 >> t3

dag = beer_dag()
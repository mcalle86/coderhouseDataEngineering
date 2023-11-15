from airflow.decorators import task, dag
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime
import pendulum

def _email(mens):
    mensaje = mens[2]
    print(f'variable: {mensaje}')
    if mensaje == '0':
        msg = "Proceso Finalizado correctamente"
    elif mensaje == '1':
        msg = "Error al obtener datos de la API"
    elif mensaje == '2':
        msg = "Error de conexión con la DB en Redshift"
    elif mensaje == '3':
        msg = "Error de volcado de datos en tabla staging"
    elif mensaje == '4':
        msg = "Error durante la inserción de datos en tabla cerveza"
    elif mensaje == '5':
        msg = "Error durante el borrado de tabla staging"
    else:
        msg = "Salio por cualquier lado"    
    return msg

@dag(
    schedule_interval='@daily'
    ,start_date=pendulum.datetime(2023, 11, 2, tz="America/Argentina/Buenos_Aires")
    ,catchup=False
    ,tags=['Entrega Final']
)

def beer_dag():

    @task(task_id= 'Inicio')
    def inicio():
        pass

    
    procesoBeer = DockerOperator(
        task_id = 'procesoBeer',
        #imagen creaddda en el host
        image='beer_env:latest',
        environment= {'SERVIDOR_REDSHIFT': "data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com",
                    'DB_REDSHIFT': "data-engineer-database",
                    'PUERTO_REDSHIFT': 5439,
                    'USUARIO_REDSHIFT': "marcocalle86_coderhouse",
                    'CLAVE_REDSHIFT': "ouCZJ8c2z0",
                    'SIZER':3},
        #comunicación con docker engine de host
        docker_url="unix://var/run/docker.sock",
        #Indicación de borrado del contenedor luego de la ejecución, se comenta solo con el proposito
        #de poder comprobar si se realizó la ejecución.
        auto_remove=True,
        network_mode="bridge",
        do_xcom_push=True,
    )
    #Tomo el valor del xcom return value de DockerOperator y analizo si el proceso ejecutado se realizo correctamente
    #o si ocurrió un error en alguno de los pasos. 
    creaMensaje = PythonOperator(
        task_id = "creaMensaje",
        python_callable=_email,
        op_kwargs={'mens':'{{ ti.xcom_pull(task_ids=[\'procesoBeer\']) }}'},
        do_xcom_push=True,
    )

    #Toma el mensaje de la funcion _email() y la incluye en un correo que va a ser enviado al destinatario
    #indicando si el proceso finalizó correctamente o si hubo un error en alguno de los pasos.
    envioEmail = EmailOperator(
       task_id='envioEmail',
       to='marcocalle86@gmail.com',
       subject='Proceso Beer',
       html_content="<h3>Informe de proceso Beer</h> <br>" + "{{ ti.xcom_pull(task_ids=['creaMensaje']) }}".replace('[','').replace(']',''),
       do_xcom_push=False,
       )
    inicio() >> procesoBeer >> creaMensaje >> envioEmail
dag = beer_dag()
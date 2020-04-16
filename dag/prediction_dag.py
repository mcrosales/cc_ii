from datetime import timedelta 
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['mariocrosl@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval':None

}
#Inicialización del grafo DAG de tareas para el flujo de trabajo
dag = DAG(
    '2do_dag',
    default_args=default_args,
    description='Grafo de prediccion de clima',
    schedule_interval=None,
)


CrearDirectorio = BashOperator(
    task_id='CrearDirectorio',
    depends_on_past=False,
    bash_command='mkdir /tmp/workflow/;mkdir /tmp/workflow/data',
    dag=dag
    )


CapturaDatosHumedad = BashOperator(
    task_id='CapturarDatosHumedad',
    depends_on_past=False,
    bash_command='curl -o /tmp/workflow/humidity_min.csv https://raw.githubusercontent.com/mcrosales/cc_ii/master/data/humidity_min.csv',
    dag=dag
    )

CapturaDatosTemperatura = BashOperator(
    task_id='CapturarTemperatura',
    depends_on_past=False,
    bash_command='curl -o /tmp/workflow/temperature_min.csv https://raw.githubusercontent.com/mcrosales/cc_ii/master/data/temperature_min.csv',
    dag=dag
    )

CapturaMezclaDatos = BashOperator(
    task_id='CapturaMezclaDatos',
    depends_on_past=False,
    bash_command='curl -o /tmp/workflow/merge_data.py https://raw.githubusercontent.com/mcrosales/cc_ii/master/data/merge_data.py',
    dag=dag
    )

MezclarDatos = BashOperator(
    task_id='MezclarDatos',
    depends_on_past=False,
    bash_command='cd /tmp/workflow/; python3 /tmp/workflow/merge_data.py',
    dag=dag
    )


CapturaCodigoFuenteV1=BashOperator(
    task_id='CapV1',
    depends_on_past=False,
    bash_command='cd /tmp/workflow/;git clone --branch flask_microservice https://github.com/mcrosales/cc_ii.git prediction_flask',
    dag=dag
    )

ContenedorBD=BashOperator(
    task_id='ContenedorBD',
    depends_on_past=False,
    bash_command='docker run --name=weather_prediction_db  -d -v /tmp/workflow/data/:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=admin -p 3306:3306 weather_prediction_db:1.0',
    dag=dag
    )


InsertarDatos = BashOperator(
    task_id='InsertarDatos',
    depends_on_past=False,
    bash_command='cp /home/mario/Desktop/cc_ii/p1/insert_data.py /tmp/workflow/;cd /tmp/workflow/; python3 /tmp/workflow/insert_data.py',
    dag=dag
    )

DetenerContenedorBD=BashOperator(
    task_id='DetenerContenedorBD',
    depends_on_past=False,
    bash_command='docker stop weather_prediction_db;docker rm  weather_prediction_db',
    dag=dag
    )

CapturaConfiguracionContenedores = BashOperator(
    task_id='CapturaConfiguracionContenedores',
    depends_on_past=False,
    bash_command='curl -o /tmp/workflow/docker-compose.yml https://raw.githubusercontent.com/mcrosales/cc_ii/master/docker-compose.yml',
    dag=dag
    )

LanzarContenedores = BashOperator(
    task_id='LanzarContenedores',
    depends_on_past=False,
    bash_command='cd /tmp/workflow/; docker-compose up -d',
    dag=dag
    )


CrearDirectorio >> CapturaCodigoFuenteV1 >> [CapturaDatosHumedad,CapturaDatosTemperatura] >> CapturaMezclaDatos >> MezclarDatos >> ContenedorBD >> InsertarDatos >> DetenerContenedorBD >> CapturaConfiguracionContenedores >> LanzarContenedores
 


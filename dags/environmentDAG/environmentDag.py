import logging
import airflow
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule
import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DAG_NAME = 'environment_dag'

default_args = {
    'start_date': datetime.datetime(2017, 1, 1),
    'retries': 0
}

environmentDag = airflow.DAG(DAG_NAME, default_args=default_args, schedule_interval=None)

def process_data_decision(**kwargs):
    conf = kwargs['dag_run'].conf
    environment_type = conf['environment_type']
    if environment_type == 'development':
         return 'file_creation_development'
    elif environment_type == 'production':
            return 'file_creation_production'
    else:
        raise ValueError('Invalid environment_type: {}'.format(environment_type))


def file_creation(**kwargs):
    conf = kwargs['dag_run'].conf
    environment_type = conf['environment_type']
    timestamp = int(time.time()*1000)
    file_name = "civalue_{}_{}.txt".format(environment_type,timestamp)
    ti = kwargs['ti']
    ti.xcom_push(key='file_name', value=file_name)
    with open('{}'.format(file_name), 'w') as f:
        f.write('hello ciValue from {} branch'.format(environment_type))
    return 'file_creation_development'

def print_to_log(**kwargs):
    conf = kwargs['dag_run'].conf
    environment_type = conf['environment_type']
    ti = kwargs['ti']
    file_name = ti.xcom_pull(key='file_name', task_ids='file_creation_{}'.format(environment_type))
    with open('{}'.format(file_name), 'r') as f:
        logger.info(f.read())
    
with environmentDag as dag:
     
    process_data = BranchPythonOperator(
        task_id='process_data',
        provide_context=True,
        python_callable=process_data_decision,
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    file_creation_development = PythonOperator(
        task_id='file_creation_development',
        provide_context=True,
        python_callable=file_creation
    )

    file_creation_production = PythonOperator(
        task_id='file_creation_production',
        provide_context=True,
        python_callable=file_creation
    )

    print_to_console = PythonOperator(
        task_id='print_to_console',
        provide_context=True,
        python_callable=print_to_log,
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    process_data >> [file_creation_development, file_creation_production] >> print_to_console

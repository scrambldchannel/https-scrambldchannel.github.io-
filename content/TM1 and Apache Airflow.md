Title: TM1 and Apache Airflow
Date: 2020-07-23 08:56
Category: tm1
Tags: tm1, python, airflow
slug: airflow-tm1
Authors: Alexander
Summary: Initial takeaways from trying to use Apache Airflow to schedule ETL tasks involving TM1 

I've been enjoying a bit of down time recently which, as well as exploring the lakes of Berlin and Brandenburg, gave me a chance to check out the excellent talks during the [Airflow Summit 2020](https://airflowsummit.org/). They are all still available and I'd recommend them for those interested in learning more about what [Airflow](https://airflow.apache.org/) can do. I've worked with it before but haven't tried to use it with TM1, even though I've felt it might have been useful in some cases. So I decided to create a simple PoC to see how feasible it would be.

### But why? 

I've worked on many projects where TM1 was used to create a dataset (eg a forecast) but that ultimately the data, once finalised, needed to get somewhere else. This can be particularly prevalent in organisations where tools like Tableau are (with good reason) thought to be better options for creating dashboards and visualisations but also just arise from a desire to see their forecast numbers somewhere else, such as their ERP system. Developers not familiar with TM1 often just expect they can easily connect via ODBC or similar only to realise it's not that simple.

I've seen numerous solutions over the years, most end up involving multiple tasks triggered and managed in different tools by different teams. None of the moving parts are particularly complicated but the end to end process can be difficult to debug and it never seems to result in a particularly reusable solution. I felt using Airflow to manage these tasks end to end might avoid some of these issues.

### So what is it?

In their words, "Airflow is a platform created by the community to programmatically author, schedule and monitor workflows". Most commonly, it gets used to orchestrate data pipelines. It was written in Python but can be used to schedule tasks that are written in other languages. It also provides built in "hooks" for connecting to a wide range of third party systems, particularly in the cloud/big data space. This allows you to manage and monitor all of your ETL pipelines in a single place.

The jobs themselves are written in code which means they can be version controlled and tested. The [Airflow docs](https://gtoonstra.github.io/etl-with-airflow/principles.html) lists the principles they try to follow. One thing it doesn't do out of the box is to connect to TM1 but it's easy to extend it with Python which then allows to leverage the power of [TM1py](https://github.com/cubewise-code/tm1py).

### Did it work? 

Yes! At least in the basic use cases I identified:

* Extract the data from a cube view and write this as a csv to an S3 bucket
* Run a TI processes
* Detect whether a value in a cell met a certain condition

### Putting it to the test

Extracting the data from a cube and writing it somewhere was of the most interest to me initially. I chose S3 because of it's widespread use but the same concept could easily be applied to writing to any other system. I was able to create an Airflow DAG that did this pretty easily. To simplify the management of the connection to TM1, I created a library that extends Airflow's base functionality. I've released the resulting code as [airflow-tm1](https://github.com/scrambldchannel/airflow-tm1) on Github and published it to [PyPi](https://pypi.org/project/airflow-tm1/).

*Note* This depends on having a working Airflow environment with support for S3 and airflow_tm1. Read more in [the docs](https://airflow.apache.org/docs/stable/start.html) if you want to get started. 

*Note* this also depends on having connections set up for TM1 and S3. Read more about managing [Airflow connections](https://airflow.apache.org/docs/stable/howto/connection/index.html) for details. The [TM1Hook](https://github.com/scrambldchannel/airflow-tm1/blob/master/airflow_tm1/hooks/tm1.py) requires at least the following to be specified:

* Host
* Login
* Port
* Extras
    * ssl

The trick here is that ```ssl``` needs to defined in the json string in the ```Extras``` field:

```json
{"ssl": false}
```

#### Creating a DAG

Airflow uses DAGs to manage ETL jobs and [the project team](https://airflow.apache.org/docs/stable/concepts.html#core-ideas) are much better at explaining what they are than I am. In short, a DAG can be thought of a list of tasks defined together in a Python script. The fundamental components of a DAG are hooks, which manage connections to other systems; operators, which complete an independent task; and sensors, which check whether a condition is true.

Here is the simple DAG I created to pull data from a cube and write it to S3. It uses the TM1Hook from airflow-tm1 to manage the connection to TM1py and transfers the data using a Python operator that leverages TM1py. I created it with the name

##### Import the necessary libraries

You can use this import any other modules you want to use in your DAGs.

```python
from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago, timedelta

from airflow_tm1.hooks.tm1 import TM1Hook
```

##### Set defaults

These can be overwritten on a task by task basis. 

```python
# set defaults that DAG will pass to each task
default_args = {
    "owner": "Airflow",
    "start_date": days_ago(2),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "you@somewhere.com",
    "retries": 1
}
```

##### Define the Python function the task will use

This gets run by our task in the DAG and manages the end to end transfer of the data from TM1 to S3.


```python
def cube_view_to_s3(cube, view, bucket, key, **kwargs):

    # instantiate our TM1Hook using the "tm1_default" connection
    tm1_hook = TM1Hook(tm1_conn_id="tm1_default")
    # return an instance of the TM1Service from TM1py
    tm1 = tm1_hook.get_conn()

    # pull data in csv format from specified cube view
    view_data = tm1.cubes.cells.execute_view_csv(
        cube_name=cube, view_name=view, private=False)

    # instantiate S3Hook using the "s3_default" connection
    s3_hook = S3Hook(aws_conn_id="s3_default")
    # write the data to a key in the bucket specified
    s3_hook.load_string(string_data=view_data, key=key,
        bucket_name=bucket, replace=True)
```

##### Create the DAG and a single task

This DAG only has a single task ```t1``` but will usually contain several more and manage how they depend on one another.

```python
with DAG(dag_id="example_tm1_to_s3", schedule_interval="@daily", default_args=default_args) as dag:

    t1 = PythonOperator(
        task_id="view_to_S3",
        # specifies the function we want to call
        python_callable=cube_view_to_s3,
        # and the arguments to pass it
        op_kwargs={"cube": "Income Statement Reporting", "view": "Income Statement - Management",
            "key": 'airflow-test/{{ ds_nodash }}.csv', "bucket": "scrambldbucket"},
        dag=dag,
    )

    t1
```

##### Running the DAG

DAGS need to be saved in Airflow's DAG folder as ```*.py``` files. Airflow has a built in [web UI](https://airflow.apache.org/docs/stable/ui.html) that can manage DAGs. They can also be managed from a [cli](https://airflow.apache.org/docs/stable/usage-cli.html) which can be useful for testing purposes.

```sh
airflow trigger_dag example_tm1_to_s3
```

##### Results

I tested on small views, running both TM1 and Airflow locally with an OK internet connection. I was able to transfer small datasets (<10mb) relatively quickly but I've not done any serious testing and, obviously, scalability would be a concern. For pulling large volumes of data, a good understanding of TM1, and the model itself, would be required to develop a sensible strategy. That said, it should work for in some cases such as where summary data is required for a Tableau dashboard. Additionally, I'd expect exporting cube data via TI first would prove faster in many cases. 

#### Custom Operators

The DAG above uses the ```PythonOperator``` to call a custom function. For tasks that are likely to be used repeatedly, it's possible to create custom operators than can provide a useful abstraction to tasks. There's no reason one couldn't create a custom operator that would replicate the function I used above, but I thought I'd start with something simpler. I created custom operators to trigger TI processes and Chores. 

##### A DAG using a Custom Operator

Using the [TM1RunTIOperator](https://github.com/scrambldchannel/airflow-tm1/blob/master/airflow_tm1/operators/tm1_run_ti.py) the task can be written in just a few lines of code specifying the process to run and their parameters. This specific task triggers a feeders refresh in a specific cube but could be used to run anything best handled by TI.

```python
from airflow import DAG
from airflow.utils.dates import days_ago, timedelta

from airflow_tm1.operators.tm1_run_ti import TM1RunTIOperator

default_args = {
    "owner": "Airflow",
    "start_date": days_ago(2),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "you@somewhere.com",
    "retries": 1
}

with DAG(dag_id="example_run_ti", default_args=default_args, schedule_interval="@daily") as dag:

    t1 = TM1RunTIOperator(
        task_id="run_ti",
        process_name="Refresh Feeders",
        parameters={"pCube": "Capital"},
        dag=dag,
    )

    t1
```

#### Custom Sensors

Sensors are used to control flow in a DAG. In this DAG, an instance of the [TM1CellValueSensor](https://github.com/scrambldchannel/airflow-tm1/blob/fef460219bca80203119dd794716ddef8e58fe20/airflow_tm1/sensors/tm1_cell_value.py#L10) checks that a value in a 


##### A DAG using a Custom Operator

```python
from operator import eq, ge, gt, le, lt, ne

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago, timedelta

from airflow_tm1.sensors.tm1_cell_value import TM1CellValueSensor

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(2),
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(dag_id="example_value_sensor", default_args=default_args) as dag:

    t1 = TM1CellValueSensor(
        task_id='check_value',
        # check every 15 minutes
        poke_interval=60 * 15,
        # timeout in 12 hours
        timeout=60 * 60 * 12,
        tm1_conn_id="tm1_default",
        cube="Task Workflow",
        value=1,
        elements="OPEX,Total Company,Complete",
        # apply the greater than operator
        op=gt,
    )

    t2 = DummyOperator(task_id='do_nothing')

    t1 >> t2

```
Title: TM1 and Apache Airflow
Date: 2020-07-23 08:56
Category: tm1
Tags: tm1, python, airflow
slug: airflow-tm1
Authors: Alexander
Summary: Initial takeaways from trying to use Apache Airflow to schedule ETL tasks involving TM1 

I've been enjoying a bit of down time recently which, as well as exploring the lakes of Berlin and Brandenburg, gave me a chance to check out the excellent talks during the [Airflow Summit 2020](https://airflowsummit.org/). They are all still available and I'd recommend checking them out for those interested in learning more. I've worked with Airflow before but never tried to use it with TM1 up until now, even though I've felt it might be useful in some cases. So I thought I'd try to create a simple PoC for a project I was working on.

### But why? 

I've worked on many projects in the past where TM1 was used to create a dataset (i.e. a forecast) but that ultimately the data needed to get somewhere else. This can be particularly prevalent in organisations where tools like Tableau and Power BI are (understandably) thought to be better options for creating dashboards and visualisations. Developers not familiar with TM1 often just expect they can easily connect via ODBC or similar only to realise it's not that simple. I've seen numerous solutions to this problem, ("The Good, the Bad and the Ugly" springs to mind, given Ennio Morricone's recent passing), people love re-inventing the wheel. I am no different but I did genuinely feel that for organisations already using Airflow, this might be an interesting option.

### So what is it?

In [their words](https://airflow.apache.org/), "Airflow is a platform created by the community to programmatically author, schedule and monitor workflows". Most commonly, it gets used to orchestrate data pipelines. It is written in Python but can be used to schedule all sorts of tasks. It also provides built in "hooks" for connecting to a wide range of third party systems, particularly in the cloud/big data space. One thing it doesn't do out of the box is to connect to TM1 but it's pretty easy to extend it with Python which then allows to leverage the power of TM1py.

### Did it work? 

Yes! At least in the limited use cases I was targeting. I set out to achieve the following as a minimum:

* Extract the data from a cube view and write this as a csv to an S3 bucket
* Trigger a TI processes
* Create a sensor to detect whether an element existed in a dimension

Extracting the data from a cube and writing it somewhere was of the most interest to me initially. I chose S3 because of it's widespread use but the same concept could easily be applied to writing to any other system. My first iteration just used the PythonOperator and PythonSensor classes but I thought it would be cleaner to create my own custom hook, operators and sensors. Having spent a bit of time looking at the Airflow codebase, I found this surprisingly easy. I've released the resulting code as [airflow-tm1](https://github.com/scrambldchannel/airflow-tm1) on Github and published it to [PyPi](https://pypi.org/project/airflow-tm1/). I've only tested it on a fairly narrow set of use cases but it does what I need it to do, maybe someone out there will find it useful.


### Overview of the airflow-tm1 package

#### Installation

Via pip:

```sh
pip install airflow-tm1
```

Note that it depends on Airflow so will bring in a pretty hefty list of dependencies if you're not installing it in an existing Airflow environment. In this case, you probably want to go back and start at [the beginning](https://airflow.apache.org/docs/stable/start.html).

#### Usage

As of today, the library provides a hook, a couple of operators to run TI processes and chores and a couple of sensors to detect whether or not an element exists in a dimension or the value in a given cell meets a given criteria. The advantage of using the hook is that it allows you to store your connection information (ip address, username, password etc) in Airflow's connections rather than embedding it in the code of your DAG. Once initialiased and the connection established, the hook gives you access to an instance of [TM1py's](https://github.com/cubewise-code/tm1py) TM1Service object from which you can do pretty much anything you want.

##### Using the Hook

Simply import the hook object:

```python
from airflow_tm1.hooks.tm1 import TM1Hook
```

Then, within you code, instantiate it and create the connection (note this depends on the existence of an Airflow connection named "tm1_default"):

```python
tm1_hook = TM1Hook(tm1_conn_id="tm1_default")
tm1 = tm1_hook.get_conn()
```

From then on, you'll be able to access all the methods and properties of the [TM1Service object](https://github.com/cubewise-code/tm1py/blob/master/TM1py/Services/TM1Service.py). I've used this approach to build several DAGs that accomplish tasks such as:


Moving data to and from S3 just happened to be what I needed to achieve but there is no reason you couldn't use this to orchestrate pulling data out of TM1 and pushing it to any sort of data(base/warehouse/lake).

##### Using the Operators

I'm in two minds about how useful custom operators actually are in a TM1 context. I did toy with the idea of writing one to pull data from a named cube view and write it to S3 but felt this was so specific given how different every TM1 model is. In the end I felt it was probably more useful to use the TM1Hook while taking advantage of the flexibility of a PythonOperator. I did build a couple of operators for triggering TIs and Chores though as this seemed quite a generic requirement. The idea is that rather than triggering these via the hook directly, they can be run in a uniform way with consistent exception handling and logging when wrapped up as a custom operator.

For example, you could create a task in your DAG such as the following which triggers a TI process "Refresh Feeders" with a parameter specifying the cube name:

```python
task_run_ti = TM1RunTIOperator(
    task_id="refresh_feeders_of_gl_cube",
    process_name="Refresh Feeders",
    parameters =  { "pCube" : "GL"},
    dag=dag,
)

```

I can see this also being as useful for data exports where writing a large set of data to a file via TI will likely be much more performant than trying to pull the same through the REST API. It would be interesting to do some benchmarking though. One could create a task that triggers the process, one that checks that the file has been written and one that then loads it into the desired destination. I've worked on implementations where these same three steps (or similar) were run but no one team had end to end visibility of the process. Doing it in Airflow would give you that transparency and debugging a lot easier.


##### Using the Sensors

I can see the usefulness of custom sensors a bit more clearly. For example, the TM1ElementSensor as used below will wake up every 30 minutes and check for the existence of a specific element in a dimension. I thought this might be useful in situations where a new version of a forecast was created and this would signal that a new dataset should be exported. 

```python
task_element_sensor = TM1ElementSensor(
            task_id='tm1_element_sensor_task',
            poke_interval=60 * 30, # (seconds); checking file every half an hour
            timeout=60 * 60 * 12, # timeout in 12 hours
            tm1_conn_id = "tm1_default",
            element="my new version",
            dimension="Version",
            dag=dag)
```

The value sensor can be used to check that the value of a specific cell meets a criteria. For example, the task below would check every fifteen minutes to see if the sale figure for a given year was greater than zero. This might imply that the new sales rolling forecast for 2021 was available and that it should be extracted to then be loaded downstream. 

```python
task_value_sensor = TM1CellValueSensor(
            task_id='tm1_value_sensor_task',
            poke_interval=60 * 15, # check every 15 minutes 
            timeout=60 * 60 * 12, # timeout in 12 hours
            tm1_conn_id = "tm1_default",
            cube="GL",
            value = 0,
            elements="RF,2021,Sales,Amount",
            op=gt, 
            dag=dag)
```

#### Next Steps

I don't have a live project that is using this currently but I would like to extend it a bit further and think about a few more use cases. I aim to add a few example DAGS to Github soon and flesh out the documentation generally. I also need to think more about the best approach for exception handling and logging.  
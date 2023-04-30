# AirflowTask

The workflow (DAG) creates a file according to a user parameter and print it to the console


**Prerequisites**


You should have the following :

1- Python >=3.7.


2- Python IDE.


3- Docker Engine.


4- REST API tool.


**To run this project follow these instructions:**

1- Git all the app files to a directory in your system.


2- Open this directory in terminal.


3- Run the project in docker-compose with this command :

    `docker-compose up`
    
4- Navigate to this url in your browser:
   </br>
http://localhost:8080/

5- Use your REST API tool to send POST request :
</br>
  `{
  "conf" : {"environment_type" : "production"}
    }`

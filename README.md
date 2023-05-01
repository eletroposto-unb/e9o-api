# Eletrogama Service

Microservices to Eletrogama project

## Requirements

- A mysql instance running
- At least python in version 3.8
- pip installed

## How to run

For each service, the instructions to run all are the same. First of all, with pip run the folowing command to install requirements:

```shell
pip install -r requirements.txt
```

After that, to run the service you need to run the following command:
```shell
uvicorn <service_folder>.main:<service_name> --reload --port 8081 --host 0.0.0.0
```

- --reload: Means the service will reload everytime any file changes.
- --host 0.0.0.0: Allow requests from any ip address
- --port 8081: Get the port number 8081
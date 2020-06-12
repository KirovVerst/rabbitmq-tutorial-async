# rabbitmq-tutorial-async
![Github CI](https://github.com/KirovVerst/rabbitmq-tutorial-async/workflows/Github%20CI/badge.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

RabbitMQ [tutorials](https://www.rabbitmq.com/getstarted.html) on Python with [aio-pika](https://github.com/mosquito/aio-pika)

## Development
### Run RabbitMQ
```bash
$ docker-compose up -d
```

### Install requirements
Python 3.8 is required.
```bash
$(venv) pip install -r requirements.txt
```

### Run static checks
```bash
$(venv) pip install -r requirements-test.txt
$(venv) pre-commit run --all-files
```

## Licensing
The code in this project is licensed under MIT license.

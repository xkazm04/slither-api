## Setup

1. [Create virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

2. [Activate virual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)

3. Install packages

```bash
pip3 install -r requirements.txt
```

## Slither scanner endpoint

### POST /scanner

Request body

1. sol_contract - string
2. pragma - string

## Run server

```bash
uvicorn main:app --reload
```

## Run in container (Docker)

```bash
docker-compose up --build -d
```

Now your app is running on `http://localhost:8000`

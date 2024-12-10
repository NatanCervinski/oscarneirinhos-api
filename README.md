##  Como rodar com Docker
 ### Subindo o Ambiente 
 1. Na raiz do projeto, execute: 
 2. ```bash
	  docker-compose up --build
	 ```

## Como rodar com localmente com uv
```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```
ou
```
$ wget -qO- https://astral.sh/uv/install.sh | sh
```

e logo após
```
$ uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em http://localhost:8000.

👍
(eu acho)

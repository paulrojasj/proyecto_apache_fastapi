# Proyecto: Apache como Proxy Inverso para FastAPI

Este proyecto configura un sistema donde Apache actúa como un proxy inverso para un backend FastAPI, todo orquestado mediante Docker Compose. El objetivo es que las solicitudes a `http://localhost/api/data` sean redirigidas al backend FastAPI y devuelvan una respuesta JSON.

## Estructura del Proyecto

```
proyecto_apache_fastapi/
├── app/
│   ├── main.py
│   └── __pycache__/
├── apache/
│   ├── Dockerfile
│   └── fastapi.conf
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Tecnologías Involucradas

- **FastAPI**: Framework de Python para construir APIs rápidas y modernas.
- **Apache HTTP Server**: Servidor web que actúa como proxy inverso.
- **Docker**: Contenedores que aíslan cada servicio.
- **Docker Compose**: Orquestación de múltiples contenedores.

## Configuración del Proyecto

### 1. FastAPI

El backend FastAPI maneja solicitudes HTTP y devuelve respuestas JSON.

Archivo `app/main.py`:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
def get_data():
    return {"message": "Hola, tus datos están protegidos!"}
```

Archivo `requirements.txt`:
```
fastapi
uvicorn
```

Dockerfile para FastAPI:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### 2. Apache como Proxy Inverso

Archivo `apache/fastapi.conf`:
```apache
<VirtualHost *:80>
    ServerName localhost

    ProxyPreserveHost On

    ProxyPassMatch ^/api/(.*)$ http://fastapi:5000/$1
    ProxyPassReverse /api/ http://fastapi:5000/
</VirtualHost>
```

Dockerfile para Apache:
```dockerfile
FROM httpd:2.4

# Habilita los módulos de proxy
RUN sed -i 's/#LoadModule proxy_module/LoadModule proxy_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule proxy_http_module/LoadModule proxy_http_module/' /usr/local/apache2/conf/httpd.conf

# Copia la configuración de proxy
COPY fastapi.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf

# Incluye el archivo de virtual hosts
RUN sed -i 's|#Include conf/extra/httpd-vhosts.conf|Include conf/extra/httpd-vhosts.conf|' /usr/local/apache2/conf/httpd.conf
```

### 3. Docker Compose

Archivo `docker-compose.yml`:
```yaml
version: "3.8"

services:
  fastapi:
    build: .
    container_name: fastapi_app
    ports:
      - "5000:5000"
    networks:
      - app-network

  apache:
    build: ./apache
    container_name: apache_proxy
    ports:
      - "80:80"
    depends_on:
      - fastapi
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## Cómo Ejecutar el Proyecto

1. Construye y levanta los servicios:
   ```bash
   docker-compose up --build
   ```

2. Accede a FastAPI directamente:
   - [http://localhost:5000/data](http://localhost:5000/data)

3. Accede a través de Apache:
   - [http://localhost/api/data](http://localhost/api/data)

## Flujo de una Solicitud

1. El navegador envía una solicitud a `http://localhost/api/data`.
2. Apache recibe la solicitud y la reenvía a `http://fastapi:5000/data`.
3. FastAPI responde con un mensaje JSON.
4. Apache devuelve la respuesta al navegador.

## Buenas Prácticas Aplicadas

- **Separación de responsabilidades**: FastAPI maneja la lógica del backend, Apache actúa como proxy.
- **Uso de Docker Compose**: Facilita la orquestación y asegura que los servicios estén aislados.
- **Configuración explícita**: Los Dockerfiles y archivos de configuración son claros y reproducibles.

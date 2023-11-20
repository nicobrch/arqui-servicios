# Arquitectura de Software

## Env

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=arquisw
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
HIDE_EMPTY_PASSWORD=yes
```

## Ejecutar

```shell
docker compose build
docker compose up -d
```

Borrar volumen cuando termina

```shell
docker compose down -v
```
# Arquitectura de Software

## Ejecutar

```shell
docker compose build
docker compose up
```

Para botarlo

```shell
docker compose down
```

#### Iniciar BUS

```bash
docker run -d -p 5000:5000 jrgiadach/soabus:v1
```

#### Iniciar BDD

```bash
cd ./db
docker compose build
docker compose up -d
```
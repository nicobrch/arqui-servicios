# Arquitectura de Software

## Iniciar BUS

```bash
docker run -d -p 5000:5000 jrgiadach/soabus:v1
```

## Iniciar BDD

```bash
cd ./db
docker compose build
docker compose up -d
```
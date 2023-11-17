# Usa la imagen oficial de PostgreSQL como base
FROM postgres:16.1

# Configura las variables de entorno para la creación de la base de datos
ENV POSTGRES_DB arquisw
ENV POSTGRES_USER root
ENV POSTGRES_PASSWORD root

# Copia el archivo init.sql al directorio de Docker
COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
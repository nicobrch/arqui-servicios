# Usar una imagen base de Python en Alpine
FROM python:3.8-alpine

# Establecer el directorio de trabajo
WORKDIR /Escritorio/arqui-servicios-main/servicios

# Copiar los scripts de Python al contenedor
COPY . .

# Comando para ejecutar los scripts (modificar según sea necesario)
CMD ["python", "db_connect.py"]

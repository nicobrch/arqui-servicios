# Arquitectura de Software

Este repositorio contiene el proyecto de Arquitectura de Software de 2023, donde se realizó un sistema el cuál 
gestiona los horarios de los trabajadores de una empresa utilizando el modelo Software Oriented Architecture (SOA).

Para la realización se este proyecto, se tiene un cliente el cuál permite el inicio de sesión de los usuarios, y una 
vez autenticados poseen distintas funciones. El cliente envía información al bus de datos, el cuál se encarga de 
redireccionar los datos a los servicios indicados. El funcionamiento de este proyecto se ilustra mediante el 
siguiente diagrama:

![Diagrama](/img/diagrama.png "Diagrama")

De este diagrama se tiene que:

* El supercliente se encarga de instanciar los clientes necesarios.
* Los clientes se comunican mediante el bus de datos con los servicios.
* Tanto el bus, como los servicios y la base de datos estan dentro de containers de docker.
* Para acceder a la base de datos, se debe hacer mediante el servicio de BDD.

## Ejecutar proyecto

Dentro de la carpeta principal del proyecto, ejecutar los siguientes comandos:

```shell
docker compose build
docker compose up
```

Esto levantará el bus de datos, la base de datos y los servicios.

Además, se requiere crear un archivo .env el cuál se encargará de tener las credenciales del proyecto, para probar 
puede usar el siguiente archivo de ejemplo:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=arquisw
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
HIDE_EMPTY_PASSWORD=yes
SOABUS_HOST=localhost
```

## Comentarios

El proyecto es grande y extenso, pero es de fácil comprensión y uso. Para comunicar los clientes y servicios, se 
utilizó un formato JSON, lo cuál fue lo más complicado de implementar. Para poder crear algún servicio nuevo, 
basarse en el archivo [User Management](/servicios/user_management.py). Este es el ejemplo más claro y completo para 
guiarse.
# Data Engineering
Repositorio de entregables del curso Data Engineering comision 55990

## Componentes
- **config.ini:** archivo de configuración con datos de conexión a redshift.
- **conect.py:** script que lee config.ini e inicia la conexión hacia la DB.
- **main.py:** script de ejecución principal.
- **tabla_cerveza.sql:** script sql para la creación de la tabla en el esquema **marcocalle86_coderhouse**.
- **Dockerfile:** script para la creación de la imagen docker que se utilizará para crear contenedores.
- **beer_dag:** script para la ejecución de la aplicacion contenerizada desde airflow.

Avance del proyecto
---
Entregable - 1
---
Se crean los script de conexión a la DB data-engineer-database y obtencion de datos a partir de la API https://random-data-api.com/api/v2/beers la cual devuelve un registro el cual contiene una variedad de cerveza artesanal y sus datos técnicos.  
Los datos de porcentaje, IBU y Blg se transforman a números para poder insertarlos en la tabla y que puedan ser utilizados con funciones.  

Entregable - 2
---
Para la verificación de datos duplicados que provienen de la API se utiliza el metodo **drop_duplicates()** y se vuelca el resultado en **p0** para luego hacer la conversion de datos string a tipo integer (campo ibu) o float (campos alcohol y blg), como funcion adicional se renombran los nombres de los campos que estan en inglés para que concuerden con los que estan definidos en español en la tabla **cerveza**.  

El poblado de la tabla **cerveza** se realiza en 2 pasos:
- Volcado de datos con el método **to_sql()** en la que se define la tabla **staging** con parametro **if_exists='replace'** para que se sobreescriba en cada ejecución y solo contenga los datos de la ultima ejecución.  
- Ejecución de **DELETE** para borrar los registros duplicados entre la tabla **cerveza** y **staging**.  
- Insersión de datos únicos de la tabla **staging** sobre la tabla **cerveza**.  



#### Mejoras del proyecto en Entregable 2
Se modifica la tabla para agregar PRIMARY KEY para el campo **id** y SORTKEY en los campos **marca** y **estilo**, los cambios quedan asentados en el script tabla_cerveza.sql.  
En el script main.py se define la variable **convertir** para obtener los datos directamente de la API y la variable **convertir2** tiene datos duplicados para pruebas.  
Se crear el archivo **requirements.txt** con las librerias utilizadas y sus versiones, pip resuelve las dependencias.

Entregable - 3  
---
La aplicación contenerizada utiliza python:3.10-slim como imagen base por ser más estable y ocupar menos espacio en disco que si se utilizara una imagen basada en alpine.  
Se agrega la carpeta airflow (version airflow:2.7.2) que contiene docker-compose.yaml descargado del sitio oficial de airflow en la cual se modificaron las variables **AIRFLOW__API__AUTH_BACKENDS** y **AIRFLOW__CORE__ENABLE_XCOM_PICKLING** además de agregar los volumenes **'/var/run/docker.sock:/var/run/docker.sock'** y **'/tmp:/tmp'** que permiten utilizar el docker engine del host.  
En el archivo **.env** se agrega la instalacion de **apache-airflow-providers-docker** para poder utilizar DockeerOperator además de la utilización de un usuario del host con UID 1000 para la correcta ejecución de airflow.  
En la carpeta dag se encuentra **beer_dag.py** que contiene los pasos de ejecución de la aplicación contenerizada utilizando decoradores task y dag además de DockerOperator, el proceso se programa para ejecución diaria a partir del 1/11/2023. En el dag se agregan lso comentarios de cada componente utilizado

~~~
#### Proceso de ejecución
El siguiente procedimiento se realizó en Ubuntu Server 22.04.3 y Debian 12 instalados en Virtual Box.  
1- Situarse en la carpeta raiz del proyecto y ejecutar **docker build -t beer .** para crear la imagen **beer:latest**  
2- Ejecutar el siguiente comando con permisos de super usuario: **chmod 666 /var/run/docker.sock**, este cambio de permisos permite la utilización de docker engine desde el contenedor de airflow. **Este paso se debe realizar cada vez que se reinicia el host.**  
La ubicación de **docker.sock** puede diferir si se cambia en docker.conf o si se esta utilizando Docker Desktop.  
3- Ubicarse en la carpeta airflow y ejecutar **docker compose up** para que se generen los contenedores de airflow.  
4- Acceder a airflow desde un browser y verificar que aparezca **beer_dag**, realizar una ejecución para comprobar el funcionamiento.  
5- Ejecutar **docker compose down** para eliminar todos los contenedores de airflow.  
~~~

#### Mejoras del proyecto en Entregable 3
Se modifica el script tabla_cerveza.sql, incluye IF EXISTS para verificar si la tabla existe previamente.  
Se hace la definición de los campos de la tabla staging desde to_sql para que concuerde con la tabla cerveza. Durante la pruebas en la tabla staging se recibieron datos con una longitud superior a la esperada.  
Se mejora la detección de duplicados entre la tabla staging y la tabla cerveza utilizando LEFT JOIN y realizando un DROP TABLE de staging para liberar espacio.  


Entregable - 4
---

1- Para evitar que el uso de credenciales en el codigo, se pasan por variable de entorno el nombre de la base de datos, esquema, credenciales, puerto y cantidad de registros que se quieran obtener desde la API (la variable para este fin, SIZER, esta seteada para obtener 4 registros).

2- Se modifica el script main.py para agregar codigos de ejecución que serán utilizados para generar mensajes siguiente detalle:  
'0': "Proceso Finalizado correctamente"  
'1': "Error al obtener datos de la API"  
'2': "Error de conexión con la DB en Redshift"  
'3': "Error de volcado de datos en tabla staging"  
'4': "Error durante la inserción de datos en tabla cerveza"  
'5': "Error durante el borrado de tabla staging"  

3- Se modifica el DAG beer_dag.py:
 - Se configuran las variables de entorno que utilizará la aplicacion contenerizada desde DockerOperator y se pasa el codigo de ejecución, se utiliza la imagen beer_env.
 - Desde PythonOperator se ejecuta la función _email() para procesar los codigos de ejecución para que envie DockerOperator y el resultado pasa a la siguiente tarea por xcom
 - EmailOperator se hace el envio de email con el mensaje generado en la terea anterior, se puede cambiar el destinatario. Ver archivo emailPruebaDAG.PNG que tien  los email de prueba enviados desde el proyecto. 


~~~
#### Proceso de ejecución
El siguiente procedimiento se realizó en Ubuntu Server 22.04.3 y Debian 12 instalados en Virtual Box.  
1- Situarse en la carpeta raiz del proyecto y ejecutar **docker build -t beer_env .** para crear la imagen **beer_env:latest**  
2- Ejecutar el siguiente comando con permisos de super usuario: **sudo chmod 666 /var/run/docker.sock**, este cambio de permisos permite la utilización de docker engine desde el contenedor de airflow. **Este paso se debe realizar cada vez que se reinicia el host.**  
La ubicación de **docker.sock** puede diferir si se cambia en docker.conf o si se esta utilizando Docker Desktop. Se agrega el script bash contenedorbeer.sh para poder hacer una prueba de ejecución de la aplicacion contenerizada cambiando usuario y contraseña.
3- Ubicarse en la carpeta airflow y ejecutar **docker compose up** para que se generen los contenedores de airflow y lla instalación de dependencias.  
4- Acceder a airflow desde un browser y verificar que aparezca **beer_dag**, realizar una ejecución para comprobar el funcionamiento.  (ver imagen beer_dag_en_airflow.PNG)
5- Ejecutar **docker compose down --volumes --remove-orphans** para eliminar todos los contenedores de airflow y volumenes creados para su funcionamiento.  
~~~

#### Mejoras del proyecto en Entregable 4

- Se agregan variables de entorno para configurar el SMTP y zona horaria sin necesidad de modificar airflow.cfg:
AIRFLOW__SMTP__SMTP_HOST: 'smtp.gmail.com'  
AIRFLOW__SMTP__SMTP_USER: 'email@gmail.com'  
AIRFLOW__SMTP__SMTP_PASSWORD: 'contraseña'  
AIRFLOW__SMTP__SMTP_PORT: 587  
AIRFLOW__SMTP__SMTP_MAIL_FROM: 'Monitoreo Proceso Beer'  

AIRFLOW__CORE__DEFAULT_TIMEZONE: 'America/Argentina/Buenos_Aires'  

- Se crea nueva imagen airflow a partir de un Dockerfile que instala las librerias para poder utilizar DockerOperator y cambio de zona horaria desde el DAG, en requirements.txt se encuentran las dependencias.
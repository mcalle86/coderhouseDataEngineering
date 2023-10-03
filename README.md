# Data Engineering
Repositorio de entregables del curso Data Engineering comision 55990

## Componentes
- **config.ini:** archivo de configuración con datos de conexión a redshift.
- **conexion.py:** script que lee config.ini e inicia la conexión hacia la DB.
- **main.py:** script de ejecución principal.
- **tabla_cerveza.sql:** script sql para la creación de la tabla en el esquema **marcocalle86_coderhouse**.

## Avance del proyecto
### Entregable - 1
Se crean los script de conexión a la DB data-engineer-database y obtencion de datos a partir de la API https://random-data-api.com/api/v2/beers la cual devuelve un registro el cual contiene una variedad de cerveza artesanal y sus datos técnicos.

Los datos de porcentaje, IBU y Blg se transforman a números para poder insertarlos en la tabla y que puedan ser utilizados con funciones.

### Entregable - 2
Para la verificación de datos duplicados que provienen de la API se utiliza el metodo **drop_duplicates()** y se vuelca el resultado en **p0** para luego hacer la conversion de datos string a tipo integer (campo ibu) o float (campos alcohol y blg), como funcion adicional se renombran los nombres de los campos que estan en inglés para que concuerden con los que estan definidos en español en la tabla **cerveza**

El poblado de la tabla **cerveza** se realiza en 2 pasos:
- Volcado de datos con el método **to_sql()** en la que se define la tabla **staging** con parametro **if_exists='replace'** para que se sobreescriba en cada ejecución y solo contenga los datos de la ultima ejecución.
- Ejecución de **DELETE** para borrar los registros duplicados entre la tabla **cerveza** y **staging**
- Insersión de datos únicos de la tabla **staging** sobre la tabla **cerveza**



#### Mejoras del proyecto
Se modifica la tabla para agregar PRIMARY KEY para el campo **id** y SORTKEY en los campos **marca** y **estilo**, los cambios quedan asentados en el script tabla_cerveza.sql.

En el script main.py se define la variable **convertir** para obtener los datos directamente de la API y la variable **convertir2** tiene datos duplicados para pruebas.


Se crear el archivo **requirements.txt** con las librerias utilizadas y sus versiones, pip resuelve las dependencias.


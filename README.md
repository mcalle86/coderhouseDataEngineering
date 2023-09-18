# Data Engineering
Repositorio de entregables del curso Data Engineering comision 55990

## Componentes
- **config.ini:** archivo de configuración con datos de conexión a redshift.
- **conexion.py:** script que lee config.ini e inicia la conexión hacia la DB.
- **main.py:** script de ejecución principal.
- **tabla_cerveza.sql:** script sql para la creación de la tabla en el esquema **marcocalle86_coderhouse**.

## Avance del proyecto
Se crean los script de conexión a la DB data-engineer-database y obtencion de datos a partir de la API https://random-data-api.com/api/v2/beers la cual devuelve un registro el cual contiene una variedad de cerveza artesanal y sus datos técnicos.
Los datos de porcentaje, IBU y Blg se transforman a números para poder insertarlos en la tabla y que puedan ser utilizados con funciones.

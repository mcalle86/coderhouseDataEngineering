import os
from sqlalchemy import create_engine

def connRedshiftAlchemy():
    #leer configuración
    config = {'servidor': os.environ.get("SERVIDOR_REDSHIFT"),
            'db': os.environ.get("DB_REDSHIFT"),
            'puerto': os.environ.get("PUERTO_REDSHIFT"),
            'usuario': os.environ.get("USUARIO_REDSHIFT"),
            'clave': os.environ.get("CLAVE_REDSHIFT")}
    try:
        conn = create_engine( f"""redshift+psycopg2://{config['usuario']}:{config['clave']}@{config['servidor']}:{config['puerto']}/{config['db']}""")
        return conn
    except Exception as e:
        raise Exception(e)

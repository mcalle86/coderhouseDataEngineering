import configparser
from sqlalchemy import create_engine

def leerConfiguracion():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return {'servidor': config['REDSHIFT']['servidor'],
            'db': config['REDSHIFT']['db'],
            'puerto': config['REDSHIFT']['puerto'],
            'usuario': config['REDSHIFT']['usuario'],
            'clave': config['REDSHIFT']['clave']}

# def conexionRedshift():
#     #leer configuración
#     config = leerConfiguracion()
#     try:
#         conn = redshift_connector.connect(
#             host = config['servidor'],
#             database = config['db'],
#             port = config['puerto'],
#             user = config['usuario'],
#             password = config['clave'])
#         #print(type(conn))
#         return conn
#     except Exception as e:
#         raise Exception(e)

def connRedshiftAlchemy():
    #leer configuración
    config = leerConfiguracion()
    try:
        conn = create_engine( f"""redshift+psycopg2://{config['usuario']}:{config['clave']}@{config['servidor']}:{config['puerto']}/{config['db']}""")
        return conn
    except Exception as e:
        raise Exception(e)

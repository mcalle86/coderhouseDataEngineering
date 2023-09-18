import redshift_connector
import configparser



def conexionRedshift():
    #leer configuración
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        conn = redshift_connector.connect(
            host = config['REDSHIFT']['servidor'],
            database = config['REDSHIFT']['db'],
            port = config['REDSHIFT']['puerto'],
            user = config['REDSHIFT']['usuario'],
            password = config['REDSHIFT']['clave'])
        print(type(conn))
        return conn
    except Exception as e:
        raise Exception(e)

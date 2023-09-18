import conect,requests



def insertData(lista):
    try:
        conexion = conect.conexionRedshift()
        cursor = conexion.cursor()
        query = """INSERT INTO marcocalle86_coderhouse.cerveza () 
        VALUES (?,?,?,?,?,?,?,?,?,?)"""
        cursor.execute(query,lista)
        conexion.commit()
        cursor.close
    except Exception as e:
        print(e)
    finally:
        conexion.close()
    
#funcion para obtener registros de tipos de cerveza que se comercializan y sus caracteristicas
def getbeer():
    url = "https://random-data-api.com/api/v2/beers"
    payload = {'size': 1}
    headers = {"Content-Type":"application/json"}
    response = requests.request("GET", url, headers=headers, params=payload)
    registros = response.json()
    return registros

#muestra de datos obtenidos y que luego serán insertados
convertir = getbeer()
print('id ', convertir['id'])
print('marca ',convertir['brand'])
print('nombre: ',convertir['name'])
print('estilo: ',convertir['style'])
print('lupulo: ',convertir['hop'])
print('levadura: ',convertir['yeast'])
print('malta: ',convertir['malts'])
print('amargor: ',int(str(convertir['ibu']).replace(' IBU','')))
print('alcohol (%): ', float(str(convertir['alcohol']).replace('%','')))
print('balling(blg)',float(str(convertir['blg']).replace('°Blg','')))

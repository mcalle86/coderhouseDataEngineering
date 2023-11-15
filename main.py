import conect,requests,sqlalchemy,os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

#funcion para obtener registros de tipos de cerveza que se comercializan y sus caracteristicas
#Se setea payload = {'size': 4} para recibir 4 registros de la API
def getbeer():
    url = "https://random-data-api.com/api/v2/beers"
    payload = {'size': os.environ.get("SIZER")}
    headers = {"Content-Type":"application/json"}
    response = requests.request("GET", url, headers=headers, params=payload)
    registros = response.json()
    #print(registros)
    return registros

def procesarDatos():

    #Obtener datos desde la API
    convertir = getbeer()

    # Datos de muestra para forzar datos duplicados que provienen desde la API y datos que podrían
    # existir en la tabla de redshift
    convertir2 = [{'id': 6463, 'uid': '21f519ad-a5bf-4630-a100-d2c0c3b5b964', 'brand': 'Patagonia', 'name': 'Celebrator Doppelbock', 'style': 'English Brown Ale', 'hop': 'Yakima Gol', 'yeast': '1272 - American Ale II', 'malts': 'Wheat mal', 'ibu': '32 IBU', 'alcohol': '5.6%', 'blg': '5.3°Blg'}
                ,{'id': 2960, 'uid': '94dee6da-987b-496b-8a55-bbd6cb5b9003', 'brand': 'Lowenbrau', 'name': 'Samuel Smith’s Oatmeal Stout', 'style': 'Pilsner', 'hop': 'Bullion', 'yeast': '3463 - Forbidden Fruit', 'malts': 'Carapils', 'ibu': '90 IBU', 'alcohol': '5.7%', 'blg': '18.3°Blg'}
                ,{'id': 2960, 'uid': '94dee6da-987b-496b-8a55-bbd6cb5b9003', 'brand': 'Lowenbrau', 'name': 'Samuel Smith’s Oatmeal Stout', 'style': 'Pilsner', 'hop': 'Bullion', 'yeast': '3463 - Forbidden Fruit', 'malts': 'Carapils', 'ibu': '90 IBU', 'alcohol': '5.7%', 'blg': '18.3°Blg'}
                ,{'id': 7181, 'uid': '98f4f80f-db7f-4e29-8252-89cfa8fefcb2', 'brand': 'Kirin', 'name': 'Edmund Fitzgerald Porter', 'style': 'English Pale Ale', 'hop': 'Mosaic', 'yeast': '1332 - Northwest Ale', 'malts': 'Munich', 'ibu': '89 IBU', 'alcohol': '7.8%', 'blg': '11.1°Blg'}
                ,{'id': 3730, 'uid': 'f1b631cd-27c5-45d5-97e1-98a4af6e1f91', 'brand': 'Sierra Nevada', 'name': 'Double Bastard Ale', 'style': 'Vegetable Beer', 'hop': 'Chinook', 'yeast': '3763 - Roeselare Ale Blend', 'malts': 'Black malt', 'ibu': '85 IBU', 'alcohol': '3.4%', 'blg': '13.6°Blg'}]
    
    # Los datos obtenidos de la API se conviertene en diccionarios que se pueden convertir 
    # en Dataframe sin realizar ningun proceso adicional
    
    df = pd.DataFrame(convertir)

    #Elimino columna con datos que no serán insertados en la tabla de redshift
    p0 = df.drop(['uid'], axis=1)

    #Quito sufijos de 3 campos medibles y convierto el tipo de dato de str a int o float según corresponda.
    p0['ibu'] = p0['ibu'].replace({' IBU': ''},regex=True).astype(int)
    p0['alcohol'] = p0['alcohol'].replace({'%': ''},regex=True).astype(float)
    p0['blg'] = p0['blg'].replace({'°Blg': ''},regex=True).astype(float)

    #Elimino registros duplicados que pudiera recibir de la API y renombro los nombre de los campos recibidos 
    # por los nombre de los campos que se definieron en la tabla 'cerveza'
    p1 = p0.drop_duplicates().rename(columns={'brand':'marca',
                                              'name':'nombre',
                                              'style':'estilo',
                                              'hop':'lupulo',
                                              'yeast':'levadura',
                                              'malts':'malta',
                                              'ibu':'amargor'})
    return p1

try: 
    try:
        print('1 - Intentando obtener datos de la API')
        dft = procesarDatos()
    except:
        raise Exception(1)
    #Vuelco los datos en una tabla staging que se usará para identificar datos duplicados en la tabla de redshift
    # se utiliza if_exists='replace' para que se borren los datos en la siguiente ejecución
    #Redshift ya no soporta ON CONFLIC ni upsert para evitar los registros duplicados que se vayan a insertar
    #Utilizo dtype para definir el tamaño y tipo de los campos de la tabla staging
    #para que coincida con lo definido en la tabla cerveza.
    try:
        print('2 - Iniciar conexión con la DB en Redshift')
        conn_engine = conect.connRedshiftAlchemy()
        conn_engine.execution_options(isolation_level="AUTOCOMMIT")
        conn_engine.execute('SELECT version();')
    except:
        raise Exception(2)
    try:
        print('3 - Iniciando volcado de datos en tabla staging')
        dft.to_sql(name='staging'
                ,con=conn_engine
                ,schema='marcocalle86_coderhouse'
                ,if_exists='replace'
                ,index=False
                ,dtype={'id': sqlalchemy.types.INTEGER()
                            ,'marca': sqlalchemy.types.VARCHAR(50)
                            ,'nombre': sqlalchemy.types.VARCHAR(50)
                            ,'estilo': sqlalchemy.types.VARCHAR(50)
                            ,'lupulo': sqlalchemy.types.VARCHAR(50)
                            ,'levadura': sqlalchemy.types.VARCHAR(50)
                            ,'malta': sqlalchemy.types.VARCHAR(40)
                            ,'amargor': sqlalchemy.types.INTEGER()
                            ,'alcohol': sqlalchemy.types.Numeric(4,2)
                            ,'blg': sqlalchemy.types.Numeric(4,2)})
    except:
        raise Exception(3)
    try:    
        #Inserto los registros nuevos en la tabla final 
        print('4 - Identificar datos unicos e insertar en tabla cerveza')
        conn_engine.execute("""INSERT INTO marcocalle86_coderhouse.cerveza
                            SELECT st.id, st.marca, st.nombre, st.estilo, st.lupulo, st.levadura, st.malta, st.amargor, st.alcohol, st.blg
                            FROM marcocalle86_coderhouse.staging AS st
                            LEFT JOIN marcocalle86_coderhouse.cerveza AS cv on st.id = cv.id
                            WHERE cv.id is NULL""")
    except:
        raise Exception(4)
    #Borro la tabla staging para liberar espacio en disco
    try:
        print('5 - Borrado de tabla staging')
        conn_engine.execute("""DROP TABLE marcocalle86_coderhouse.staging""")
    except:
        raise Exception(5)

    print(0)
except Exception as e:
    print(e)


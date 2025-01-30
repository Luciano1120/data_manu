#para hacer pruebas aisladas desde jupiter ya q desde el Main no puedo

import pandas as pd
from unidecode import unidecode
from transformaciones.renombraCampos import renombrar_y_filtrar
from cargaArchivos import carga_url_gDrive as cd , carga_url_oDrive as co
from transformaciones.preguntas import filtroPreg 
from transformaciones.renombraCampos import renombrar_y_filtrar
from raw import datasetsEncuestas as de, datasetPreguntas as dp, datasetMapeos as dm
from funciones import comproCursoAnterior 



#cargo preguntas
dfPreg=co(dp["dfPreg"]["url"],dp["dfPreg"]["sheet_name"]) #entro al diccionario de la variable dp y le pido el valor url y luego lo mismo para la hoja

dfPreg=filtroPreg(dfPreg) #filtro el dataset usando la funcion filtroPreg
mapeo_nombres = dict(zip(dfPreg['Pregunta'], dfPreg['Contexto'])) #ver q

#Cargo Tablas para Mapeos
T_pais=co(dm["T_Pais"]["url"],dm["T_Pais"]["sheet_name"])
T_pais['Pais'] = T_pais['Pais'].str.strip().str.lower().apply(unidecode)

T_Edad=co(dm["T_Edad"]["url"],dm["T_Edad"]["sheet_name"])
T_Edad['Edad'] = T_Edad['Edad'].str.strip().str.lower().apply(unidecode)

T_Ingresos=co(dm["T_Ingresos"]["url"],dm["T_Ingresos"]["sheet_name"])
T_Ingresos['Ingresos'] = T_Ingresos['Ingresos'].str.strip().str.lower().apply(unidecode)

T_SituacionLaboral=co(dm["T_SituacionLaboral"]["url"],dm["T_SituacionLaboral"]["sheet_name"])
T_SituacionLaboral['Situacion Laboral'] = T_SituacionLaboral['Situacion Laboral'].str.strip().str.lower().apply(unidecode)



#cargo archivos de encuestas ya quitando espacios a nombres de columnas
dataframes = {} #va a ser un json q almacena nombre de dataset como Key y el los Datos del Dataset como Valor
for datasetJs, infoJs in de.items(): #datasetJs son las key e infoJs los valores
    
    df = co(infoJs["url"], infoJs["sheet_name"])
    # Cargar el dataset usando la función carga_url_oDrive
    dataframes[datasetJs] = df  #en este caso cada Dataset llamado url_1c, url_2c, etc se le asignan los datos (df q es el dataset q cargo en el paso anterior), y así para cada uno en cada vuelta. En comentario debajo es como los llamo. Ver en pruebasDataset.ipynb
    #dataframes["url_1c"].head()

    dataframes[datasetJs]=renombrar_y_filtrar(dataframes[datasetJs],mapeo_nombres) #mapeo nombre de campos enn base a Contexto

    dataframes[datasetJs]['Origen']=datasetJs #le agrego campo con origen del dataset

    df_consolidado = pd.concat(dataframes.values(), ignore_index=True)

df_consolidado['Pais'] = df_consolidado['Pais'].astype(str)
df_consolidado['Pais'] = df_consolidado['Pais'].str.strip().str.lower().apply(unidecode).str.strip()

df_consolidado['Ingresos'] = df_consolidado['Ingresos'].astype(str)
df_consolidado['Ingresos'] = df_consolidado['Ingresos'].str.strip().str.lower().apply(unidecode)

df_consolidado['Edad'] = df_consolidado['Edad'].astype(str)
df_consolidado['Edad'] = df_consolidado['Edad'].str.strip().str.lower().apply(unidecode)


df_consolidado['Situacion Laboral'] = df_consolidado['Situacion Laboral'].astype(str)
df_consolidado['Situacion Laboral'] = df_consolidado['Situacion Laboral'].str.strip().str.lower().apply(unidecode)


df_consolidado = df_consolidado.merge(T_pais, on='Pais', how='left')
df_consolidado = df_consolidado.merge(T_Ingresos, on='Ingresos', how='left')
df_consolidado = df_consolidado.merge(T_Edad, on='Edad', how='left')
df_consolidado = df_consolidado.merge(T_SituacionLaboral, on='Situacion Laboral', how='left')

df_consolidado = df_consolidado.fillna("sin info")

df_consolidado['comproCursoAnterior'] = df_consolidado['¿Has comprado algún otro curso de Emprendelandia?'].apply(comproCursoAnterior)


df_consolidado['TipoEncuesta']=df_consolidado['Origen'].str[3] #agrego campo para identificar el Origen si es Lead o Comprador

df_consolidado_Comp = df_consolidado[df_consolidado['TipoEncuesta'] == 'c'] #filtro solo compradores
df_consolidado_Leads = df_consolidado[df_consolidado['TipoEncuesta'] == 'l'] #filtro solo leads

df_consolidado_7l = df_consolidado[df_consolidado['Origen'] == 'df7l'] #filtro solo la 7ma
df_consolidado_7c = df_consolidado[df_consolidado['Origen'] == 'df7c'] #filtro solo la 7ma


#df_consolidado=df_consolidado.dropna(axis=0)# Filas q tenga algun nulo dentro del registro será removida
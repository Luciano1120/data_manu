
from data_loader import carga_datos 
import numpy as np
from transformaciones.enconding import enconding as en
from transformaciones.feature_engineering import aplicar_pca
import pandas as pd


df_consolidado, df_consolidado_Comp, df_consolidado_Leads, df_consolidado_7l, df_consolidado_7c = carga_datos()


#para armado del Cluster de 7l
campos_a_conservar7l = [ "Estudios", "Conocimiento Importaciones", "¿Cómo conociste a Valeria o a Emprendelandia?","Tiempo Disponible en el Dia", "Tiempo dispuesto a Invertir Meses", "Sosten Economico", "Ingresos Prom", "EdadProm", "Situacion Laboral M","comproCursoAnterior","Info Ingresos"]


df_consolidado_7l_antesEncod = df_consolidado_7l[campos_a_conservar7l].dropna()
df_consolidado_7l_antesEncod.drop(columns=["¿Cómo conociste a Valeria o a Emprendelandia?","Info Ingresos"],inplace=True) #saco esta columna q no me sirve para el cluster


# lo vuelvo a hacer para q me quede el df con encoding
df_consolidado_7l_encoded = en(df_consolidado_7l[campos_a_conservar7l].dropna().drop(columns=["¿Cómo conociste a Valeria o a Emprendelandia?","Info Ingresos"]))



#Antes de aplicar PCA, hay que convertir las variables categóricas en formato numérico
# con PCA reduzco la cantidad de variables, pero las nuevas variables son combinaciones de las originales, yo tenia 15 originales y ahora tengo 40, pero es por q aplique encoding lo q hice incrementar la cantidad de variables. Ya que el encoding me llevo el dataset a 47 columnas
df_pca_7l_encoded, modelo_pca = aplicar_pca(df_consolidado_7l_encoded, 17)
#no puedo poner como argumento de variables PC mas de la cantidad de variables Originales- Por eso me dio error cuando tenia 40 dado q reduje la cant de variables
#PCA transforma los datos generando nuevos campos de combinacion con las variables originales y con el metodo del CODO aplico la cantidad de PC necesarias para bajar la cantidad

#---------------------------------------------------------------------
#puedo ver desde mi jupyter este df sin pasarlo por una funcion
dfPrueba = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5],
    "Nombre": ["Ana", "Luis", "Carlos", "María", "Sofía"],
    "Edad": [25, 30, 22, 35, 28],
    "Ciudad": ["Buenos Aires", "Madrid", "Lima", "Santiago", "Bogotá"]
})






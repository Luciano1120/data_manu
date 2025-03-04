
from data_loader import carga_datos 
import numpy as np
from transformaciones.enconding import enconding as en
from transformaciones.feature_engineering import aplicar_pca
import pandas as pd


df_consolidado, df_consolidado_Comp, df_consolidado_Leads, df_consolidado_7l, df_consolidado_7c = carga_datos()


#para armado del Cluster de 7c
campos_a_conservar7c = [ "Estudios", "Conocimiento Importaciones", "¿Cómo conociste a Valeria o a Emprendelandia?","Tiempo Disponible en el Dia", "Tiempo dispuesto a Invertir Meses", "Sosten Economico", "Ingresos Prom", "EdadProm", "Situacion Laboral M","comproCursoAnterior","Info Ingresos"]


df_consolidado_7c_antesEncod = df_consolidado_7c[campos_a_conservar7c].dropna()
df_consolidado_7c_antesEncod.drop(columns=["¿Cómo conociste a Valeria o a Emprendelandia?","Info Ingresos"],inplace=True) #saco esta columna q no me sirve para el cluster


df_consolidado_7c_encoded = en(df_consolidado_7c[campos_a_conservar7c].drop(columns=["¿Cómo conociste a Valeria o a Emprendelandia?","Info Ingresos"]).dropna())


df_pca_7c_encoded, modelo_pca = aplicar_pca(df_consolidado_7c_encoded, 15)



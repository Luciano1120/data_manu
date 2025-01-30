import streamlit as st


def filtroPreg(preg):

    
    preg['Considerar']=preg['Considerar'].str.lower() # de haber algun elemento del campo en mayuscula lo convierte a minuscula

    preguntas_filtradas = preg.query('Considerar== "si"').reset_index(drop=True) #filtro solo las a cosiderar = si

    return preguntas_filtradas


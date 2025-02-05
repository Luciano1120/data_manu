import streamlit as st
import pandas as pd
from unidecode import unidecode
from transformaciones.renombraCampos import renombrar_y_filtrar
from cargaArchivos import carga_url_gDrive as cd , carga_url_oDrive as co
from transformaciones.preguntas import filtroPreg 
from transformaciones.renombraCampos import renombrar_y_filtrar
from raw import datasetsEncuestas as de, datasetPreguntas as dp, datasetMapeos as dm
from funciones import comproCursoAnterior 
from graficos import grafico_barras as gb, grafico_barras_sinInfo as gbsi

from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling.config import Settings
import streamlit.components.v1 as components

from data_loader import carga_datos 



def main():  

    st.set_page_config(layout="wide", #aprovecho todo el ancho de la web, se debe definir al principio
                       initial_sidebar_state= "expanded") 
    
    if 'df_consolidado' not in st.session_state:
        # Cargar los datos solo si no están en session_state
        df_consolidado, df_consolidado_Comp, df_consolidado_Leads, df_consolidado_7l, df_consolidado_7c = carga_datos()

        # Guardar los datos en session_state
        st.session_state.df_consolidado = df_consolidado
        st.session_state.df_consolidado_Comp = df_consolidado_Comp
        st.session_state.df_consolidado_Leads = df_consolidado_Leads
        st.session_state.df_consolidado_7l = df_consolidado_7l
        st.session_state.df_consolidado_7c = df_consolidado_7c
    else:
        # Usar los datos desde session_state si ya están cargados
        df_consolidado = st.session_state.df_consolidado
        df_consolidado_Comp = st.session_state.df_consolidado_Comp
        df_consolidado_Leads = st.session_state.df_consolidado_Leads
        df_consolidado_7l = st.session_state.df_consolidado_7l
        df_consolidado_7c = st.session_state.df_consolidado_7c
    
    
    #Armo la Barra de Navegacion
    
    st.sidebar.success("Selecciona una página arriba 👆")

    

   

    #Cuando sea necesario se los exporto a Excel, quizas debería sacarlo de acá a las lineas comentadsas debajo,, y hacerle algun boton, ya q me come performance
    #df_consolidado.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetConsol.xlsx',index=False, encoding="utf-8-sig", engine="openpyxl")
        
    #df_consolidado_Comp.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetComp.xlsx',index=False,  engine="openpyxl")
    
    #df_consolidado_Leads.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetLead.xlsx',index=False,  engine="openpyxl")
    
    

if __name__=="__main__":
    main()
import pandas as pd
import streamlit as st



#archivos de googleDrive
@st.cache_data
def carga_url_gDrive(ruta,sheet):

    df_gd=pd.read_excel(ruta,sheet)
    df_gd.columns = df_gd.columns.str.strip()    

    return df_gd



#cargo archivos de OneDrive
#el decorador solo se puede usar para funciones, metodos o Clases
@st.cache_data
def carga_url_oDrive(ruta,sheet):

    df_od= pd.read_excel(ruta,sheet,index_col=None)
    
    return df_od




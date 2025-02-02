import streamlit as st
import pandas as pd
from unidecode import unidecode
from transformaciones.renombraCampos import renombrar_y_filtrar
from cargaArchivos import carga_url_gDrive as cd , carga_url_oDrive as co
from transformaciones.preguntas import filtroPreg 
from transformaciones.renombraCampos import renombrar_y_filtrar
from raw import datasetsEncuestas as de, datasetPreguntas as dp, datasetMapeos as dm
from funciones import comproCursoAnterior 
from graficos import grafico_barras as gb

from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling.config import Settings
import streamlit.components.v1 as components



def main():  

    st.set_page_config(layout="wide") #aprovecho todo el ancho de la web
    st.title("Emprendelandia") #h1
    st.header("Encuestas") #h2
    #st.subheaderheader("Emprendelandia") #h3

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

    #duracion aprox: to csv 4' y to excel 5' 37984 registros
    #el csv se ve correctamente en cuanto a caracteres especiales desde el bloc de notas (ya q cuando se manda a csv usa utf-8 por default pero se corrompen cuando lo abro desde excel, al usar utf-8-sig se ven correctamente desde excel)
    #"""df_consolidado.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\pruebaDatasetConsol.csv',index=False, encoding="utf-8-sig", #line_terminator="\n", quoting=1)"""
        
     #lo exporto excel para subsanar algunos registros q se abren en dif lineas
    
    #df_consolidado=df_consolidado.dropna(axis=0)# Filas q tenga algun nulo dentro del registro será removida

    df_consolidado = df_consolidado.fillna("sin info")

    df_consolidado['comproCursoAnterior'] = df_consolidado['¿Has comprado algún otro curso de Emprendelandia?'].apply(comproCursoAnterior)

    df_consolidado['TipoEncuesta']=df_consolidado['Origen'].str[3] #agrego campo para identificar el Origen si es Lead o Comprador

    
    campos_a_conservar = [
    "Estudios", "Conocimiento Importaciones", "¿Cómo conociste a Valeria o a Emprendelandia?",
    "Tiempo Disponible en el Dia", "Tiempo dispuesto a Invertir Meses", "Sosten Economico",
    "M_Pais", "Ingresos Prom", "Ingreso_Calidad", "EdadProm", "RangoEtario", "Situacion Laboral M","comproCursoAnterior","TipoEncuesta","Origen"
    ]


    df_consolidado=df_consolidado[campos_a_conservar]
    
    
    df_consolidado_Comp = df_consolidado[df_consolidado['TipoEncuesta'] == 'c'] #filtro solo compradores
    df_consolidado_Leads = df_consolidado[df_consolidado['TipoEncuesta'] == 'l'] #filtro solo leads

    df_consolidado_7l = df_consolidado[df_consolidado['Origen'] == 'df7l'] #filtro solo la 7ma
    df_consolidado_7c = df_consolidado[df_consolidado['Origen'] == 'df7c'] #filtro solo la 7ma



    #df_consolidado.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetConsol.xlsx',index=False, encoding="utf-8-sig", engine="openpyxl")
        
    df_consolidado_Comp.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetComp.xlsx',index=False,  engine="openpyxl")
    
    df_consolidado_Leads.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetLead.xlsx',index=False,  engine="openpyxl")
    
    # Carga Dataset en StreamLit
    title0= "Dataset Leads Condolidado"
    st.markdown(f"## {title0}")
    
    st.dataframe(df_consolidado_7c) # me carga la tabla del dataset, no es recomendable usar st.table() ya q carga una tabla muy grande y no es interactiva
    
    #para generar Pandas Profiling-------------------------------------
    
    title1= "Reporte de Leads Pandas Profiling"
    st.markdown(f"## {title1}")
    
    profile = ProfileReport(
                            df_consolidado_Leads, 
                            title=title1, 
                             html={"style": {"full_width": True}}
                            )
    
    st_profile_report(profile)

    title2= "Reporte de Compradores Pandas Profiling"
    st.markdown(f"## {title2}")
    profile2 = ProfileReport(
                            df_consolidado_Comp, 
                            title=title2, 
                             html={"style": {"full_width": True}}
                            )
    
    st_profile_report(profile2)


    titleLeads7ma= "Reporte de 7ma Leads Pandas Profiling"
    st.markdown(f"## {titleLeads7ma}")
    profile3 = ProfileReport(
                            df_consolidado_7l, 
                            title=titleLeads7ma, 
                             html={"style": {"full_width": True}}
                            )
    
    st_profile_report(profile3)

    titleComp7ma= "Reporte de 7ma Compradores Pandas Profiling"
    st.markdown(f"## {titleComp7ma}")
    profile4 = ProfileReport(
                            df_consolidado_7c, 
                            title=titleComp7ma, 
                             html={"style": {"full_width": True}}
                            )
    
    st_profile_report(profile4)
    #--------------------------------------------

    #Para Generar Graficas de Variables de Dataset de Leads Consolidado-----
    
    title3= "Analisis Univariado de Leads"
    st.markdown(f"## {title3}")
    col1, col2, col3 = st.columns(3) #defino los alias de 3 columnas y le paso como argumento la cantidad (3)
    
    with col1:

        variable1= "M_Pais"
        st.header(variable1)
        gb(df_consolidado_Leads, variable1)

    with col2:
        variable2= "Estudios"
        st.header(variable2)
        gb(df_consolidado_Leads, variable2)    

    with col3:
        variable3= "Situacion Laboral M"
        st.header(variable3)
        gb(df_consolidado_Leads, variable3)        


    col4, col5, col6 = st.columns(3) #defino otra fila de 3 columnas
    
    with col4:

        variable4= "Conocimiento Importaciones"
        st.header(variable4)
        gb(df_consolidado_Leads, variable4)

    with col5:
        variable5= "¿Cómo conociste a Valeria o a Emprendelandia?"
        st.header(variable5)
        gb(df_consolidado_Leads, variable5)    

    with col6:
        variable6= "Tiempo Disponible en el Dia"
        st.header(variable6)
        gb(df_consolidado_Leads, variable6)        


        #Dataset de Compradores Consolidado
    title4= "Analisis Univariado de Compradores"
    st.markdown(f"## {title4}")
    
    col7, col8, col9 = st.columns(3) #defino los alias de 3 columnas y le paso como argumento la cantidad (3)
    
    with col7:

        variable7= "M_Pais"
        st.header(variable7)
        gb(df_consolidado_Comp, variable7)

    with col8:
        variable8= "Estudios"
        st.header(variable8)
        gb(df_consolidado_Comp, variable8)    

    with col9:
        variable9= "Situacion Laboral M"
        st.header(variable9)
        gb(df_consolidado_Comp, variable9)        


    col10, col11, col12 = st.columns(3) #defino otra fila de 3 columnas
    
    with col10:

        variable10= "Conocimiento Importaciones"
        st.header(variable10)
        gb(df_consolidado_Comp, variable10)

    with col11:
        variable11= "¿Cómo conociste a Valeria o a Emprendelandia?"
        st.header(variable11)
        gb(df_consolidado_Comp, variable11)    

    with col12:
        variable12= "Tiempo Disponible en el Dia"
        st.header(variable12)
        gb(df_consolidado_Comp, variable12)        



        #Dataset de 7ma Generacion Leads
    title5= "Analisis Univariado de 7ma Gneracion Leads"
    st.markdown(f"## {title5}")
    
    col13, col14, col15 = st.columns(3) #defino los alias de 3 columnas y le paso como argumento la cantidad (3)
    
    with col13:

        variable13= "M_Pais"
        st.header(variable13)
        gb(df_consolidado_7l, variable13)

    with col14:
        variable14= "Estudios"
        st.header(variable14)
        gb(df_consolidado_7l, variable14)    

    with col15:
        variable15= "Situacion Laboral M"
        st.header(variable15)
        gb(df_consolidado_7l, variable15)        


    col16, col17, col18 = st.columns(3) #defino otra fila de 3 columnas
    
    with col16:

        variable16= "Conocimiento Importaciones"
        st.header(variable16)
        gb(df_consolidado_7l, variable16)

    with col17:
        variable17= "¿Cómo conociste a Valeria o a Emprendelandia?"
        st.header(variable17)
        gb(df_consolidado_7l, variable17)    

    with col18:
        variable18= "Tiempo Disponible en el Dia"
        st.header(variable18)
        gb(df_consolidado_7l, variable18)            




        #Dataset de 7ma Generacion Compradores
    title6= "Analisis Univariado de 7ma Gneracion Compradores"
    st.markdown(f"## {title6}")
    
    col19, col20, col21 = st.columns(3) 
    
    with col19:

        variable19= "M_Pais"
        st.header(variable19)
        gb(df_consolidado_7l, variable19)

    with col20:
        variable20= "Estudios"
        st.header(variable20)
        gb(df_consolidado_7l, variable20)    

    with col21:
        variable21= "Situacion Laboral M"
        st.header(variable21)
        gb(df_consolidado_7l, variable21)        


    col22, col23, col24 = st.columns(3) #defino otra fila de 3 columnas
    
    with col22:

        variable22= "Conocimiento Importaciones"
        st.header(variable22)
        gb(df_consolidado_7l, variable22)

    with col23:
        variable23= "¿Cómo conociste a Valeria o a Emprendelandia?"
        st.header(variable23)
        gb(df_consolidado_7l, variable23)    

    with col24:
        variable24= "Tiempo Disponible en el Dia"
        st.header(variable24)
        gb(df_consolidado_7l, variable24)            
    #--------------------------------------------------------------------

if __name__=="__main__":
    main()
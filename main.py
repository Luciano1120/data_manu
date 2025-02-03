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

    st.set_page_config(layout="wide") #aprovecho todo el ancho de la web, se debe definir al principio
    
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
    st.sidebar.title("Navegación") #permite una barra de Navegacion a la izquierda
    pagina = st.sidebar.radio("Ir a:", ["Inicio", "EDA", "Analisis"]) # le da contenido al sidebar

    

   

    #Cuando sea necesario se los exporto a Excel, quizas debería sacarlo de acá a las lineas comentadsas debajo,, y hacerle algun boton, ya q me come performance
    #df_consolidado.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetConsol.xlsx',index=False, encoding="utf-8-sig", engine="openpyxl")
        
    #df_consolidado_Comp.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetComp.xlsx',index=False,  engine="openpyxl")
    
    #df_consolidado_Leads.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetLead.xlsx',index=False,  engine="openpyxl")
    
    #Pagina Inicio
    if pagina == "Inicio": 
        st.title("Emprendelandia") #h1
        st.header("Encuestas") #h2
        #st.subheaderheader("Emprendelandia") #h3
    
    # Carga Dataset en StreamLit
        title0= "Dataset Leads Condolidado"
        st.markdown(f"## {title0}")
        
        st.dataframe(df_consolidado_7c) # me carga la tabla del dataset, no es recomendable usar st.table() ya q carga una tabla muy grande y no es interactiva
            
        
    elif pagina == "EDA":
        
        #para generar Pandas Profiling-------------------------------------
        
        

        title1= "Reporte de Leads Pandas Profiling"
        st.markdown(f"## {title1}")

        if 'profile' not in st.session_state:
            """ la sesion se reinicia cuando se recarga la pagina,
             profile es una alias para guardar dicho proceso, q le paso despues cuando quiero dejar iniciada la sesion """    
            profile = ProfileReport(
                                    df_consolidado_Leads, 
                                    title=title1, 
                                    html={"style": {"full_width": True}}
                                    )
            st.session_state.profile = profile

        else: 
            profile=st.session_state.profile    
            
        st_profile_report(profile)

        title2= "Reporte de Compradores Pandas Profiling"
        st.markdown(f"## {title2}")

        if 'profile2' not in st.session_state:


            profile2 = ProfileReport(
                                    df_consolidado_Comp, 
                                    title=title2, 
                                    html={"style": {"full_width": True}}
                                    )
            
            st.session_state.profile2 = profile2
            
        else:
            profile2=st.session_state.profile2    

        st_profile_report(profile2)


        titleLeads7ma= "Reporte de 7ma Leads Pandas Profiling"
        st.markdown(f"## {titleLeads7ma}")

        if 'profile3' not in st.session_state:

            profile3 = ProfileReport(
                                    df_consolidado_7l, 
                                    title=titleLeads7ma, 
                                    html={"style": {"full_width": True}}
                                    )

            st.session_state.profile3=profile3

        else:     
             profile3=st.session_state.profile3

        st_profile_report(profile3)

        
        titleComp7ma= "Reporte de 7ma Compradores Pandas Profiling"
        st.markdown(f"## {titleComp7ma}")
        
        if 'profile4' not in st.session_state:
            profile4 = ProfileReport(
                                df_consolidado_7c, 
                                title=titleComp7ma, 
                                html={"style": {"full_width": True}}
                                )
            st.session_state.profile4= profile4
        
        else: 
            profile4=st.session_state.profile4

        st_profile_report(profile4)
        #--------------------------------------------
    elif pagina == "Analisis" :
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

            variable4= "M_Pais"
            st.header(f'{variable4} Filtando sin Info' )
            gbsi(df_consolidado_Leads, variable4)

        with col5:
            variable5= "Estudios"
            st.header(variable5)
            gbsi(df_consolidado_Leads, variable5)    

        with col6:
            variable6= "Situacion Laboral M"
            st.header(variable6)
            gbsi(df_consolidado_Leads, variable6)        


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
import streamlit as st
from data_loader import carga_datos 
from transformaciones.enconding import enconding as en
from transformaciones.feature_engineering import aplicar_pca



def main():  

    st.set_page_config(layout="wide", #aprovecho todo el ancho de la web, se debe definir al principio
                       initial_sidebar_state= "expanded") 
    
    if 'df_consolidado' not in st.session_state:
        # Cargar los datos solo si no están en session_state
        df_consolidado, df_consolidado_Comp, df_consolidado_Leads, df_consolidado_7l, df_consolidado_7c = carga_datos()

        # Crear una copia para Feature Engineering (sin modificar los datos originales)
        #para armado del Cluster de 7l
        campos_a_conservar7l = [ "Estudios", "Conocimiento Importaciones", "¿Cómo conociste a Valeria o a Emprendelandia?","Tiempo Disponible en el Dia", "Tiempo dispuesto a Invertir Meses", "Sosten Economico", "Ingresos Prom", "EdadProm", "Situacion Laboral M","comproCursoAnterior","Info Ingresos"]
        df_consolidado_7l_encoded = df_consolidado_7l[campos_a_conservar7l].copy()
        df_consolidado_7l_encoded = en(df_consolidado_7l_encoded)

        # Aplicar PCA, y le paso cantidad de componentes PCA a conservar con el metodo del CODO
        df_pca_7l_encoded, modelo_pca = aplicar_pca(df_consolidado_7l_encoded, 40)


        # Guardar los datos en session_state
        st.session_state.df_consolidado = df_consolidado
        st.session_state.df_consolidado_Comp = df_consolidado_Comp
        st.session_state.df_consolidado_Leads = df_consolidado_Leads
        st.session_state.df_consolidado_7l = df_consolidado_7l
        st.session_state.df_consolidado_7c = df_consolidado_7c
        st.session_state.df_consolidado_7l_encoded = df_consolidado_7l_encoded #agrego el df con encoding
        st.session_state.df_pca_7l_encoded = df_pca_7l_encoded  # agrego el PCA
        
    else:
        # Usar los datos desde session_state si ya están cargados
        df_consolidado = st.session_state.df_consolidado
        df_consolidado_Comp = st.session_state.df_consolidado_Comp
        df_consolidado_Leads = st.session_state.df_consolidado_Leads
        df_consolidado_7l = st.session_state.df_consolidado_7l
        df_consolidado_7c = st.session_state.df_consolidado_7c
        df_consolidado_7l_encoded = st.session_state.df_consolidado_7l_encoded #agrego el df con encoding
        df_pca_7l_encoded = st.session_state.df_pca_7l_encoded  

    df_consolidado_7l_encoded=df_consolidado_7l_encoded.dropna() # Filas q tenga algun nulo dentro del registro será removida (pierdo 2 registros q no tenian sentido)
    
    
    #Armo la Barra de Navegacion con la carpeta pages y ordenando los archivos por nombre
    st.sidebar.success("Selecciona una página arriba 👆") #es una linea q agrego al sidebar

    

   

    #Cuando sea necesario se los exporto a Excel, quizas debería sacarlo de acá a las lineas comentadsas debajo,, y hacerle algun boton, ya q me come performance
    #df_consolidado.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetConsol.xlsx',index=False, encoding="utf-8-sig", engine="openpyxl")
        
    #df_consolidado_Comp.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetComp.xlsx',index=False,  engine="openpyxl")
    
    #df_consolidado_Leads.to_excel(r'C:\Users\lucia\OneDrive\Laboral\manu\DatasetLead.xlsx',index=False,  engine="openpyxl")
    
    

if __name__=="__main__":
    main()
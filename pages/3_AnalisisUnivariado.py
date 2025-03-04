import streamlit as st
from graficos import grafico_barras as gb, grafico_barras_sinInfo as gbsi

st.title("Análisis Univariado")

if 'df_consolidado_Leads' not in st.session_state:
    st.warning("No hay datos cargados. Vuelve a la página principal para cargar los datos.")
else:
    datasets = {
       "Leads": st.session_state.df_consolidado_Leads,
        "Compradores": st.session_state.df_consolidado_Comp,
        "7ma Leads": st.session_state.df_consolidado_7l,
        "7ma Compradores": st.session_state.df_consolidado_7c,
    }

    variables = ["M_Pais", "Estudios", "Situacion Laboral M", "Conocimiento Importaciones","¿Cómo conociste a Valeria o a Emprendelandia?","Tiempo Disponible en el Dia","Tiempo dispuesto a Invertir Meses","Sosten Economico","Ingresos Prom","Ingreso_Calidad","EdadProm","RangoEtario","comproCursoAnterior","Info Ingresos"]

    selected_variable = st.selectbox("Selecciona una Variable para analizar", variables)

    st.write(f"### Análisis de {selected_variable} en distintos datasets")

    # Primera fila con dos gráficos
    cols1 = st.columns(2)
    with cols1[0]:
        st.subheader("Leads")
        gbsi(datasets["Leads"], selected_variable)

    with cols1[1]:
        st.subheader("Compradores")
        gbsi(datasets["Compradores"], selected_variable)

    # Segunda fila con los otros dos gráficos
    cols2 = st.columns(2)
    with cols2[0]:
        st.subheader("7ma Leads")
        gbsi(datasets["7ma Leads"], selected_variable)

    with cols2[1]:
        st.subheader("7ma Compradores")
        gbsi(datasets["7ma Compradores"], selected_variable)
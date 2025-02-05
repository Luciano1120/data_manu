
import streamlit as st

st.title("Emprendelandia") #h1
st.header("Encuestas") #h2
#st.subheaderheader("Emprendelandia") #h3

if 'df_consolidado_7c' in st.session_state:
    st.markdown("## Dataset Leads Consolidado")
    st.dataframe(st.session_state.df_consolidado_7c)  # consume del main mientras esté la seson iniciada
else:
    st.warning("Los datos aún no se han cargado. Ve a la página principal primero.")
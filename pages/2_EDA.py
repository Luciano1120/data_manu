import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling.config import Settings

title1= "Reporte de Leads Pandas Profiling"
st.markdown(f"## {title1}")

datasets = {
    "Leads": "df_consolidado_Leads",
    "Compradores": "df_consolidado_Comp",
    "7ma Leads": "df_consolidado_7l",
    "7ma Compradores": "df_consolidado_7c",
}

selected_dataset = st.selectbox("Selecciona un dataset para analizar", list(datasets.keys()))

if datasets[selected_dataset] in st.session_state:
    df = st.session_state[datasets[selected_dataset]]

    if f"profile_{selected_dataset}" not in st.session_state:
        profile = ProfileReport(df, title=f"Reporte {selected_dataset}", html={"style": {"full_width": True}})
        st.session_state[f"profile_{selected_dataset}"] = profile
    else:
        profile = st.session_state[f"profile_{selected_dataset}"]

    st_profile_report(profile)
else:
    st.warning("No hay datos cargados. Vuelve a la página principal para cargar los datos.")
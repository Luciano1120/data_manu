#funciones q implican transformaciones de dataset. Especificas y dificilmente reutilizables
import streamlit as st

@st.cache_data
def renombrar_y_filtrar(df, mapeo):

    df.columns = df.columns.str.strip()

    #print("Columnas antes del renombrado:", df.columns)

    df_renombrado = df.rename(columns=mapeo)

    #print("Columnas después del renombrado:", df_renombrado.columns)

    # Filtrar columnas válidas que existen en el DataFrame renombrado
    columnas_validas = [col for col in mapeo.values() if col in df_renombrado.columns]

    #print("Columnas válidas después del filtro:", columnas_validas)

    # Retornar solo las columnas válidas
    df_final = df_renombrado[columnas_validas]

    # Verificar columnas antes de eliminar duplicados
    #print("Columnas antes de eliminar duplicados:", df_final.columns)

    # Eliminar columnas duplicadas
    df_final = df_final.loc[:, ~df_final.columns.duplicated()]

    # Verificar columnas después de eliminar duplicados
    #print("Columnas después de eliminar duplicados:", df_final.columns)

    return df_final
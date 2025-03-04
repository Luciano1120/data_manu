import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

def grafico_barras(df, variable):
    """
    Función para crear un gráfico de barras horizontales.
    Este tipo de Comentarios Doctrings se usan dentro de clases o funciones, si no se entienden como strings
    """
    dfAg = df[variable].value_counts().reset_index() #con reset_index lo convierto en dataframe
    dfAg.columns = [variable, "Cantidad"]  #renombro las columnas, col 1 : con el nombre de la Variable y la 2 con la Cantidad
    total = df[variable].count()
    dfAg["Porcentaje"] = (dfAg["Cantidad"] / total) * 100  # Calcula el porcentaje para cada fila

    # Configuración del gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dfAg, x="Cantidad", y=variable, palette="pastel")  # Gráfico horizontal

    # Etiquetas y estilo
    plt.xlabel("Cantidad", fontsize=12)
    plt.ylabel(variable, fontsize=12)
    plt.title(f"Distribución de {variable} (Total: {total})", fontsize=14) #concateno en el titulo el total de la muestra
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    
    # Añadir etiquetas de porcentaje en las barras
    for index, row in dfAg.iterrows():
        plt.text(row["Cantidad"] + 0.5,  # Posición a la derecha de la barra
                 index,                  # Posición en el eje y
                 f'{row["Cantidad"]} ({row["Porcentaje"]:.1f}%)',  # Concatenar cantidad y porcentaje, porcentaje se formate 
                 va='center', ha='left', fontsize=10)

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)


#alternativa sin valores sin Info
def grafico_barras_sinInfo(df, variable):
    """
    Función para crear un gráfico de barras horizontales.
    Si la variable es numérica, se agrupa en rangos específicos.
    """
    dfFiltrado = df[(df[variable] != "sin info") & df[variable].notna()].copy()  # 🚀 Evita el Warning de pandas

    if dfFiltrado.empty:
        st.warning(f"No hay datos para mostrar en {variable} después de filtrar 'sin info'.")
        return

    # 📌 Verificar si la variable es numérica
    if pd.api.types.is_numeric_dtype(dfFiltrado[variable]):
        # Si es numérica, agrupar en bins según la variable
        if variable == "EdadProm":
            bins = [17, 21, 26, 31, 36, 41, 45, 50, 55, 60, 100]
            labels = ["17-20", "21-25", "26-30", "31-35", "36-40", "41-44", "45-49", "50-54", "55-59", "60+"]
            
        elif variable == "Ingresos Prom":
            bins = [   0,     75,          400,     750,             1500,2001, float("inf")]
            labels = ["0-74", "74-399",  "400-749", "750-1499", "1500-2000", "2000+"]

        else:
            bins = None

        if bins:
            dfFiltrado["Rangos"] = pd.cut(dfFiltrado[variable], bins=bins, labels=labels, right=False)
            variable = "Rangos"  # Se usa la columna con rangos

            # 🚀 Validación de los valores en los bins
            st.write("Conteo de datos por bin:")
            st.write(dfFiltrado["Rangos"].value_counts())

    # Agrupar valores
    dfAg = dfFiltrado[variable].value_counts().reset_index()
    dfAg.columns = [variable, "Cantidad"]

    # 🔍 Asegurar que los valores de los bins no sean NaN
    dfAg = dfAg.dropna()

    total = dfFiltrado[variable].count()
    dfAg["Porcentaje"] = (dfAg["Cantidad"] / total) * 100  

    # Ordenar si es una variable categórica
    if variable == "Rangos":
        dfAg[variable] = pd.Categorical(dfAg[variable], categories=labels, ordered=True)
        #dfAg = dfAg.sort_values(by=variable)

    # 🚀 Validación en consola- para ver las tablas q arman los graficos
    #st.write("Datos para la gráfica:")
    #st.write(dfAg)

    # Configuración del gráfico
    plt.figure(figsize=(8, 5))
    sns.barplot(data=dfAg, x="Cantidad", y=variable, palette="pastel")  

    # Etiquetas y estilo
    plt.xlabel("Cantidad", fontsize=12)
    plt.ylabel(variable, fontsize=12)
    plt.title(f"Distribución de {variable} (Total: {total})", fontsize=14)
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    # Añadir etiquetas de porcentaje en las barras
    for index, row in dfAg.iterrows():
        plt.text(row["Cantidad"] + 0.5, row[variable],  # <- CAMBIO AQUÍ
             f'{row["Cantidad"]} ({row["Porcentaje"]:.1f}%)', 
             va='center', ha='left', fontsize=10)

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)
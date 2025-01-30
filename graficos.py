import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def grafico_barras(df, variable):
    """
    Función para crear un gráfico de barras horizontales.
    Este tipo de Comentarios Doctrings se usan dentro de clases o funciones, si no se entienden como strings
    """
    dfAg = df[variable].value_counts().reset_index()
    dfAg.columns = [variable, "Cantidad"]  
    total = df[variable].count()
    dfAg["Porcentaje"] = (dfAg["Cantidad"] / total) * 100  # Calcula el porcentaje

    # Configuración del gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dfAg, x="Cantidad", y=variable, palette="pastel")  # Gráfico horizontal

    # Etiquetas y estilo
    plt.xlabel("Cantidad", fontsize=12)
    plt.ylabel(variable, fontsize=12)
    plt.title(f"Distribución de {variable}", fontsize=14)
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    
    # Añadir etiquetas de porcentaje en las barras
    for index, row in dfAg.iterrows():
        plt.text(row["Cantidad"] + 0.5,  # Posición a la derecha de la barra
                 index,                  # Posición en el eje y
                 f'{row["Porcentaje"]:.1f}%', 
                 va='center', ha='left', fontsize=10)

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

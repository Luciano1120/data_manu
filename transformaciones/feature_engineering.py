import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def aplicar_pca(df, n_componentes):
    """
    Aplica PCA (PCA aplica solo a variables numéricas, pero las categóricas fueron convertidas a numéricas en el OHE).

    Parámetros:
    - df: DataFrame ya con encoding (todas las variables deben ser numéricas).
    - n_componentes: Número de componentes principales a conservar.

    Retorna:
    - df_pca: DataFrame con los componentes principales.
    - modelo_pca: Modelo PCA ajustado.
    """
    # Comprobar si hay valores nulos en el DataFrame
    if df.isnull().sum().sum() > 0:
        print("Atención: Hay valores nulos en el DataFrame. Se procederá a imputarlos o eliminarlos.")
        # Eliminar filas con NaN (también podrías imputar si es necesario)
        df = df.dropna()

    # Asegurarse de que todas las columnas sean numéricas
    if not all(pd.api.types.is_numeric_dtype(df[col]) for col in df.columns):
        print("Atención: Hay columnas no numéricas. Asegúrate de que todas las columnas sean numéricas antes de aplicar PCA.")
        return None, None  # Si hay columnas no numéricas, retornar None para indicar error.

    # Estandarizar las variables (PCA es sensible a las escalas)
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # Aplicar PCA
    pca = PCA(n_components=n_componentes)
    pca_resultado = pca.fit_transform(df_scaled)

    # Crear DataFrame con los componentes principales
    df_pca = pd.DataFrame(pca_resultado, columns=[f"PC{i+1}" for i in range(n_componentes)])

    return df_pca, pca
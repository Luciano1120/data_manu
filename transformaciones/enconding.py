import pandas as pd
from sklearn.preprocessing import LabelEncoder

def enconding(df):
    """
    Aplica transformación a las variables categóricas del dataset.
    - Label Encoding para variables con orden.
    - One-Hot Encoding para variables sin orden.
    """

    
    # 🔹 Label Encoding para variables con orden
    le = LabelEncoder()
    df["Estudios"] = le.fit_transform(df["Estudios"])  

    # 🔹 One-Hot Encoding para variables sin orden
    df = pd.get_dummies(df, columns=["Sosten Economico","Conocimiento Importaciones","Tiempo Disponible en el Dia", "Tiempo dispuesto a Invertir Meses","Situacion Laboral M","comproCursoAnterior"], drop_first=True)
    # a esta variable "Info Ingresos" podría haberle hecho algun mapeo Manual, pero un OHE le queda bien tambien, aunq la estoy dejando afuera, dado q no puedo poner variables acá q no voy a pasar para la funcion enconding en() de debug.py
    
    # Alternativa Crear una nueva variable combinada de compromiso temporal
    #df["Compromiso_Temporal"] = df["Tiempo Disponible en el Dia"] * df["Tiempo dispuesto a Invertir Meses"]



    # Convertir columnas booleanas a 0 y 1
    boolean_columns = df.select_dtypes(include=[bool]).columns  # Seleccionar solo columnas booleanas
    df[boolean_columns] = df[boolean_columns].astype(int)  # Convertirlas a 0 y 1


    return df
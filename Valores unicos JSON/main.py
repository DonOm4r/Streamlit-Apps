import pandas as pd
import streamlit as st
import json

st.title("Convertir CSV a JSON")

# Permitir la carga de múltiples archivos
uploaded_files = st.file_uploader("Elige los archivos CSV", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Leer archivo CSV
        df = pd.read_csv(uploaded_file, sep=";")
        
        # Obtener columnas únicas
        unique_cols = df.columns.tolist()
        
        # Diccionario para almacenar valores únicos
        unique_values = {}
        
        # Extraer valores únicos por columna
        for col in unique_cols:
            unique_values[col] = df[col].unique().tolist()
        
        # Convertir a JSON
        json_data = unique_values
        
        # Mostrar JSON
        st.write(f"JSON para {uploaded_file.name}:")
        st.json(json_data)
        
        # Descargar JSON
        json_str = json.dumps(json_data, indent=4)
        st.download_button(
            label=f"Descargar {uploaded_file.name.replace('.csv', '.json')}",
            data=json_str,
            file_name=f"{uploaded_file.name.replace('.csv', '.json')}"
        )
        
    st.success("Todos los archivos han sido procesados")

else:
    st.warning("Por favor, carga al menos un archivo CSV.")
        
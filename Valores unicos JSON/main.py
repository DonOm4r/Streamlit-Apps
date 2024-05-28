import pandas as pd
import streamlit as st
import json
import zipfile
import io

st.title("Convertir CSV a JSON")

# Permitir la carga de múltiples archivos
uploaded_files = st.file_uploader("Elige los archivos CSV", accept_multiple_files=True)

if uploaded_files:
    # Diccionario para almacenar JSONs
    all_jsons = {}

    for uploaded_file in uploaded_files:
        # Leer archivo CSV
        df = pd.read_csv(uploaded_file)
        
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
        
        # Agregar JSON al diccionario
        all_jsons[uploaded_file.name.replace('.csv', '.json')] = json_data
        
        # Descargar JSON individual
        json_str = json.dumps(json_data, indent=4)
        st.download_button(
            label=f"Descargar {uploaded_file.name.replace('.csv', '.json')}",
            data=json_str,
            file_name=f"{uploaded_file.name.replace('.csv', '.json')}"
        )
        
    # Crear archivo ZIP con todos los JSONs
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for filename, data in all_jsons.items():
            zip_file.writestr(filename, json.dumps(data, indent=4))
    
    # Descargar archivo ZIP
    st.download_button(
        label="Descargar todos los JSONs",
        data=zip_buffer.getvalue(),
        file_name="LOS YEISONS.zip",
        mime="application/zip"
    )
        
    st.success("Todos los archivos han sido procesados")

else:
    st.warning("Por favor, carga al menos un archivo CSV.")

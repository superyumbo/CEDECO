"""
Archivo principal de la aplicación Streamlit para el análisis de datos CEDECO.
Este archivo inicializa la aplicación y gestiona la navegación entre páginas.
"""

import streamlit as st
import pandas as pd
import os

# Importar módulos de páginas
from utils.load_data import load_data, load_sample_data
from pages.home import show_home_page
from pages.basic_info import show_basic_info
from pages.infrastructure import show_infrastructure
from pages.history import show_history_participation
from pages.technology import show_technology
from pages.financing import show_financing
from pages.population import show_population
from pages.activities import show_activities
from pages.development import show_development_potential

# Configuración de la página
st.set_page_config(
    page_title="CEDECO - Análisis de Datos",
    page_icon="🍽️",
    layout="wide",
)

# Estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2563EB;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .subsection-header {
        font-size: 1.4rem;
        color: #3B82F6;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .highlight {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .conclusion {
        background-color: #E0F2FE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.3rem solid #0284C7;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal que controla el flujo de la aplicación"""
    
    # Título principal
    st.markdown('<div class="main-header">CEDECO - Centro de Desarrollo Comunitario</div>', unsafe_allow_html=True)
    st.markdown('Dashboard para análisis de comedores comunitarios y su potencial como centros de desarrollo')
    
    # Verificar existencia del archivo de credenciales
    if not os.path.exists('credentials.json'):
        st.error("El archivo de credenciales 'credentials.json' no se encuentra en la carpeta del proyecto.")
        st.info("""
        Para conectarse a Google Sheets, se necesita un archivo de credenciales. Por favor:
        1. Asegúrate de que el archivo 'credentials.json' está en la misma carpeta que el archivo main.py
        2. Verifica que las credenciales tienen permisos para acceder a la hoja de cálculo de CEDECO
        
        Mientras tanto, se mostrarán datos de ejemplo para demostración.
        """)
        df = load_sample_data()
    else:
        # Cargar datos
        df = load_data()
        if df is None:
            st.warning("Se están utilizando datos de ejemplo para demostración.")
            df = load_sample_data()
    
    # Menú lateral
    section = st.sidebar.radio(
        "Selecciona una sección para analizar:",
        ["Inicio", 
         "Información Básica", 
         "Infraestructura y Funcionamiento", 
         "Historia y Participación",
         "Uso de Tecnología y Comunicación",
         "Financiación y Dificultades",
         "Población Atendida",
         "Actividades Realizadas",
         "Potencial como Centro de Desarrollo"]
    )
    
    # Navegación a la página seleccionada
    if section == "Inicio":
        show_home_page()
    elif section == "Información Básica":
        show_basic_info(df)
    elif section == "Infraestructura y Funcionamiento":
        show_infrastructure(df)
    elif section == "Historia y Participación":
        show_history_participation(df)
    elif section == "Uso de Tecnología y Comunicación":
        show_technology(df)
    elif section == "Financiación y Dificultades":
        show_financing(df)
    elif section == "Población Atendida":
        show_population(df)
    elif section == "Actividades Realizadas":
        show_activities(df)
    elif section == "Potencial como Centro de Desarrollo":
        show_development_potential(df)
    
    # Pie de página
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Acerca de la aplicación")
    st.sidebar.info("Desarrollado para el proyecto CEDECO © 2025")
    st.sidebar.markdown("[Documentación](https://github.com/tu-usuario/cedeco-app)")

if __name__ == "__main__":
    main()
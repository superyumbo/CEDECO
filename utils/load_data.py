"""
Módulo para la carga de datos desde archivos Excel o Google Sheets.
"""

import streamlit as st
import pandas as pd
import gspread
import json
import os
from google.oauth2.service_account import Credentials
import openpyxl

def load_data():
    """
    Carga los datos desde Google Sheets o archivo Excel.
    
    Returns:
        pandas.DataFrame: Dataframe con los datos cargados.
    """
    
    # Intentar cargar datos desde Google Sheets primero
    try:
        # Verificar si hay credenciales de Streamlit Cloud
        if 'gcp_service_account' in st.secrets:
            # Configurar credenciales desde secretos de Streamlit
            credentials_info = st.secrets["gcp_service_account"]
            spreadsheet_id = st.secrets["sheets"]["spreadsheet_id"]
            
            # Configurar credenciales
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_info(credentials_info, scopes=scope)
            client = gspread.authorize(creds)
            
            # Abrir la hoja
            spreadsheet = client.open_by_key(spreadsheet_id)
            
            # Obtener hojas disponibles
            sheet_names = [sheet.title for sheet in spreadsheet.worksheets()]
            
            # Cargar la hoja CEDECO
            if 'CEDECO' in sheet_names:
                sheet = spreadsheet.worksheet('CEDECO')
                data = sheet.get_all_records()
                return pd.DataFrame(data)
    except Exception as e:
        # Silenciosamente pasar al siguiente método si falla
        pass
    
    # Intentar usar archivo credentials.json para Google Sheets
    try:
        if os.path.exists('credentials.json'):
            # Configurar credenciales
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
            client = gspread.authorize(creds)
            
            # Abrir la hoja
            spreadsheet = client.open_by_key('1n7f_BWmVmdfvE75_HFf2az0DFGQUAMxqca-zEB91X-A')
            
            # Obtener hojas disponibles
            sheet_names = [sheet.title for sheet in spreadsheet.worksheets()]
            
            # Cargar la hoja CEDECO
            if 'CEDECO' in sheet_names:
                sheet = spreadsheet.worksheet('CEDECO')
                data = sheet.get_all_records()
                return pd.DataFrame(data)
    except Exception as e:
        # Silenciosamente pasar al siguiente método si falla
        pass
    
    # Intentar cargar directamente desde archivo Excel
    try:
        # Verificar varios nombres posibles de archivo Excel
        excel_files = ['CEDECO.xlsx', 'CEDECO 2.xlsx', 'data/CEDECO.xlsx', 'data/CEDECO 2.xlsx']
        
        for file in excel_files:
            if os.path.exists(file):
                # Cargar datos de Excel
                return pd.read_excel(file)
    except Exception as e:
        # Silenciosamente pasar al siguiente método si falla
        pass
    
    # Si llegamos aquí, creamos un DataFrame vacío con las columnas esperadas
    # para evitar errores en el resto de la aplicación
    empty_df = pd.DataFrame({
        'ID': [],
        'FECHA': [],
        'NOMBRE_COMEDOR': [],
        'NOMBER_GESTORA': [],
        'TELEFONO1': [],
        'DIRECCION': [],
        'COMUNA': [],
        'BARRIO': [],
        'NODO': [],
        'NICHO': [],
        'PREFESIONAL_REALIZA_VISITA': [],
        'LUGAR_DONDE_FUNCIONA_COMEDOR': [],
        'ESPACIO_TALLERES': [],
        'ARTICULACION_CON_ORGANIZACIONES': [],
        'HISTORIA_COMEDOR': [],
        'PARTICIPACION_ACTIVIDADES': [],
        'USO_DE_TIC': [],
        'QUE_REDES': [],
        'HA_TENIDO_DIFICULTADES': [],
        'FINANCIACION_ACTIVIDADES': [],
        'POBLACION_PRINCIPAL_COMEDOR': [],
        'ETAPA_VITAL': [],
        'BENEFICIARIOS_SON_MISMOS_QUE_REALIZA_LABORA_SOCIAL': [],
        'ACCIONES_PUNTUALES_COMEDOR': [],
        'VINCULACION_OTROS_ACTORES': [],
        'SEGUIMIENTO_EVALUACION_A_OTRAS_ACTIVIDADES': [],
        'INICIATIVA_HUERTAS': [],
        'INTERESADO_COMO_CENTRO_DESARROLLO': [],
        'NECESIDADES_QUE_SE_APOYARAN': [],
        'USER': [],
        'NOMBRE': [],
        'UBICACION': [],
        'Observaciones1': [],
        'Observaciones2': [],
        'OBSERVACIONES_ALIANZAS_ESTRATEGICAS': [],
        'OBSERVACIONES_AREA_FINANCIAMIENTO': [],
        'OBSERVACIONES_CAPACITACION_INTEGRAL': [],
        'OBSERVACIONES_VISIBILIDAD_RECONOCIMIENTO': [],
        'OBSERVACIONES_PROCESOS_PLANIFICACIONES': [],
        'RECURSO_HUMANO_CON_EL_QUE_CUENTA': [],
        'OBSERVACIONES': [],
    })
    
    return empty_df
"""
Módulo para la carga de datos desde Google Sheets o datos de ejemplo.
"""

import streamlit as st
import pandas as pd
import gspread
import json
import os
from google.oauth2.service_account import Credentials

def load_data():
    """
    Carga los datos desde Google Sheets usando las credenciales proporcionadas.
    
    Returns:
        pandas.DataFrame: Dataframe con los datos cargados o None si hay error.
    """
    
    # Mostrar un spinner mientras se cargan los datos
    with st.spinner("Cargando datos desde Google Sheets..."):
        try:
            # Intentar usar secretos de Streamlit Cloud primero
            if 'gcp_service_account' in st.secrets:
                st.info("Usando credenciales desde Streamlit Secrets")
                # Usar credenciales directamente desde los secretos de Streamlit
                credentials_info = st.secrets["gcp_service_account"]
                spreadsheet_id = st.secrets["sheets"]["spreadsheet_id"]
                
                # Configurar credenciales
                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                creds = Credentials.from_service_account_info(credentials_info, scopes=scope)
                client = gspread.authorize(creds)
                
                # Abrir la hoja
                spreadsheet = client.open_by_key(spreadsheet_id)
            else:
                st.info("Intentando usar credenciales locales")
                # Alternativa: usar archivo credentials.json local
                credentials_path = 'credentials.json'
                
                # Verificar si el archivo existe
                if not os.path.exists(credentials_path):
                    st.error(f"No se encontró el archivo de credenciales en {credentials_path} y no se configuraron secretos en Streamlit")
                    return None
                
                # Configurar credenciales
                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
                client = gspread.authorize(creds)
                
                # Abrir la hoja
                spreadsheet = client.open_by_key('1n7f_BWmVmdfvE75_HFf2az0DFGQUAMxqca-zEB91X-A')
            
            # Obtener todas las hojas disponibles
            sheet_names = [sheet.title for sheet in spreadsheet.worksheets()]
            st.success(f"Conexión establecida. Hojas disponibles: {', '.join(sheet_names)}")
            
            # Cargar la hoja CEDECO
            if 'CEDECO' in sheet_names:
                sheet = spreadsheet.worksheet('CEDECO')
                data = sheet.get_all_records()
                df_cedeco = pd.DataFrame(data)
                
                # Si el dataframe está vacío, cargar datos de ejemplo
                if df_cedeco.empty:
                    st.warning("La hoja CEDECO está vacía. Se cargarán datos de ejemplo para demostración.")
                    df_cedeco = load_sample_data()
                else:
                    st.success(f"Datos cargados correctamente: {len(df_cedeco)} registros encontrados.")
                
                return df_cedeco
            else:
                st.warning("No se encontró la hoja CEDECO. Se cargarán datos de ejemplo para demostración.")
                return load_sample_data()
            
        except Exception as e:
            st.error(f"Error al cargar datos desde Google Sheets: {str(e)}")
            st.info("Cargando datos de ejemplo como alternativa...")
            return load_sample_data()

def load_sample_data():
    """
    Carga datos de ejemplo para demostración en caso de fallo con Google Sheets.
    
    Returns:
        pandas.DataFrame: Dataframe con datos de ejemplo.
    """
    # Datos de muestra basados en el análisis previo del archivo CEDECO 2.xlsx
    data = {
        'ID': ['b7d94891', 'a4f40e35', 'ea8c61c7', '94787d85', '94787d86'],
        'FECHA': ['13/05/2025', '13/05/2025', '12/05/2025', '12/05/2025', '14/05/2025'],
        'NOMBRE_COMEDOR': ['MANOS QUE DAN', 'FUNDAGOL', 'EL PEROL POR LA PAZ', 'ASOPANID', 'EL PAN DE DIOS'],
        'NOMBER_GESTORA': ['LUZ ALBA COSME', 'LORENA', 'ERLENDY CUERO BRAVO', 'EUCARIS RAMIREZ', 'DORA GIL'],
        'TELEFONO1': ['3007715731', '', '', '', '3184556180'],
        'DIRECCION': ['CA 18A VDA GUAYACANES', 'CORREGIMIENTO GOLONDRINAS', 'CL 56I # 47 A 18', 'CR 17 # 13A-67', 'CLL 78C ·23C- 81 (TALLERES) – CLL 80 ·23-49'],
        'COMUNA': ['19', '65', '15', '9', '21'],
        'BARRIO': ['PARCELACION LOS MANGOS', 'CABECERA CASA 4', 'LLANO VERDE', 'GUAYAQUIL', 'VALLEGRANDE'],
        'NODO': ['12', '1', '8', '3', '15'],
        'NICHO': ['1', '3', '3', '2', '5'],
        'PREFESIONAL_REALIZA_VISITA': ['PAULINA ROJAS REYES', 'OCTAVIO GARCIA', 'NELMY BENITEZ', 'NELMY BENITEZ', 'JEMIMA PARRA'],
        'LUGAR_DONDE_FUNCIONA_COMEDOR': ['A. VIVIENDA DE UNA DE LAS/OS GESTORAS/ES', 'C. INSTITUCIÓN (FUNDACIÓN, IGLESIA, ETC.) QUE AVALA EL COMEDOR', 'B. LOCAL COMERCIAL EN ALQUILER', 'A. VIVIENDA DE UNA DE LAS/OS GESTORAS/ES', 'C. INSTITUCIÓN (FUNDACIÓN, IGLESIA, ETC.) QUE AVALA EL COMEDOR'],
        'ESPACIO_TALLERES': ['SI', 'SI', 'NO', 'SI', 'SI'],
        'ARTICULACION_CON_ORGANIZACIONES': ['SI', 'SI', 'SI', 'SI', 'SI'],
        'HISTORIA_COMEDOR': ['SI', 'SI', 'SI', 'SI', 'SI'],
        'PARTICIPACION_ACTIVIDADES': ['SI', 'SI', 'SI', 'SI', 'SI'],
        'USO_DE_TIC': ['REDES SOCIALES', 'REDES SOCIALES', 'REDES SOCIALES', 'CORREO ELECTRÓNICO; REDES SOCIALES', ''],
        'QUE_REDES': ['FACEBOOK, WHATSAPP', 'FACEBOOK, INSTAGRAM', '', 'FACEBOOK, WHATSAPP', ''],
        'HA_TENIDO_DIFICULTADES': ['NO', 'NO', 'NO', '', ''],
        'FINANCIACION_ACTIVIDADES': ['DONACIONES, RECURSOS PROPIOS', 'RECURSOS PROPIOS', 'DONACIONES, RECURSOS PROPIOS', 'OTRA', 'DONACIONES, RECURSOS PROPIOS'],
        'POBLACION_PRINCIPAL_COMEDOR': ['NEGRO(A), MULATO(A), AFRODESCENDIENTE, AFROCOLOMBIANO(A)', 'OTRO', 'NEGRO(A), MULATO(A), AFRODESCENDIENTE, AFROCOLOMBIANO(A)', 'MESTIZA', 'NINGÚN GRUPO ÉTNICO'],
        'ETAPA_VITAL': ['PERSONAS MAYORES (60 AÑOS Y MÁS)', '', 'INFANCIA (6-11 AÑOS), ADOLESCENTES (12-18 AÑOS), ADULTOS/AS (29-59 AÑOS)', '', 'PERSONAS MAYORES (60 AÑOS Y MÁS)'],
        'BENEFICIARIOS_SON_MISMOS_QUE_REALIZA_LABORA_SOCIAL': ['SI', 'SI', 'SI', 'SI', 'SI'],
        'ACCIONES_PUNTUALES_COMEDOR': ['A. REALIZACIÓN DE TALLERES O ESPACIOS FORMATIVOS. B. EJECUCIÓN DE ACTIVIDADES LÚDICO-RECREATIVAS. C. ARTICULACIÓN CON ENTIDADES. D. SOCIALIZACIÓN DE RUTAS DE ATENCIÓN.',
                                         'A. REALIZACIÓN DE TALLERES O ESPACIOS FORMATIVOS. D. SOCIALIZACIÓN DE RUTAS DE ATENCIÓN. E. PROMUEVE DONACIONES. H. OLLA COMUNITARIA.',
                                         'A. REALIZACIÓN DE TALLERES O ESPACIOS FORMATIVOS. B. EJECUCIÓN DE ACTIVIDADES LÚDICO-RECREATIVAS. C. ARTICULACIÓN CON ENTIDADES. F. DENUNCIAS FORMALES.',
                                         '',
                                         'A. REALIZACIÓN DE TALLERES O ESPACIOS FORMATIVOS. M. CELEBRACIÓN DE FECHAS ESPECIALES.'],
        'VINCULACION_OTROS_ACTORES': ['SIEMPRE', 'EN OCASIONES', 'SIEMPRE', '', ''],
        'SEGUIMIENTO_EVALUACION_A_OTRAS_ACTIVIDADES': ['SI', 'NO', 'SI', '', ''],
        'INICIATIVA_HUERTAS': ['NO', 'SI', 'SI', '', 'NO'],
        'INTERESADO_COMO_CENTRO_DESARROLLO': ['SI', 'SI', 'SI', 'SI', 'SI'],
        'NECESIDADES_QUE_SE_APOYARAN': ['OTRA', 'GESTION DE ALIANZAS ESTRATEGICAS, AREA DE FINANCIAMIENTO, CAPACITACION Y FORMACION INTEGRAL', 'GESTIÓN DE ALIANZAS ESTRATÉGICAS, ÁREA DE FINANCIAMIENTO, CAPACITACIÓN Y FORMACIÓN INTEGRAL', '', ''],
        'USER': ['paulinareyro@gmail.com', 'tavogarbe@gmail.com', 'nelmybenitezpino@gmail.com', 'nelmybenitezpino@gmail.com', 'trabajosocialpsexodo@arquicali.org'],
        'NOMBRE': ['PAULINA ROJAS REYES', 'OCTAVIO GARCIA', 'NELMY BENITEZ', 'NELMY BENITEZ', 'JEMIMA PARRA'],
        'UBICACION': ['3.412768, -76.570213', '3.499194, -76.550501', '3.392992, -76.505671', '3.441389, -76.527061', ''],
        'Observaciones1': ['Hace 6 años inicie en el comedor, desde hace 16 años trabajo por la comunidad. Di inicio a mi labor desde la generación de espacios religiosos, soy cristiana, a partir de mi trabajo con la iglesia empecé mi labor social.', 
                          'La gestora principal manifiesta que trabaja con la comunidad del corregimiento, población de adulto mayor, que viven muy solos.', 
                          'La iniciativa nace desde su hijo Álvaro en el año 1996, el cual cuenta con una condición especial (síndrome de down), buscó estrategias para poder implementar y visibilizar la comunidad con discapacidad.',
                          'Desde el año 2007, desde Comfenalco se empezaron a dar talleres de liderazgo en el barrio donde ella identificó que tiene habilidades para aportar a la comunidad.',
                          ''],
        'Observaciones2': ['He sido participe de las retribuciones sociales, el año pasado tuvimos buena acogida por parte de la comunidad y de los participantes.',
                          'A todas las reuniones convocadas, como jornadas de autocuidado, talleres y capacitaciones.',
                          'Reuniones por nodo, no va a la reunión generales que se realizan, representa comunidades Afro',
                          'Participa en espacios de formación y educación para personas con condiciones especiales (síndrome de down)',
                          'Desde el año 2018 ha participado en todas las capacitaciones, retribuciones con el programa y feria de servicios'],
        'OBSERVACIONES_ALIANZAS_ESTRATEGICAS': ['RED DE APOYO SOCIAL (AMIGOS, VECINOS), RED DE APOYO FAMILIAR, RED DE APOYO DE COLABORADORES PROPIOS DEL COMEDOR O FUNDACIÓN',
                                              'Tener más acceso a las estrategias de la alcaldía para la comunidad',
                                              'Docentes y formadores',
                                              '',
                                              ''],
        'OBSERVACIONES_AREA_FINANCIAMIENTO': ['Emprendimiento para la población del comedor a través de educación',
                                            'Donación de sillas y mesas. Pago a formadores.',
                                            '',
                                            '',
                                            ''],
        'OBSERVACIONES_CAPACITACION_INTEGRAL': ['La gestora expresa contar con un apoyo significativo con su red de apoyo familiar, representada en su hija quien cuenta con formación profesional.',
                                              'Capacitación en emprendimientos',
                                              'Capacitación en el manejo financiero de la fundación.',
                                              '',
                                              ''],
        'OBSERVACIONES_VISIBILIDAD_RECONOCIMIENTO': ['Reconocimiento de la comunidad viven de la minería ilegal',
                                                   '',
                                                   '',
                                                   '',
                                                   ''],
        'OBSERVACIONES_PROCESOS_PLANIFICACIONES': ['Ella requiere se le asesore para tener una mayor planificación de las actividades',
                                                 '',
                                                 '',
                                                 '',
                                                 ''],
        'RECURSO_HUMANO_CON_EL_QUE_CUENTA': ['RED DE APOYO DE VOLUNTARIADO',
                                           'RED DE APOYO SOCIAL (AMIGOS, VECINOS), RED DE APOYO FAMILIAR, RED DE APOYO DE VOLUNTARIADO',
                                           'RED DE APOYO SOCIAL (AMIGOS, VECINOS), RED DE APOYO DE COLABORADORES PROPIOS DEL COMEDOR O FUNDACIÓN',
                                           '',
                                           ''],
        'OBSERVACIONES': ['La gestora es fisioterapeuta y desarrolla actividades de voluntariado con la comunidad',
                        'Ampliar cupo de oferta para diferentes beneficiarios sin sesgo de edad (21 años en adelante) ya que también se trabajan con adultos mayores.',
                        'La gestora requiere apoyo en el fortalecimiento de los ejes que desarrolla mediante personal para los espacios formativos, insumos, materiales de funcionamiento.',
                        '',
                        ''],
    }
    
    st.success("Datos de ejemplo cargados correctamente.")
    return pd.DataFrame(data)
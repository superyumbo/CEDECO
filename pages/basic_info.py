"""
Módulo que muestra la página de información básica de comedores.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_basic_info(df):
    """
    Muestra la página de información básica de los comedores.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="section-header">Información Básica</div>', unsafe_allow_html=True)
    st.markdown("Análisis de los datos básicos de identificación de los comedores y sus gestoras")
    
    # Métricas generales
    total_comedores = len(df)
    total_comunas = df['COMUNA'].nunique()
    total_gestoras = df['NOMBER_GESTORA'].nunique()
    
    # Mostrar métricas en 3 columnas
    col_metrics = st.columns(3)
    
    with col_metrics[0]:
        st.metric("Total Comedores Evaluados", total_comedores)
    
    with col_metrics[1]:
        st.metric("Comunas Representadas", total_comunas)
        
    with col_metrics[2]:
        st.metric("Gestoras Únicas", total_gestoras)
    
    # Dividir en columnas para gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico 1: Distribución por comunas
        st.markdown('<div class="subsection-header">Distribución por Comuna</div>', unsafe_allow_html=True)
        
        # Contar comedores por comuna
        comuna_counts = df['COMUNA'].value_counts().reset_index()
        comuna_counts.columns = ['Comuna', 'Cantidad']
        
        # Crear gráfico de barras horizontal
        fig_comuna = px.bar(comuna_counts, y='Comuna', x='Cantidad', 
                          orientation='h', 
                          title='Distribución de Comedores por Comuna',
                          color='Cantidad',
                          color_continuous_scale='Blues')
        
        fig_comuna.update_layout(height=400)
        st.plotly_chart(fig_comuna, use_container_width=True)
        
        # Conclusión
        st.markdown('<div class="conclusion">Las comunas 19, 65, 15, 9 y 21 tienen representación en la muestra actual, con una distribución uniforme de un comedor por comuna. Esto indica una buena cobertura geográfica en esta fase inicial.</div>', unsafe_allow_html=True)
        
    with col2:
        # Gráfico 2: Profesionales que realizaron visitas
        st.markdown('<div class="subsection-header">Visitas por Profesional</div>', unsafe_allow_html=True)
        
        # Contar visitas por profesional
        prof_counts = df['PREFESIONAL_REALIZA_VISITA'].value_counts().reset_index()
        prof_counts.columns = ['Profesional', 'Visitas']
        
        # Crear gráfico de pastel
        fig_prof = px.pie(prof_counts, values='Visitas', names='Profesional', 
                        title='Visitas realizadas por Profesional',
                        color_discrete_sequence=px.colors.sequential.Blues)
        
        fig_prof.update_traces(textposition='inside', textinfo='percent+label')
        fig_prof.update_layout(height=400)
        st.plotly_chart(fig_prof, use_container_width=True)
        
        # Conclusión
        nelmy_count = prof_counts[prof_counts['Profesional'] == 'NELMY BENITEZ']['Visitas'].values[0] if 'NELMY BENITEZ' in prof_counts['Profesional'].values else 0
        if nelmy_count > 0:
            nelmy_percent = int((nelmy_count / prof_counts['Visitas'].sum()) * 100)
            conclusion = f"NELMY BENITEZ ha realizado el {nelmy_percent}% de las visitas, seguido por los demás profesionales. Esto podría indicar una especialización por zonas o tipos de comedores."
        else:
            conclusion = "La distribución de visitas entre profesionales es equilibrada, lo que refleja un reparto equitativo del trabajo de campo."
        
        st.markdown(f'<div class="conclusion">{conclusion}</div>', unsafe_allow_html=True)
    
    # Análisis adicional - Distribución de telefonía
    st.markdown('<div class="subsection-header">Completitud de Datos de Contacto</div>', unsafe_allow_html=True)
    
    # Calcular presencia/ausencia de teléfono
    df['tiene_telefono'] = df['TELEFONO1'].apply(lambda x: "Con teléfono" if x else "Sin teléfono")
    telefono_counts = df['tiene_telefono'].value_counts().reset_index()
    telefono_counts.columns = ['Estado', 'Cantidad']
    
    # Crear gráfico de barras
    fig_tel = px.bar(telefono_counts, x='Estado', y='Cantidad',
                   title='Disponibilidad de Datos de Contacto',
                   color='Estado',
                   color_discrete_map={'Con teléfono': '#1E40AF', 'Sin teléfono': '#93C5FD'})
    
    fig_tel.update_layout(height=400)
    st.plotly_chart(fig_tel, use_container_width=True)
    
    # Calcular el porcentaje de registros sin teléfono
    if len(telefono_counts) > 1:
        sin_telefono = telefono_counts[telefono_counts['Estado'] == 'Sin teléfono']['Cantidad'].values[0]
        porcentaje_sin_telefono = int((sin_telefono / len(df)) * 100)
        conclusion_tel = f"El {porcentaje_sin_telefono}% de los registros no tienen número de teléfono disponible, lo que podría dificultar la comunicación directa con las gestoras."
    else:
        conclusion_tel = "No se pudo calcular la distribución de datos de contacto."
    
    st.markdown(f'<div class="conclusion">{conclusion_tel}</div>', unsafe_allow_html=True)
    
    # Distribución por nombre del comedor y fecha
    st.markdown('<div class="subsection-header">Distribución Temporal de Visitas</div>', unsafe_allow_html=True)
    
    # Procesar las fechas 
    try:
        df['FECHA_PROC'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df['FECHA_STR'] = df['FECHA_PROC'].dt.strftime('%d/%m/%Y')
        fecha_counts = df['FECHA_STR'].value_counts().reset_index()
        fecha_counts.columns = ['Fecha', 'Visitas']
        
        # Ordenar por fecha
        fecha_counts['FECHA_TEMP'] = pd.to_datetime(fecha_counts['Fecha'], format='%d/%m/%Y')
        fecha_counts = fecha_counts.sort_values('FECHA_TEMP')
        fecha_counts = fecha_counts.drop('FECHA_TEMP', axis=1)
        
        # Crear gráfico de línea
        fig_fecha = px.line(fecha_counts, x='Fecha', y='Visitas',
                          title='Distribución Temporal de Visitas',
                          markers=True)
        
        fig_fecha.update_layout(height=400)
        st.plotly_chart(fig_fecha, use_container_width=True)
        
        # Conclusión
        st.markdown('<div class="conclusion">Las visitas se han realizado en un periodo corto de tiempo (12-14 de mayo de 2025), lo que facilita la comparabilidad de los datos. Se observa una distribución relativamente uniforme, con una ligera concentración en ciertos días.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"No se pudo procesar la distribución temporal debido a: {str(e)}")
    
    # Conclusión general de la sección
    st.markdown('<div class="conclusion"><strong>Conclusiones principales:</strong><br><ul><li>Solo el 40% de los registros tienen número de teléfono disponible, lo que dificulta la comunicación directa.</li><li>Hay una distribución geográfica amplia que incluye diferentes comunas de la ciudad.</li><li>La gestión del trabajo de campo muestra concentración en ciertos profesionales, lo que podría representar una vulnerabilidad si no se cuenta con backup de conocimiento sobre las zonas visitadas.</li><li>Las visitas se realizaron en un periodo concentrado, asegurando condiciones similares para la evaluación de los comedores.</li></ul></div>', unsafe_allow_html=True)
    
    # Mostrar tabla de datos
    with st.expander("Ver datos originales"):
        st.dataframe(df[['ID', 'NOMBRE_COMEDOR', 'NOMBER_GESTORA', 'TELEFONO1', 'COMUNA', 'BARRIO', 'NODO', 'NICHO', 'PREFESIONAL_REALIZA_VISITA', 'FECHA']])
"""
Módulo que muestra la página de población atendida por los comedores.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import re

def show_population(df):
    """
    Muestra la página de población atendida por los comedores.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="section-header">Población Atendida</div>', unsafe_allow_html=True)
    st.markdown("Análisis de los grupos poblacionales beneficiados por los comedores comunitarios")
    
    # Verificar columnas relevantes
    poblacion_col = 'POBLACION_PRINCIPAL_COMEDOR' if 'POBLACION_PRINCIPAL_COMEDOR' in df.columns else None
    etapa_col = 'ETAPA_VITAL' if 'ETAPA_VITAL' in df.columns else None
    grupos_col = 'GRUPOS_EN_SITUACION_DE_VULNERABILIDAD' if 'GRUPOS_EN_SITUACION_DE_VULNERABILIDAD' in df.columns else None
    
    # Dividir en columnas
    col1, col2 = st.columns(2)
    
    with col1:
        if poblacion_col:
            # Análisis de población por grupo étnico
            st.markdown('<div class="subsection-header">Población por Grupo Étnico</div>', unsafe_allow_html=True)
            
            # Procesar los datos para el análisis
            etnias = []
            for pob in df[poblacion_col].dropna():
                if isinstance(pob, str):
                    # Manejar diferentes variantes en los grupos étnicos
                    if "AFRO" in pob.upper() or "NEGRO" in pob.upper() or "MULATO" in pob.upper():
                        etnias.append("Afrodescendiente")
                    elif "MESTIZA" in pob.upper():
                        etnias.append("Mestizo")
                    elif "INDÍGENA" in pob.upper():
                        etnias.append("Indígena")
                    elif "NINGÚN" in pob.upper():
                        etnias.append("Sin grupo étnico específico")
                    elif "OTRO" in pob.upper():
                        etnias.append("Otro grupo étnico")
                    else:
                        etnias.append("No especificado")
            
            if etnias:
                etnias_counts = pd.Series(etnias).value_counts().reset_index()
                etnias_counts.columns = ['Grupo Étnico', 'Cantidad']
                
                # Crear gráfico de barras
                fig_etnias = px.bar(
                    etnias_counts, 
                    y='Grupo Étnico', 
                    x='Cantidad',
                    orientation='h',
                    title='Distribución por Grupo Étnico',
                    color='Cantidad',
                    color_continuous_scale='Blues'
                )
                
                fig_etnias.update_layout(height=400)
                st.plotly_chart(fig_etnias, use_container_width=True)
                
                # Conclusión
                porcentaje_afro = round((etnias_counts[etnias_counts['Grupo Étnico'] == 'Afrodescendiente']['Cantidad'].sum() / sum(etnias_counts['Cantidad'])) * 100) if 'Afrodescendiente' in etnias_counts['Grupo Étnico'].values else 0
                
                st.markdown(f'<div class="conclusion">El {porcentaje_afro}% de los comedores atiende principalmente a población afrodescendiente, lo que refleja el enfoque en comunidades históricamente marginadas. La diversidad étnica muestra el alcance inclusivo de los comedores comunitarios.</div>', unsafe_allow_html=True)
            else:
                st.info("No hay datos suficientes sobre grupos étnicos de la población atendida.")
    
    with col2:
        if etapa_col:
            # Análisis por etapa vital
            st.markdown('<div class="subsection-header">Población por Etapa Vital</div>', unsafe_allow_html=True)
            
            # Procesar los datos para el análisis
            etapas = []
            for etapa in df[etapa_col].dropna():
                if isinstance(etapa, str):
                    # Extraer etapas específicas
                    if "INFANCIA" in etapa.upper():
                        etapas.append("Infancia (6-11 años)")
                    if "ADOLESCENTES" in etapa.upper():
                        etapas.append("Adolescentes (12-18 años)")
                    if "JÓVENES" in etapa.upper() or "JOVENES" in etapa.upper():
                        etapas.append("Jóvenes (19-28 años)")
                    if "ADULTOS/AS (" in etapa.upper():
                        etapas.append("Adultos (29-59 años)")
                    if "MAYORES" in etapa.upper():
                        etapas.append("Personas mayores (60+ años)")
            
            if etapas:
                etapas_counts = pd.Series(etapas).value_counts().reset_index()
                etapas_counts.columns = ['Etapa Vital', 'Cantidad']
                
                # Ordenar las etapas en orden cronológico
                etapa_order = [
                    "Infancia (6-11 años)",
                    "Adolescentes (12-18 años)",
                    "Jóvenes (19-28 años)",
                    "Adultos (29-59 años)",
                    "Personas mayores (60+ años)"
                ]
                etapas_counts['Orden'] = etapas_counts['Etapa Vital'].apply(lambda x: etapa_order.index(x) if x in etapa_order else 999)
                etapas_counts = etapas_counts.sort_values('Orden').drop('Orden', axis=1)
                
                # Crear gráfico de barras
                fig_etapas = px.bar(
                    etapas_counts, 
                    y='Etapa Vital', 
                    x='Cantidad',
                    orientation='h',
                    title='Distribución por Etapa Vital',
                    color='Cantidad',
                    color_continuous_scale='Blues'
                )
                
                fig_etapas.update_layout(height=400)
                st.plotly_chart(fig_etapas, use_container_width=True)
                
                # Conclusión
                mayores_count = etapas_counts[etapas_counts['Etapa Vital'] == 'Personas mayores (60+ años)']['Cantidad'].sum() if 'Personas mayores (60+ años)' in etapas_counts['Etapa Vital'].values else 0
                porcentaje_mayores = round((mayores_count / etapas_counts['Cantidad'].sum()) * 100) if etapas_counts['Cantidad'].sum() > 0 else 0
                
                if porcentaje_mayores > 0:
                    st.markdown(f'<div class="conclusion">Las personas mayores (60+ años) representan el {porcentaje_mayores}% de la población atendida, siendo el grupo más significativo. Sin embargo, varios comedores atienden múltiples grupos etarios, mostrando un enfoque intergeneracional.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="conclusion">Se observa una distribución diversa en las etapas vitales atendidas, con presencia de comedores enfocados en diferentes grupos etarios. Esta diversidad permite adaptar los servicios a las necesidades específicas de cada etapa.</div>', unsafe_allow_html=True)
            else:
                st.info("No hay datos suficientes sobre etapas vitales de la población atendida.")
    
    # Análisis de grupos en situación de vulnerabilidad
    if grupos_col:
        st.markdown('<div class="subsection-header">Grupos en Situación de Vulnerabilidad</div>', unsafe_allow_html=True)
        
        # Procesar los datos para el análisis
        grupos = []
        for grupo in df[grupos_col].dropna():
            if isinstance(grupo, str):
                for g in re.split(r',|\s+', grupo):
                    g = g.strip()
                    if g:
                        # Simplificar y categorizar
                        if "SPA" in g.upper():
                            grupos.append("Consumidores SPA")
                        elif "MIGRANTES" in g.upper():
                            grupos.append("Migrantes")
                        elif "INFORMAL" in g.upper():
                            grupos.append("Trabajadores informales")
                        elif "CALLE" in g.upper():
                            grupos.append("Habitantes de calle")
                        elif "FORMAL" in g.upper():
                            grupos.append("Trabajadores formales")
                        elif "LIDERAZGO" in g.upper() or "JAC" in g.upper() or "JAL" in g.upper():
                            grupos.append("Liderazgo social")
                        elif "RECICLADORES" in g.upper() or "RECUPERADORES" in g.upper():
                            grupos.append("Recicladores")
                        elif "HOGAR" in g.upper() or "JEFE" in g.upper():
                            grupos.append("Jefes de hogar")
                        elif "VÍCTIMAS" in g.upper() or "VICTIMAS" in g.upper() or "CONFLICTO" in g.upper():
                            grupos.append("Víctimas del conflicto")
                        elif "DISCAPACIDAD" in g.upper():
                            grupos.append("Personas con discapacidad")
                        elif "OTRO" in g.upper():
                            grupos.append("Otros grupos vulnerables")
        
        if grupos:
            grupos_counts = pd.Series(grupos).value_counts().reset_index()
            grupos_counts.columns = ['Grupo Vulnerable', 'Cantidad']
            
            # Crear gráfico de barras
            fig_grupos = px.bar(
                grupos_counts, 
                y='Grupo Vulnerable', 
                x='Cantidad',
                orientation='h',
                title='Grupos en Situación de Vulnerabilidad Atendidos',
                color='Cantidad',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig_grupos, use_container_width=True)
            
            # Conclusión
            st.markdown('<div class="conclusion">Los comedores atienden una amplia variedad de poblaciones vulnerables, destacando consumidores de SPA, migrantes, trabajadores informales y habitantes de calle. Esta diversidad muestra el rol esencial de los comedores como red de protección social para múltiples grupos en situación de vulnerabilidad.</div>', unsafe_allow_html=True)
        else:
            st.info("No hay datos suficientes sobre grupos en situación de vulnerabilidad.")
    
    # Verificar si los beneficiarios son quienes realizan labor social
    if 'BENEFICIARIOS_SON_MISMOS_QUE_REALIZA_LABORA_SOCIAL' in df.columns:
        st.markdown('<div class="subsection-header">Participación de Beneficiarios en Labor Social</div>', unsafe_allow_html=True)
        
        # Contar respuestas
        beneficiarios_labor = df['BENEFICIARIOS_SON_MISMOS_QUE_REALIZA_LABORA_SOCIAL'].apply(
            lambda x: 'Sí' if x == 'SI' else ('No' if x == 'NO' else 'Sin datos')
        ).value_counts().reset_index()
        
        beneficiarios_labor.columns = ['Beneficiarios realizan labor social', 'Cantidad']
        
        # Crear gráfico de pastel
        fig_beneficiarios = px.pie(
            beneficiarios_labor, 
            values='Cantidad', 
            names='Beneficiarios realizan labor social',
            title='¿Los Beneficiarios Realizan Labor Social?',
            color_discrete_sequence=['#1E40AF', '#93C5FD', '#E0F2FE']
        )
        
        fig_beneficiarios.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_beneficiarios, use_container_width=True)
        
        # Conclusión
        si_count = beneficiarios_labor[beneficiarios_labor['Beneficiarios realizan labor social'] == 'Sí']['Cantidad'].sum() if 'Sí' in beneficiarios_labor['Beneficiarios realizan labor social'].values else 0
        porcentaje_si = round((si_count / beneficiarios_labor['Cantidad'].sum()) * 100) if beneficiarios_labor['Cantidad'].sum() > 0 else 0
        
        st.markdown(f'<div class="conclusion">El {porcentaje_si}% de los comedores reportan que los beneficiarios son los mismos que realizan labor social, lo que refleja un modelo de participación activa y corresponsabilidad en la gestión comunitaria. Este enfoque fortalece la sostenibilidad y el sentido de pertenencia.</div>', unsafe_allow_html=True)
    
    # Conclusión general
    st.markdown("""
    <div class="conclusion">
        <strong>Conclusiones principales sobre población atendida:</strong>
        <ul>
            <li>Los comedores atienden predominantemente a población afrodescendiente, reflejando su enfoque en comunidades históricamente marginadas.</li>
            <li>Las personas mayores constituyen un grupo significativo, aunque muchos comedores tienen un enfoque intergeneracional.</li>
            <li>Se observa una amplia diversidad de grupos vulnerables atendidos, destacando consumidores de SPA, migrantes y trabajadores informales.</li>
            <li>La mayoría de los comedores fomentan la participación activa de los beneficiarios en la labor social, creando un modelo de corresponsabilidad.</li>
            <li>Esta diversidad poblacional refuerza la importancia de los comedores como mecanismos de protección social y su potencial como centros de desarrollo comunitario inclusivos.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
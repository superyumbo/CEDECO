"""
Módulo que muestra la página de financiación y dificultades de comedores.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def show_financing(df):
    """
    Muestra la página de financiación y dificultades de los comedores.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="section-header">Financiación y Dificultades</div>', unsafe_allow_html=True)
    st.markdown("Análisis de las fuentes de financiación, recursos y principales dificultades de los comedores")
    
    # Verificar columnas relevantes
    financiacion_col = 'FINANCIACION_ACTIVIDADES' if 'FINANCIACION_ACTIVIDADES' in df.columns else None
    otra_financiacion_col = 'QUE_OTRA_FINANCIACION' if 'QUE_OTRA_FINANCIACION' in df.columns else None
    dificultades_col = 'HA_TENIDO_DIFICULTADES' if 'HA_TENIDO_DIFICULTADES' in df.columns else None
    que_dificultades_col = 'QUE_DIFICULTADES' if 'QUE_DIFICULTADES' in df.columns else None
    
    # Dividir en columnas
    col1, col2 = st.columns(2)
    
    with col1:
        if financiacion_col:
            # Análisis de fuentes de financiación
            st.markdown('<div class="subsection-header">Fuentes de Financiación</div>', unsafe_allow_html=True)
            
            # Procesar los datos para el análisis
            fuentes = []
            for financiacion in df[financiacion_col].dropna():
                if isinstance(financiacion, str):
                    for fuente in financiacion.split(','):
                        fuente = fuente.strip()
                        if fuente:
                            fuentes.append(fuente)
            
            if fuentes:
                fuentes_counts = pd.Series(fuentes).value_counts().reset_index()
                fuentes_counts.columns = ['Fuente', 'Cantidad']
                
                # Crear gráfico de barras
                fig_fuentes = px.bar(
                    fuentes_counts, 
                    y='Fuente', 
                    x='Cantidad',
                    orientation='h',
                    title='Fuentes de Financiación Utilizadas',
                    color='Cantidad',
                    color_continuous_scale='Blues'
                )
                
                fig_fuentes.update_layout(height=400)
                st.plotly_chart(fig_fuentes, use_container_width=True)
                
                # Conclusión
                st.markdown('<div class="conclusion">Los recursos propios y las donaciones son las principales fuentes de financiación de los comedores. Esta dependencia de recursos limitados y variables podría afectar la sostenibilidad a largo plazo.</div>', unsafe_allow_html=True)
            else:
                st.info("No hay datos suficientes sobre fuentes de financiación.")
    
    with col2:
        if dificultades_col:
            # Análisis de dificultades
            st.markdown('<div class="subsection-header">Presencia de Dificultades</div>', unsafe_allow_html=True)
            
            # Contar comedores que han tenido dificultades
            tiene_dificultades = df[dificultades_col].apply(
                lambda x: 'Sí' if x == 'SI' else ('No' if x == 'NO' else 'Sin datos')
            ).value_counts().reset_index()
            
            tiene_dificultades.columns = ['Ha tenido dificultades', 'Cantidad']
            
            # Crear gráfico de pastel
            fig_dificultades = px.pie(
                tiene_dificultades, 
                values='Cantidad', 
                names='Ha tenido dificultades',
                title='Comedores que han Reportado Dificultades',
                color_discrete_sequence=['#1E40AF', '#93C5FD', '#E0F2FE']
            )
            
            fig_dificultades.update_traces(textposition='inside', textinfo='percent+label')
            fig_dificultades.update_layout(height=400)
            st.plotly_chart(fig_dificultades, use_container_width=True)
            
            # Calcular porcentaje para conclusión
            total_respuestas = tiene_dificultades['Cantidad'].sum()
            no_dificultades = tiene_dificultades[tiene_dificultades['Ha tenido dificultades'] == 'No']['Cantidad'].sum() if 'No' in tiene_dificultades['Ha tenido dificultades'].values else 0
            porcentaje_no = round((no_dificultades / total_respuestas) * 100) if total_respuestas > 0 else 0
            
            # Conclusión
            st.markdown(f'<div class="conclusion">El {porcentaje_no}% de los comedores que respondieron reportan no haber tenido dificultades significativas, lo que sugiere resiliencia y capacidad de gestión. Sin embargo, es importante analizar si esta percepción refleja la realidad o si hay retos que no están siendo identificados.</div>', unsafe_allow_html=True)
    
    # Análisis de financiación adicional
    if otra_financiacion_col:
        st.markdown('<div class="subsection-header">Fuentes Alternativas de Financiación</div>', unsafe_allow_html=True)
        
        # Mostrar información sobre otras fuentes de financiación
        otra_financiacion = df[[otra_financiacion_col, 'NOMBRE_COMEDOR']].dropna(subset=[otra_financiacion_col])
        
        if not otra_financiacion.empty:
            for _, row in otra_financiacion.iterrows():
                if pd.notna(row[otra_financiacion_col]) and row[otra_financiacion_col].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row[otra_financiacion_col]}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown('<div class="conclusion">Las fuentes alternativas de financiación incluyen aportes personales, convenios institucionales, articulación con organizaciones y apoyo de comerciantes locales. Se observa creatividad y diversificación en la búsqueda de recursos, aunque muchas iniciativas dependen del esfuerzo personal de las gestoras.</div>', unsafe_allow_html=True)
        else:
            st.info("No hay información disponible sobre fuentes alternativas de financiación.")
    
    # Análisis detallado de dificultades
    if que_dificultades_col:
        st.markdown('<div class="subsection-header">Análisis de Dificultades Reportadas</div>', unsafe_allow_html=True)
        
        # Mostrar información sobre dificultades específicas
        dificultades_detalle = df[[que_dificultades_col, 'NOMBRE_COMEDOR']].dropna(subset=[que_dificultades_col])
        
        if not dificultades_detalle.empty:
            for _, row in dificultades_detalle.iterrows():
                if pd.notna(row[que_dificultades_col]) and row[que_dificultades_col].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row[que_dificultades_col]}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown('<div class="conclusion">Entre las principales dificultades reportadas se encuentran la falta de recursos estables, infraestructura limitada y desafíos para ampliar la cobertura. A pesar de esto, la mayoría reporta no tener dificultades mayores, lo que puede indicar adaptabilidad o normalización de ciertos retos.</div>', unsafe_allow_html=True)
        else:
            st.info("No hay información detallada sobre dificultades específicas.")
    
    # Análisis de necesidades de financiamiento
    if 'OBSERVACIONES_AREA_FINANCIAMIENTO' in df.columns:
        st.markdown('<div class="subsection-header">Necesidades de Financiamiento</div>', unsafe_allow_html=True)
        
        # Mostrar observaciones sobre financiamiento
        financiamiento_obs = df[['OBSERVACIONES_AREA_FINANCIAMIENTO', 'NOMBRE_COMEDOR']].dropna(subset=['OBSERVACIONES_AREA_FINANCIAMIENTO'])
        
        if not financiamiento_obs.empty:
            for _, row in financiamiento_obs.iterrows():
                if pd.notna(row['OBSERVACIONES_AREA_FINANCIAMIENTO']) and row['OBSERVACIONES_AREA_FINANCIAMIENTO'].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row['OBSERVACIONES_AREA_FINANCIAMIENTO']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown('<div class="conclusion">Las principales necesidades de financiamiento se centran en emprendimientos para la sostenibilidad, equipamiento (sillas, mesas) y remuneración de formadores. Esto refleja un enfoque tanto en operaciones cotidianas como en desarrollo de capacidades a largo plazo.</div>', unsafe_allow_html=True)
        else:
            st.info("No hay observaciones disponibles sobre necesidades de financiamiento.")
    
    # Conclusión general
    st.markdown("""
    <div class="conclusion">
        <strong>Conclusiones principales sobre financiación y dificultades:</strong>
        <ul>
            <li>Los comedores dependen principalmente de recursos propios y donaciones, lo que plantea retos de sostenibilidad a largo plazo.</li>
            <li>La mayoría de los comedores evaluados no reportan dificultades significativas, lo que sugiere resiliencia o adaptación a sus condiciones actuales.</li>
            <li>Existe una diversificación creativa de fuentes de financiamiento, pero con fuerte dependencia del esfuerzo personal de las gestoras.</li>
            <li>Las necesidades de financiamiento se orientan tanto a operaciones básicas (equipamiento) como a desarrollo de capacidades (formación).</li>
            <li>Se recomienda fortalecer estrategias de sostenibilidad financiera como parte del proceso de transformación a centros de desarrollo comunitario.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
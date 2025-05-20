"""
Módulo que muestra la página de actividades realizadas por los comedores.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import re

def show_activities(df):
    """
    Muestra la página de actividades realizadas por los comedores.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="section-header">Actividades Realizadas</div>', unsafe_allow_html=True)
    st.markdown("Análisis de las actividades, programas y su frecuencia en los comedores comunitarios")
    
    # Verificar columnas relevantes
    acciones_col = 'ACCIONES_PUNTUALES_COMEDOR' if 'ACCIONES_PUNTUALES_COMEDOR' in df.columns else None
    vinculacion_col = 'VINCULACION_OTROS_ACTORES' if 'VINCULACION_OTROS_ACTORES' in df.columns else None
    seguimiento_col = 'SEGUIMIENTO_EVALUACION_A_OTRAS_ACTIVIDADES' if 'SEGUIMIENTO_EVALUACION_A_OTRAS_ACTIVIDADES' in df.columns else None
    
    # Analizar acciones puntuales
    if acciones_col:
        st.markdown('<div class="subsection-header">Acciones Realizadas por los Comedores</div>', unsafe_allow_html=True)
        
        # Procesar los datos para el análisis
        acciones = []
        for accion in df[acciones_col].dropna():
            if isinstance(accion, str):
                # Extraer acciones específicas con su letra
                matches = re.findall(r'([A-Z])\.\s+([^\.]+?)(?=\s*[A-Z]\.\s+|\s*$)', accion)
                for match in matches:
                    letra, descripcion = match
                    descripcion_corta = descripcion.strip()
                    if len(descripcion_corta) > 40:
                        descripcion_corta = descripcion_corta[:37] + "..."
                    acciones.append((letra, descripcion_corta))
        
        if acciones:
            # Contar frecuencia de cada acción
            accion_counts = pd.DataFrame(acciones, columns=['Letra', 'Descripción'])
            accion_counts = accion_counts.groupby(['Letra', 'Descripción']).size().reset_index(name='Cantidad')
            
            # Ordenar por letra para mantener orden original
            accion_counts['Letra_num'] = accion_counts['Letra'].apply(lambda x: ord(x))
            accion_counts = accion_counts.sort_values('Letra_num').drop('Letra_num', axis=1)
            
            # Crear etiquetas combinadas para el gráfico
            accion_counts['Acción'] = accion_counts.apply(lambda row: f"{row['Letra']}. {row['Descripción']}", axis=1)
            
            # Crear gráfico de barras
            fig_acciones = px.bar(
                accion_counts, 
                y='Acción', 
                x='Cantidad',
                orientation='h',
                title='Acciones Realizadas por los Comedores',
                color='Cantidad',
                color_continuous_scale='Blues'
            )
            
            fig_acciones.update_layout(height=600)  # Mayor altura para acomodar todas las acciones
            st.plotly_chart(fig_acciones, use_container_width=True)
            
            # Top 3 acciones más comunes
            top_acciones = accion_counts.sort_values('Cantidad', ascending=False).head(3)
            top_nombres = [f"{row['Letra']}. {row['Descripción']}" for _, row in top_acciones.iterrows()]
            
            # Conclusión
            st.markdown(f"""
            <div class="conclusion">
                Las acciones más comunes realizadas por los comedores son:
                <ol>
                    <li>{top_nombres[0] if len(top_nombres) > 0 else ''}</li>
                    <li>{top_nombres[1] if len(top_nombres) > 1 else ''}</li>
                    <li>{top_nombres[2] if len(top_nombres) > 2 else ''}</li>
                </ol>
                Esto refleja un enfoque integral que combina formación, recreación y articulación institucional, fortaleciendo el rol de los comedores como centros de desarrollo comunitario.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos suficientes sobre acciones puntuales de los comedores.")
    
    # Análisis de frecuencia de actividades
    st.markdown('<div class="subsection-header">Frecuencia de Actividades</div>', unsafe_allow_html=True)
    
    # Identificar columnas de frecuencia
    frecuencia_cols = [col for col in df.columns if '_FRECUENCIA' in col]
    
    if frecuencia_cols:
        # Crear una tabla de frecuencias
        frecuencia_data = []
        
        for col in frecuencia_cols:
            # Extraer tipo de actividad del nombre de la columna
            actividad = col.split('_FRECUENCIA')[0].replace('_', ' ').title()
            
            # Contar frecuencias
            frecuencias = df[col].value_counts().reset_index()
            if not frecuencias.empty:
                frecuencias.columns = ['Frecuencia', 'Cantidad']
                
                # Añadir información de actividad
                frecuencias['Actividad'] = actividad
                
                frecuencia_data.append(frecuencias)
        
        if frecuencia_data:
            # Combinar todos los datos de frecuencia
            frecuencia_df = pd.concat(frecuencia_data, ignore_index=True)
            
            # Crear un mapa de calor
            freq_pivot = frecuencia_df.pivot_table(
                values='Cantidad', 
                index='Actividad', 
                columns='Frecuencia', 
                aggfunc='sum',
                fill_value=0
            )
            
            # Orden personalizado para las frecuencias
            orden_freq = ['DIARIA', 'SEMANAL', 'QUINCENAL', 'MENSUAL', 'BIMESTRAL', 'TRIMESTRAL', 'SEMESTRAL', 'ANUAL', 'NUNCA']
            columnas_ordenadas = [col for col in orden_freq if col in freq_pivot.columns]
            freq_pivot = freq_pivot[columnas_ordenadas]
            
            # Convertir a formato largo para plotly
            freq_long = freq_pivot.reset_index().melt(
                id_vars='Actividad',
                var_name='Frecuencia',
                value_name='Cantidad'
            )
            
            # Crear mapa de calor
            fig_heat = px.density_heatmap(
                freq_long,
                y='Actividad',
                x='Frecuencia',
                z='Cantidad',
                title='Frecuencia de Realización de Actividades',
                color_continuous_scale='Blues'
            )
            
            fig_heat.update_layout(height=500)
            st.plotly_chart(fig_heat, use_container_width=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                Se observa una variación significativa en la frecuencia de las actividades. Las actividades formativas tienden a realizarse con mayor frecuencia (semanal/mensual), mientras que eventos especiales y ferias se realizan más esporádicamente (trimestral/anual). Esta distribución refleja una combinación efectiva de acciones continuas y eventos especiales.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos suficientes sobre frecuencia de actividades.")
    else:
        st.info("No se encontraron columnas con información de frecuencia de actividades.")
    
    # Análisis de vinculación con otros actores
    col1, col2 = st.columns(2)
    
    with col1:
        if vinculacion_col:
            st.markdown('<div class="subsection-header">Vinculación con Otros Actores</div>', unsafe_allow_html=True)
            
            # Contar tipos de vinculación
            vinculacion_counts = df[vinculacion_col].value_counts().reset_index()
            vinculacion_counts.columns = ['Vinculación', 'Cantidad']
            
            # Crear gráfico de pastel
            fig_vinc = px.pie(
                vinculacion_counts, 
                values='Cantidad', 
                names='Vinculación',
                title='Frecuencia de Vinculación con Otros Actores',
                color_discrete_sequence=px.colors.sequential.Blues
            )
            
            fig_vinc.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_vinc, use_container_width=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                La mayoría de comedores reporta una vinculación frecuente ("Siempre" u "Ocasional") con otros actores, lo que demuestra capacidad de articulación y trabajo en red. Esta característica es fundamental para su potencial como centros de desarrollo comunitario.
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if seguimiento_col:
            st.markdown('<div class="subsection-header">Seguimiento y Evaluación</div>', unsafe_allow_html=True)
            
            # Contar realización de seguimiento
            seguimiento_counts = df[seguimiento_col].value_counts().reset_index()
            seguimiento_counts.columns = ['Realiza Seguimiento', 'Cantidad']
            
            # Crear gráfico de pastel
            fig_seg = px.pie(
                seguimiento_counts, 
                values='Cantidad', 
                names='Realiza Seguimiento',
                title='Comedores que Realizan Seguimiento a Actividades',
                color_discrete_sequence=px.colors.sequential.Blues
            )
            
            fig_seg.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_seg, use_container_width=True)
            
            # Conclusión
            si_count = seguimiento_counts[seguimiento_counts['Realiza Seguimiento'] == 'SI']['Cantidad'].sum() if 'SI' in seguimiento_counts['Realiza Seguimiento'].values else 0
            total = seguimiento_counts['Cantidad'].sum()
            porcentaje = round((si_count / total) * 100) if total > 0 else 0
            
            st.markdown(f"""
            <div class="conclusion">
                El {porcentaje}% de los comedores realiza seguimiento y evaluación de sus actividades, lo que evidencia capacidad de gestión y mejora continua. Esta práctica es esencial para la sostenibilidad y el impacto a largo plazo.
            </div>
            """, unsafe_allow_html=True)
    
    # Análisis de huertas comunitarias
    if 'INICIATIVA_HUERTAS' in df.columns:
        st.markdown('<div class="subsection-header">Iniciativas de Huertas Comunitarias</div>', unsafe_allow_html=True)
        
        # Contar comedores con huertas
        huertas_counts = df['INICIATIVA_HUERTAS'].value_counts().reset_index()
        huertas_counts.columns = ['Tiene Huerta', 'Cantidad']
        
        # Crear gráfico de barras
        fig_huertas = px.bar(
            huertas_counts, 
            x='Tiene Huerta', 
            y='Cantidad',
            title='Comedores con Iniciativas de Huertas Comunitarias',
            color='Cantidad',
            color_continuous_scale='Greens'
        )
        
        st.plotly_chart(fig_huertas, use_container_width=True)
        
        # Mostrar información sobre gestión de huertas
        if 'GESTION_HC' in df.columns:
            st.markdown("#### Gestión de las Huertas Comunitarias")
            
            for idx, row in df.iterrows():
                if pd.notna(row['INICIATIVA_HUERTAS']) and row['INICIATIVA_HUERTAS'] == 'SI' and pd.notna(row['GESTION_HC']):
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row['GESTION_HC']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Conclusión sobre huertas
        si_count = huertas_counts[huertas_counts['Tiene Huerta'] == 'SI']['Cantidad'].sum() if 'SI' in huertas_counts['Tiene Huerta'].values else 0
        total = huertas_counts['Cantidad'].sum()
        porcentaje = round((si_count / total) * 100) if total > 0 else 0
        
        st.markdown(f"""
        <div class="conclusion">
            El {porcentaje}% de los comedores ha implementado iniciativas de huertas comunitarias, lo que fortalece la sostenibilidad alimentaria y el componente ambiental. Las huertas son gestionadas principalmente con apoyo comunitario y representan un potencial significativo para la transformación a centros de desarrollo.
        </div>
        """, unsafe_allow_html=True)
    
    # Conclusión general
    st.markdown("""
    <div class="conclusion">
        <strong>Conclusiones principales sobre actividades realizadas:</strong>
        <ul>
            <li>Los comedores realizan una amplia variedad de actividades que trascienden la provisión de alimentos, incluyendo talleres formativos, actividades recreativas y articulación institucional.</li>
            <li>Existe una gestión diferenciada de frecuencias, con actividades continuas (semanales/mensuales) y eventos especiales (trimestrales/anuales).</li>
            <li>La mayoría de comedores demuestra capacidad de articulación con otros actores y realiza seguimiento a sus actividades.</li>
            <li>Las iniciativas de huertas comunitarias representan un componente innovador con potencial para fortalecer la sostenibilidad.</li>
            <li>Este perfil de actividades demuestra que los comedores ya funcionan como centros de desarrollo comunitario incipientes, con potencial para fortalecer y formalizar este rol.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
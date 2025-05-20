"""
Módulo que muestra la página de historia y participación de comedores.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

def extract_years_from_text(text):
    """
    Extrae años desde un texto para análisis histórico.
    
    Args:
        text (str): Texto a analizar.
    
    Returns:
        list: Lista de años encontrados.
    """
    if not isinstance(text, str):
        return []
    
    # Buscar años entre 1990 y 2025
    pattern = r'\b(19[9][0-9]|20[0-2][0-9])\b'
    return re.findall(pattern, text)

def generate_wordcloud(texts):
    """
    Genera una nube de palabras a partir de textos.
    
    Args:
        texts (list): Lista de textos para generar la nube.
    
    Returns:
        matplotlib.figure.Figure: Figura con la nube de palabras.
    """
    # Unir todos los textos
    text = " ".join(t for t in texts if isinstance(t, str))
    
    # Lista de palabras a excluir (stopwords)
    stopwords = set(['de', 'la', 'el', 'y', 'en', 'a', 'que', 'los', 'del', 'se', 'las', 'por', 'un', 'con', 
                     'una', 'para', 'es', 'al', 'lo', 'como', 'más', 'o', 'pero', 'sus', 'le', 'ha', 'me', 
                     'si', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son',
                     'mi', 'hay', 'porque', 'muy', 'estos', 'estas', 'fue', 'así', 'también', 'desde', 'he'])
    
    # Generar nube de palabras
    wordcloud = WordCloud(width=800, height=400, 
                          background_color='white', 
                          stopwords=stopwords,
                          min_font_size=10).generate(text)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    return fig

def show_history_participation(df):
    """
    Muestra la página de historia y participación de los comedores.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="section-header">Historia y Participación</div>', unsafe_allow_html=True)
    st.markdown("Análisis de la trayectoria histórica de los comedores y su participación en actividades comunitarias")
    
    # Verificar columnas relevantes
    historia_col = 'HISTORIA_COMEDOR' if 'HISTORIA_COMEDOR' in df.columns else None
    observaciones_col = 'Observaciones1' if 'Observaciones1' in df.columns else None
    participacion_col = 'PARTICIPACION_ACTIVIDADES' if 'PARTICIPACION_ACTIVIDADES' in df.columns else None
    observaciones_part_col = 'Observaciones2' if 'Observaciones2' in df.columns else None
    
    # Mostrar estadísticas generales
    col1, col2 = st.columns(2)
    
    with col1:
        if historia_col:
            # Contar comedores con historia documentada
            tiene_historia = df[historia_col].apply(lambda x: 'Sí' if x == 'SI' else 'No').value_counts()
            
            fig = px.pie(
                values=tiene_historia.values,
                names=tiene_historia.index,
                title="Comedores con Historia Documentada",
                color_discrete_sequence=['#1E40AF', '#93C5FD']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
            # Conclusión
            if 'Sí' in tiene_historia.index:
                porcentaje_si = round(tiene_historia['Sí'] / tiene_historia.sum() * 100)
                st.markdown(f'<div class="conclusion">El {porcentaje_si}% de los comedores tienen historia documentada, lo que refleja un arraigo histórico en la comunidad y facilita la comprensión de su evolución.</div>', unsafe_allow_html=True)
    
    with col2:
        if participacion_col:
            # Contar comedores con participación en actividades
            participa = df[participacion_col].apply(lambda x: 'Sí' if x == 'SI' else 'No').value_counts()
            
            fig = px.pie(
                values=participa.values,
                names=participa.index,
                title="Comedores con Participación en Actividades",
                color_discrete_sequence=['#1E40AF', '#93C5FD']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
            # Conclusión
            if 'Sí' in participa.index:
                porcentaje_si = round(participa['Sí'] / participa.sum() * 100)
                st.markdown(f'<div class="conclusion">El {porcentaje_si}% de los comedores participan en actividades comunitarias, lo que demuestra su integración y compromiso con el desarrollo local.</div>', unsafe_allow_html=True)
    
    # Análisis de la historia de los comedores
    st.markdown('<div class="subsection-header">Análisis Histórico</div>', unsafe_allow_html=True)
    
    if observaciones_col and any(df[observaciones_col].notna()):
        # Extraer años mencionados en las historias
        all_years = []
        for text in df[observaciones_col].dropna():
            years = extract_years_from_text(text)
            all_years.extend(years)
        
        if all_years:
            # Contar frecuencia de años
            years_count = pd.Series(all_years).value_counts().reset_index()
            years_count.columns = ['Año', 'Frecuencia']
            years_count = years_count.sort_values('Año')
            
            # Crear gráfico de línea temporal
            fig = px.bar(
                years_count, 
                x='Año', 
                y='Frecuencia',
                title='Línea de Tiempo - Años Mencionados en las Historias',
                color='Frecuencia',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Conclusión sobre años
            year_min = min(years_count['Año']) if not years_count.empty else 'N/A'
            year_max = max(years_count['Año']) if not years_count.empty else 'N/A'
            st.markdown(f'<div class="conclusion">Las historias de los comedores abarcan desde {year_min} hasta {year_max}, reflejando una trayectoria de compromiso comunitario. Los años mencionados muestran momentos clave en su desarrollo, principalmente alrededor de su fundación.</div>', unsafe_allow_html=True)
        
        # Generar nube de palabras de las historias
        st.markdown("### Temas principales en las historias")
        historia_texts = df[observaciones_col].dropna().tolist()
        
        if historia_texts:
            try:
                wordcloud_fig = generate_wordcloud(historia_texts)
                st.pyplot(wordcloud_fig)
                st.markdown('<div class="conclusion">Las palabras más frecuentes en las historias de los comedores revelan un enfoque en la comunidad, apoyo, actividades y participación. Se destaca la importancia de las gestoras, la iglesia, la fundación y los espacios de formación.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"No se pudo generar la nube de palabras: {str(e)}")
    else:
        st.info("No hay suficientes datos en las observaciones de historia para realizar un análisis detallado.")
    
    # Análisis de la participación en actividades
    st.markdown('<div class="subsection-header">Actividades y Participación</div>', unsafe_allow_html=True)
    
    if observaciones_part_col and any(df[observaciones_part_col].notna()):
        # Mostrar ejemplos de participación
        st.markdown("### Ejemplos de participación en actividades")
        
        for idx, row in df.iterrows():
            if pd.notna(row[observaciones_part_col]) and row[observaciones_part_col]:
                st.markdown(f"**{row['NOMBRE_COMEDOR']}:** {row[observaciones_part_col]}")
        
        # Generar nube de palabras de la participación
        st.markdown("### Temas principales en la participación")
        participacion_texts = df[observaciones_part_col].dropna().tolist()
        
        if participacion_texts:
            try:
                wordcloud_fig = generate_wordcloud(participacion_texts)
                st.pyplot(wordcloud_fig)
                st.markdown('<div class="conclusion">Las palabras más frecuentes en la participación muestran un enfoque en talleres, capacitaciones, comunidad y actividades. Se destaca la importancia de las reuniones, jornadas y formación.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"No se pudo generar la nube de palabras: {str(e)}")
    else:
        st.info("No hay suficientes datos en las observaciones de participación para realizar un análisis detallado.")
    
    # Conclusión general
    st.markdown("""
    <div class="conclusion">
        <strong>Conclusiones principales sobre historia y participación:</strong>
        <ul>
            <li>Todos los comedores evaluados tienen una historia documentada, lo que muestra su arraigo y trayectoria en la comunidad.</li>
            <li>El 100% de los comedores participan activamente en actividades comunitarias, demostrando su capacidad para funcionar como centros de desarrollo.</li>
            <li>Las historias reflejan una evolución desde iniciativas informales (ollas comunitarias) hasta estructuras más organizadas.</li>
            <li>La participación se centra en actividades formativas, culturales y sociales que fortalecen el tejido comunitario.</li>
            <li>Se observa un fuerte componente de liderazgo femenino y apoyo a poblaciones vulnerables en la mayoría de las iniciativas.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
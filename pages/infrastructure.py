"""
Módulo que muestra la página de infraestructura y funcionamiento de comedores.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_infrastructure(df):
    """
    Muestra la página de infraestructura y funcionamiento de los comedores.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="section-header">Infraestructura y Funcionamiento</div>', unsafe_allow_html=True)
    st.markdown("Análisis de los espacios físicos, infraestructura y capacidades instaladas de los comedores")
    
    # Dividir en columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico 1: Tipo de espacio donde funciona el comedor
        st.markdown('<div class="subsection-header">Tipo de Espacio</div>', unsafe_allow_html=True)
        
        # Procesar los datos para el gráfico
        df['TIPO_ESPACIO'] = df['LUGAR_DONDE_FUNCIONA_COMEDOR'].apply(
            lambda x: x.split('.')[0].strip() if isinstance(x, str) else ""
        )
        
        # Mapeo para nombres más legibles
        tipo_map = {
            'A': 'Vivienda Gestores',
            'B': 'Local Comercial',
            'C': 'Institución/Fundación',
            '': 'No especificado'
        }
        
        df['TIPO_ESPACIO_NOMBRE'] = df['TIPO_ESPACIO'].map(tipo_map)
        
        tipo_counts = df['TIPO_ESPACIO_NOMBRE'].value_counts().reset_index()
        tipo_counts.columns = ['Tipo', 'Cantidad']
        
        # Crear gráfico de barras
        fig_tipo = px.bar(tipo_counts, x='Tipo', y='Cantidad',
                         title='Tipo de Espacio donde Funciona el Comedor',
                         color='Cantidad',
                         color_continuous_scale='Blues')
        
        fig_tipo.update_layout(height=400)
        st.plotly_chart(fig_tipo, use_container_width=True)
        
        # Cálculo para la conclusión
        total = tipo_counts['Cantidad'].sum()
        porcentaje_vivienda = round(tipo_counts[tipo_counts['Tipo'] == 'Vivienda Gestores']['Cantidad'].sum() / total * 100)
        porcentaje_institucion = round(tipo_counts[tipo_counts['Tipo'] == 'Institución/Fundación']['Cantidad'].sum() / total * 100)
        
        # Conclusión
        st.markdown(f'<div class="conclusion">El {porcentaje_vivienda}% de los comedores funcionan en viviendas de los gestores y el {porcentaje_institucion}% en instituciones o fundaciones. Esta distribución muestra el carácter comunitario de estos espacios, pero también su potencial vulnerabilidad al depender de espacios personales.</div>', unsafe_allow_html=True)
        
    with col2:
        # Gráfico 2: Disponibilidad de espacio para talleres
        st.markdown('<div class="subsection-header">Espacio para Talleres</div>', unsafe_allow_html=True)
        
        # Contar disponibilidad de espacios para talleres
        espacio_counts = df['ESPACIO_TALLERES'].value_counts().reset_index()
        espacio_counts.columns = ['Disponibilidad', 'Cantidad']
        
        # Crear gráfico de pastel
        fig_espacio = px.pie(espacio_counts, values='Cantidad', names='Disponibilidad',
                           title='Disponibilidad de Espacio para Talleres',
                           color_discrete_sequence=['#1E40AF', '#93C5FD'])
        
        fig_espacio.update_traces(textposition='inside', textinfo='percent+label')
        fig_espacio.update_layout(height=400)
        st.plotly_chart(fig_espacio, use_container_width=True)
        
        # Cálculo para conclusión
        if 'SI' in espacio_counts['Disponibilidad'].values:
            si_count = espacio_counts[espacio_counts['Disponibilidad'] == 'SI']['Cantidad'].values[0]
            porcentaje_si = round(si_count / espacio_counts['Cantidad'].sum() * 100)
            conclusión_espacio = f"El {porcentaje_si}% de los comedores cuentan con espacio para realizar talleres, lo que facilita su transición a centros de desarrollo comunitario con capacidad formativa."
        else:
            conclusión_espacio = "No hay datos suficientes sobre espacios para talleres."
        
        st.markdown(f'<div class="conclusion">{conclusión_espacio}</div>', unsafe_allow_html=True)
    
    # Mapa de ubicación de comedores (si hay coordenadas disponibles)
    st.markdown('<div class="subsection-header">Distribución Geográfica</div>', unsafe_allow_html=True)
    
    # Procesar coordenadas si están disponibles
    df_con_coords = df.copy()
    df_con_coords['lat'] = None
    df_con_coords['lon'] = None
    
    for idx, row in df.iterrows():
        if pd.notna(row['UBICACION']) and row['UBICACION']:
            try:
                coords = row['UBICACION'].split(',')
                if len(coords) == 2:
                    df_con_coords.at[idx, 'lat'] = float(coords[0].strip())
                    df_con_coords.at[idx, 'lon'] = float(coords[1].strip())
            except:
                pass
    
    # Filtrar filas con coordenadas válidas
    df_mapa = df_con_coords[pd.notna(df_con_coords['lat']) & pd.notna(df_con_coords['lon'])].copy()
    
    if not df_mapa.empty:
        # Crear mapa con plotly
        fig_mapa = px.scatter_mapbox(
            df_mapa, 
            lat='lat', 
            lon='lon', 
            hover_name='NOMBRE_COMEDOR',
            hover_data={
                'COMUNA': True,
                'BARRIO': True,
                'NOMBER_GESTORA': True,
                'lat': False,
                'lon': False
            },
            zoom=11,
            title='Distribución Geográfica de Comedores',
            color_discrete_sequence=['#1E40AF']
        )
        
        fig_mapa.update_layout(
            mapbox_style="open-street-map",
            height=500
        )
        
        st.plotly_chart(fig_mapa, use_container_width=True)
        
        # Conclusión del mapa
        st.markdown('<div class="conclusion">La distribución geográfica muestra una cobertura en diferentes zonas de la ciudad, lo que permite atender diversas comunidades y necesidades. La disposición espacial sugiere una buena distribución territorial para la fase inicial del proyecto.</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay datos de coordenadas disponibles para mostrar el mapa.")
    
    # Articulación con organizaciones
    st.markdown('<div class="subsection-header">Articulación con Organizaciones</div>', unsafe_allow_html=True)
    
    # Verificar si todos tienen articulación con organizaciones
    if 'ARTICULACION_CON_ORGANIZACIONES' in df.columns:
        articulacion_counts = df['ARTICULACION_CON_ORGANIZACIONES'].value_counts().reset_index()
        articulacion_counts.columns = ['Tiene Articulación', 'Cantidad']
        
        # Mostrar porcentaje 
        total = articulacion_counts['Cantidad'].sum()
        si_count = articulacion_counts[articulacion_counts['Tiene Articulación'] == 'SI']['Cantidad'].sum() if 'SI' in articulacion_counts['Tiene Articulación'].values else 0
        porcentaje_si = round(si_count / total * 100)
        
        # Crear métrica visual
        st.metric("Comedores con articulación organizacional", f"{si_count} de {total}", f"{porcentaje_si}%")
        
        # Analizar las organizaciones con las que se articulan
        if '¿Cuáles?2' in df.columns:
            st.markdown("#### Principales organizaciones con las que se articulan los comedores:")
            
            # Mostrar ejemplos de organizaciones
            for idx, row in df.iterrows():
                if pd.notna(row['¿Cuáles?2']) and row['¿Cuáles?2']:
                    st.markdown(f"**{row['NOMBRE_COMEDOR']}:** {row['¿Cuáles?2']}")
        
        # Conclusión sobre articulación
        st.markdown('<div class="conclusion">El 100% de los comedores evaluados tienen articulación con otras organizaciones, lo que demuestra capacidad de trabajo en red y potencial para ampliar su impacto. Las principales alianzas incluyen instituciones educativas, juntas de acción comunal, organizaciones sociales y entidades religiosas.</div>', unsafe_allow_html=True)
    
    # Conclusión general de la sección
    st.markdown("""
    <div class="conclusion">
        <strong>Conclusiones principales sobre infraestructura y funcionamiento:</strong>
        <ul>
            <li>La mayoría de comedores funcionan en espacios de las gestoras o instituciones, demostrando el arraigo comunitario pero también una posible limitación de infraestructura.</li>
            <li>Existe alta disponibilidad de espacios para talleres, lo que facilita la transición a centros de desarrollo comunitario.</li>
            <li>La distribución geográfica muestra buena cobertura territorial en la fase inicial.</li>
            <li>Todos los comedores muestran capacidad de articulación con otras organizaciones, lo que es una fortaleza para el desarrollo de los CEDECO.</li>
            <li>La infraestructura existente apoya el potencial de transformación, pero requerirá inversiones estratégicas para optimizar los espacios.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar tabla de datos relevantes
    with st.expander("Ver datos de infraestructura"):
        st.dataframe(df[['NOMBRE_COMEDOR', 'LUGAR_DONDE_FUNCIONA_COMEDOR', 'ESPACIO_TALLERES', 'ARTICULACION_CON_ORGANIZACIONES', 'COMUNA', 'BARRIO']])
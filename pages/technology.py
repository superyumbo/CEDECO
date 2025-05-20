"""
Módulo que muestra la página de uso de tecnología y comunicación de comedores.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def show_technology(df):
    """
    Muestra la página de uso de tecnología y comunicación de los comedores.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="section-header">Uso de Tecnología y Comunicación</div>', unsafe_allow_html=True)
    st.markdown("Análisis de las herramientas tecnológicas y estrategias de comunicación que utilizan los comedores")
    
    # Verificar columnas relevantes
    uso_tic_col = 'USO_DE_TIC' if 'USO_DE_TIC' in df.columns else None
    redes_col = 'QUE_REDES' if 'QUE_REDES' in df.columns else None
    office_col = 'PAQUETES_OFFICE' if 'PAQUETES_OFFICE' in df.columns else None
    estrategias_col = 'QUE_ESTRATEGIAS_USA' if 'QUE_ESTRATEGIAS_USA' in df.columns else None
    
    # Métricas generales
    col_metrics = st.columns(2)
    
    with col_metrics[0]:
        if uso_tic_col:
            # Contar comedores que usan TICs
            df_tic = df.copy()
            df_tic['usa_tic'] = df_tic[uso_tic_col].notna() & (df_tic[uso_tic_col] != '')
            total_con_tic = df_tic['usa_tic'].sum()
            porcentaje_tic = round((total_con_tic / len(df)) * 100)
            
            st.metric("Comedores que utilizan TICs", f"{total_con_tic} de {len(df)}", f"{porcentaje_tic}%")
    
    with col_metrics[1]:
        if redes_col:
            # Contar comedores que usan redes sociales
            df_redes = df.copy()
            df_redes['usa_redes'] = df_redes[redes_col].notna() & (df_redes[redes_col] != '')
            total_con_redes = df_redes['usa_redes'].sum()
            porcentaje_redes = round((total_con_redes / len(df)) * 100)
            
            st.metric("Comedores que utilizan redes sociales", f"{total_con_redes} de {len(df)}", f"{porcentaje_redes}%")
    
    # Dividir en columnas para gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        if uso_tic_col:
            # Analizar tipos de TIC utilizadas
            st.markdown('<div class="subsection-header">Tipos de TIC Utilizadas</div>', unsafe_allow_html=True)
            
            # Procesar los datos para el análisis
            tipos_tic = []
            for tic in df[uso_tic_col].dropna():
                if isinstance(tic, str):
                    for tipo in tic.split(';'):
                        tipo = tipo.strip()
                        if tipo:
                            tipos_tic.append(tipo)
            
            if tipos_tic:
                tic_counts = pd.Series(tipos_tic).value_counts().reset_index()
                tic_counts.columns = ['Tipo de TIC', 'Cantidad']
                
                # Crear gráfico de barras
                fig_tic = px.bar(
                    tic_counts, 
                    y='Tipo de TIC', 
                    x='Cantidad',
                    orientation='h',
                    title='Tipos de TIC Utilizadas',
                    color='Cantidad',
                    color_continuous_scale='Blues'
                )
                
                fig_tic.update_layout(height=400)
                st.plotly_chart(fig_tic, use_container_width=True)
                
                # Conclusión
                st.markdown('<div class="conclusion">Las redes sociales son la herramienta tecnológica más utilizada por los comedores, seguida por el correo electrónico. Esto refleja un nivel básico pero funcional de adopción de tecnologías para la comunicación.</div>', unsafe_allow_html=True)
            else:
                st.info("No hay datos suficientes sobre uso de TIC.")
    
    with col2:
        if redes_col:
            # Analizar redes sociales utilizadas
            st.markdown('<div class="subsection-header">Redes Sociales Utilizadas</div>', unsafe_allow_html=True)
            
            # Procesar los datos para el análisis
            redes = []
            for red in df[redes_col].dropna():
                if isinstance(red, str):
                    for r in red.split(','):
                        r = r.strip()
                        if r:
                            redes.append(r)
            
            if redes:
                redes_counts = pd.Series(redes).value_counts().reset_index()
                redes_counts.columns = ['Red Social', 'Cantidad']
                
                # Crear gráfico de pastel
                fig_redes = px.pie(
                    redes_counts, 
                    values='Cantidad', 
                    names='Red Social',
                    title='Redes Sociales Utilizadas',
                    color_discrete_sequence=px.colors.sequential.Blues
                )
                
                fig_redes.update_traces(textposition='inside', textinfo='percent+label')
                fig_redes.update_layout(height=400)
                st.plotly_chart(fig_redes, use_container_width=True)
                
                # Conclusión
                st.markdown('<div class="conclusion">Facebook y WhatsApp son las redes sociales predominantes, lo que indica una preferencia por plataformas accesibles y de uso masivo. Instagram tiene menor presencia, lo que sugiere una oportunidad de expansión digital.</div>', unsafe_allow_html=True)
            else:
                st.info("No hay datos suficientes sobre uso de redes sociales.")
    
    # Análisis de paquetes de Office
    if office_col:
        st.markdown('<div class="subsection-header">Conocimiento de Herramientas Ofimáticas</div>', unsafe_allow_html=True)
        
        # Procesar los datos para el análisis
        office_tools = []
        for tools in df[office_col].dropna():
            if isinstance(tools, str):
                for tool in tools.split(','):
                    tool = tool.strip()
                    if tool:
                        office_tools.append(tool)
        
        if office_tools:
            office_counts = pd.Series(office_tools).value_counts().reset_index()
            office_counts.columns = ['Herramienta', 'Cantidad']
            
            # Crear gráfico de barras
            fig_office = px.bar(
                office_counts, 
                x='Herramienta', 
                y='Cantidad',
                title='Herramientas Ofimáticas Conocidas',
                color='Cantidad',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig_office, use_container_width=True)
            
            # Conclusión
            st.markdown('<div class="conclusion">El conocimiento de herramientas ofimáticas es limitado, con predominio de Word y Excel en nivel básico. También se mencionan aplicaciones no ofimáticas como redes sociales, lo que refleja confusión en la categorización de herramientas tecnológicas.</div>', unsafe_allow_html=True)
        else:
            st.info("No hay datos suficientes sobre uso de herramientas ofimáticas.")
    
    # Análisis de estrategias de comunicación
    if estrategias_col:
        st.markdown('<div class="subsection-header">Estrategias de Comunicación</div>', unsafe_allow_html=True)
        
        # Procesar los datos para el análisis
        estrategias = []
        for est in df[estrategias_col].dropna():
            if isinstance(est, str):
                for e in est.split(';'):
                    e = e.strip()
                    if e:
                        estrategias.append(e)
        
        if estrategias:
            estrategias_counts = pd.Series(estrategias).value_counts().reset_index()
            estrategias_counts.columns = ['Estrategia', 'Cantidad']
            
            # Crear gráfico de barras
            fig_estrategias = px.bar(
                estrategias_counts, 
                y='Estrategia', 
                x='Cantidad',
                orientation='h',
                title='Estrategias de Comunicación Utilizadas',
                color='Cantidad',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig_estrategias, use_container_width=True)
            
            # Conclusión
            st.markdown('<div class="conclusion">El "voz a voz" es la estrategia de comunicación predominante, lo que refleja un enfoque tradicional y comunitario. También se utilizan redes sociales y medios visuales como carteleras y volantes, combinando métodos digitales y análogos según el contexto.</div>', unsafe_allow_html=True)
        else:
            st.info("No hay datos suficientes sobre estrategias de comunicación.")
    
    # Observaciones relevantes
    if 'Observaciones3' in df.columns:
        st.markdown('<div class="subsection-header">Observaciones sobre Uso de Tecnología</div>', unsafe_allow_html=True)
        
        observaciones = df['Observaciones3'].dropna().tolist()
        if observaciones:
            for obs in observaciones:
                st.markdown(f'<div style="background-color: #F0F9FF; padding: 10px; border-radius: 5px; margin-bottom: 10px;">{obs}</div>', unsafe_allow_html=True)
            
            # Conclusión sobre observaciones
            st.markdown('<div class="conclusion">Las observaciones reflejan un nivel básico de conocimiento tecnológico, con dependencia frecuente de familiares para tareas ofimáticas complejas. Las estrategias de comunicación combinan métodos tradicionales (voz a voz, carteles) con uso incipiente de herramientas digitales.</div>', unsafe_allow_html=True)
        else:
            st.info("No hay observaciones disponibles sobre uso de tecnología.")
    
    # Conclusión general
    st.markdown("""
    <div class="conclusion">
        <strong>Conclusiones principales sobre uso de tecnología y comunicación:</strong>
        <ul>
            <li>El nivel de adopción tecnológica es básico pero funcional, con predominio de redes sociales como Facebook y WhatsApp.</li>
            <li>Existe una brecha digital que limita el aprovechamiento pleno de herramientas ofimáticas y tecnológicas avanzadas.</li>
            <li>Las estrategias de comunicación combinan métodos tradicionales (voz a voz) con digitales, adaptándose al contexto comunitario.</li>
            <li>Hay un potencial significativo para fortalecer las capacidades tecnológicas como parte del proceso de transformación a centros de desarrollo.</li>
            <li>Se recomienda incluir capacitación en herramientas digitales como parte del plan de fortalecimiento para los CEDECO seleccionados.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
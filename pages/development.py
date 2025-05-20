"""
Módulo que muestra la primera parte de la página de potencial como centro de desarrollo de comedores.
Contiene las secciones de interés y necesidades básicas.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import re

def show_interest_section(df):
    """
    Muestra la sección de interés en convertirse en CEDECO.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    # Verificar columnas relevantes
    interesado_col = 'INTERESADO_COMO_CENTRO_DESARROLLO' if 'INTERESADO_COMO_CENTRO_DESARROLLO' in df.columns else None
    
    # Métricas generales
    if interesado_col:
        total_comedores = len(df)
        interesados = df[interesado_col].apply(lambda x: x == 'SI').sum()
        porcentaje_interesados = round((interesados / total_comedores) * 100) if total_comedores > 0 else 0
        
        # Mostrar métricas de interés
        st.metric(
            "Comedores interesados en convertirse en CEDECO", 
            f"{interesados} de {total_comedores}",
            f"{porcentaje_interesados}%"
        )
        
        # Gráfico de interés
        interes_counts = df[interesado_col].value_counts().reset_index()
        interes_counts.columns = ['Interesado', 'Cantidad']
        
        # Crear gráfico de pastel
        fig_interes = px.pie(
            interes_counts, 
            values='Cantidad', 
            names='Interesado',
            title='Interés en Convertirse en Centro de Desarrollo',
            color_discrete_sequence=['#1E40AF', '#93C5FD']
        )
        
        fig_interes.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_interes, use_container_width=True)
        
        # Conclusión sobre interés
        st.markdown(f"""
        <div class="conclusion">
            El {porcentaje_interesados}% de los comedores evaluados expresan interés en convertirse en Centros de Desarrollo Comunitario, lo que refleja una alta motivación y disposición para ampliar su impacto social más allá de la provisión de alimentos.
        </div>
        """, unsafe_allow_html=True)

def show_needs_section(df):
    """
    Muestra la sección de necesidades para la transformación.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    # Verificar columnas relevantes
    necesidades_col = 'NECESIDADES_QUE_SE_APOYARAN' if 'NECESIDADES_QUE_SE_APOYARAN' in df.columns else None
    otra_necesidad_col = 'OTRA_NECESIDAD' if 'OTRA_NECESIDAD' in df.columns else None
    
    # Análisis de necesidades
    if necesidades_col:
        st.markdown('<div class="subsection-header">Necesidades para la Transformación</div>', unsafe_allow_html=True)
        
        # Procesar los datos para el análisis
        necesidades = []
        for necesidad in df[necesidades_col].dropna():
            if isinstance(necesidad, str):
                for n in re.split(r',|\s+', necesidad):
                    n = n.strip()
                    if n:
                        # Categorizar necesidades
                        if "ALIANZAS" in n.upper() or "ARTICULACION" in n.upper():
                            necesidades.append("Gestión de alianzas estratégicas")
                        elif "FINANCIAMIENTO" in n.upper() or "AREA DE" in n.upper() or "ÁREA DE" in n.upper():
                            necesidades.append("Área de financiamiento")
                        elif "CAPACITACION" in n.upper() or "CAPACITACIÓN" in n.upper() or "FORMACION" in n.upper() or "FORMACIÓN" in n.upper():
                            necesidades.append("Capacitación y formación integral")
                        elif "VISIBILIZACION" in n.upper() or "VISIBILIZACIÓN" in n.upper() or "RECONOCIMIENTO" in n.upper():
                            necesidades.append("Visibilización y reconocimiento")
                        elif "PLANIFICACION" in n.upper() or "PLANIFICACIÓN" in n.upper() or "EVALUACION" in n.upper() or "EVALUACIÓN" in n.upper() or "SEGUIMIENTO" in n.upper():
                            necesidades.append("Procesos de planificación y evaluación")
                        elif "OTRA" in n.upper():
                            necesidades.append("Otras necesidades")
        
        if necesidades:
            # Contar frecuencia de cada necesidad
            necesidades_counts = pd.Series(necesidades).value_counts().reset_index()
            necesidades_counts.columns = ['Necesidad', 'Cantidad']
            
            # Crear gráfico de barras
            fig_necesidades = px.bar(
                necesidades_counts, 
                y='Necesidad', 
                x='Cantidad',
                orientation='h',
                title='Necesidades para la Transformación a CEDECO',
                color='Cantidad',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig_necesidades, use_container_width=True)
            
            # Top necesidades
            top_necesidades = necesidades_counts.sort_values('Cantidad', ascending=False)['Necesidad'].tolist()
            
            # Conclusión
            st.markdown(f"""
            <div class="conclusion">
                Las principales necesidades identificadas para la transformación a CEDECO son:
                <ol>
                    <li>{top_necesidades[0] if len(top_necesidades) > 0 else ''}</li>
                    <li>{top_necesidades[1] if len(top_necesidades) > 1 else ''}</li>
                    <li>{top_necesidades[2] if len(top_necesidades) > 2 else ''}</li>
                </ol>
                Esto sugiere que el fortalecimiento debe centrarse en la gestión institucional, capacidades técnicas y sostenibilidad financiera.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos suficientes sobre necesidades para la transformación.")
    
    # Análisis de otras necesidades específicas
    if otra_necesidad_col:
        st.markdown('<div class="subsection-header">Necesidades Específicas Mencionadas</div>', unsafe_allow_html=True)
        
        # Mostrar otras necesidades mencionadas
        otras_necesidades = df[[otra_necesidad_col, 'NOMBRE_COMEDOR']].dropna(subset=[otra_necesidad_col])
        
        if not otras_necesidades.empty:
            for _, row in otras_necesidades.iterrows():
                if pd.notna(row[otra_necesidad_col]) and row[otra_necesidad_col].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row[otra_necesidad_col]}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                Las necesidades específicas mencionadas muestran un enfoque en el trabajo con poblaciones vulnerables, especialmente mujeres y su empoderamiento económico. Se evidencia una visión que busca trascender la asistencia alimentaria hacia el desarrollo integral de capacidades.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay información detallada sobre necesidades específicas.")
            """
Módulo que muestra la segunda parte de la página de potencial como centro de desarrollo de comedores.
Contiene las secciones de alianzas estratégicas y financiamiento.
"""

import streamlit as st
import pandas as pd

def show_alliances_tab(df):
    """
    Muestra la pestaña de alianzas estratégicas.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    if 'OBSERVACIONES_ALIANZAS_ESTRATEGICAS' in df.columns:
        st.markdown("#### Observaciones sobre Alianzas Estratégicas")
        
        alianzas_obs = df[['OBSERVACIONES_ALIANZAS_ESTRATEGICAS', 'NOMBRE_COMEDOR']].dropna(subset=['OBSERVACIONES_ALIANZAS_ESTRATEGICAS'])
        
        if not alianzas_obs.empty:
            for _, row in alianzas_obs.iterrows():
                if pd.notna(row['OBSERVACIONES_ALIANZAS_ESTRATEGICAS']) and row['OBSERVACIONES_ALIANZAS_ESTRATEGICAS'].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row['OBSERVACIONES_ALIANZAS_ESTRATEGICAS']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                En alianzas estratégicas, se destaca la importancia de fortalecer redes de apoyo social, familiar y de voluntariado. También se menciona la necesidad de mayor acceso a programas gubernamentales y estrategias de la alcaldía.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay observaciones disponibles sobre alianzas estratégicas.")

def show_financing_tab(df):
    """
    Muestra la pestaña de financiamiento.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    if 'OBSERVACIONES_AREA_FINANCIAMIENTO' in df.columns:
        st.markdown("#### Observaciones sobre Área de Financiamiento")
        
        financ_obs = df[['OBSERVACIONES_AREA_FINANCIAMIENTO', 'NOMBRE_COMEDOR']].dropna(subset=['OBSERVACIONES_AREA_FINANCIAMIENTO'])
        
        if not financ_obs.empty:
            for _, row in financ_obs.iterrows():
                if pd.notna(row['OBSERVACIONES_AREA_FINANCIAMIENTO']) and row['OBSERVACIONES_AREA_FINANCIAMIENTO'].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row['OBSERVACIONES_AREA_FINANCIAMIENTO']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                Las necesidades de financiamiento se orientan tanto a emprendimientos que generen sostenibilidad como a equipamiento básico (sillas, mesas) y remuneración para formadores. Esto refleja una visión que equilibra necesidades operativas con desarrollo de capacidades.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay observaciones disponibles sobre área de financiamiento.")

def show_training_tab(df):
    """
    Muestra la pestaña de capacitación.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    if 'OBSERVACIONES_CAPACITACION_INTEGRAL' in df.columns:
        st.markdown("#### Observaciones sobre Capacitación Integral")
        
        capac_obs = df[['OBSERVACIONES_CAPACITACION_INTEGRAL', 'NOMBRE_COMEDOR']].dropna(subset=['OBSERVACIONES_CAPACITACION_INTEGRAL'])
        
        if not capac_obs.empty:
            for _, row in capac_obs.iterrows():
                if pd.notna(row['OBSERVACIONES_CAPACITACION_INTEGRAL']) and row['OBSERVACIONES_CAPACITACION_INTEGRAL'].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row['OBSERVACIONES_CAPACITACION_INTEGRAL']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                Se destaca la importancia del apoyo familiar y de gestoras auxiliares para el funcionamiento del comedor. También se menciona la necesidad de capacitación en emprendimientos y manejo financiero, lo que refleja un interés por fortalecer las capacidades de gestión.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay observaciones disponibles sobre capacitación integral.")

def show_visibility_tab(df):
    """
    Muestra la pestaña de visibilidad.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    if 'OBSERVACIONES_VISIBILIDAD_RECONOCIMIENTO' in df.columns:
        st.markdown("#### Observaciones sobre Visibilidad y Reconocimiento")
        
        visib_obs = df[['OBSERVACIONES_VISIBILIDAD_RECONOCIMIENTO', 'NOMBRE_COMEDOR']].dropna(subset=['OBSERVACIONES_VISIBILIDAD_RECONOCIMIENTO'])
        
        if not visib_obs.empty:
            for _, row in visib_obs.iterrows():
                if pd.notna(row['OBSERVACIONES_VISIBILIDAD_RECONOCIMIENTO']) and row['OBSERVACIONES_VISIBILIDAD_RECONOCIMIENTO'].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row['OBSERVACIONES_VISIBILIDAD_RECONOCIMIENTO']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                Se menciona la importancia del reconocimiento comunitario, especialmente en contextos donde existen actividades de minería ilegal. La visibilidad es clave para fortalecer la legitimidad y aceptación de los comedores en sus territorios.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay observaciones disponibles sobre visibilidad y reconocimiento.")

def show_areas_tabs(df):
    """
    Muestra las pestañas para cada área clave.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="subsection-header">Observaciones por Áreas Clave</div>', unsafe_allow_html=True)
    
    # Crear pestañas para cada área
    tabs = st.tabs([
        "Alianzas Estratégicas", 
        "Financiamiento", 
        "Capacitación", 
        "Visibilidad"
    ])
    
    # Pestaña 1: Alianzas Estratégicas
    with tabs[0]:
        show_alliances_tab(df)
    
    # Pestaña 2: Financiamiento
    with tabs[1]:
        show_financing_tab(df)
    
    # Pestaña 3: Capacitación
    with tabs[2]:
        show_training_tab(df)
    
    # Pestaña 4: Visibilidad
    with tabs[3]:
        show_visibility_tab(df)
        """
Módulo que muestra la tercera parte de la página de potencial como centro de desarrollo de comedores.
Contiene las secciones de planificación y recursos humanos.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import re

def show_planning_tab(df):
    """
    Muestra la pestaña de procesos de planificación.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    if 'OBSERVACIONES_PROCESOS_PLANIFICACIONES' in df.columns:
        st.markdown("#### Observaciones sobre Procesos de Planificación")
        
        plan_obs = df[['OBSERVACIONES_PROCESOS_PLANIFICACIONES', 'NOMBRE_COMEDOR']].dropna(subset=['OBSERVACIONES_PROCESOS_PLANIFICACIONES'])
        
        if not plan_obs.empty:
            for _, row in plan_obs.iterrows():
                if pd.notna(row['OBSERVACIONES_PROCESOS_PLANIFICACIONES']) and row['OBSERVACIONES_PROCESOS_PLANIFICACIONES'].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row['OBSERVACIONES_PROCESOS_PLANIFICACIONES']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                Se identifica la necesidad de asesoría en planificación de actividades para lograr un mayor alcance. Esto refleja un interés por mejorar la gestión estratégica y la organización de los ejes de trabajo del comedor.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay observaciones disponibles sobre procesos de planificación.")

def show_human_resources_tab(df):
    """
    Muestra la pestaña de recursos humanos.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    if 'RECURSO_HUMANO_CON_EL_QUE_CUENTA' in df.columns:
        st.markdown("#### Recurso Humano Disponible")
        
        # Procesar los datos para el análisis
        recursos = []
        for recurso in df['RECURSO_HUMANO_CON_EL_QUE_CUENTA'].dropna():
            if isinstance(recurso, str):
                for r in re.split(r',|\s+', recurso):
                    r = r.strip()
                    if r:
                        # Categorizar recursos
                        if "VOLUNTARIADO" in r.upper():
                            recursos.append("Voluntariado")
                        elif "SOCIAL" in r.upper() or "AMIGOS" in r.upper() or "VECINOS" in r.upper():
                            recursos.append("Red social (amigos, vecinos)")
                        elif "FAMILIAR" in r.upper():
                            recursos.append("Red familiar")
                        elif "COLABORADORES" in r.upper() or "COMEDOR" in r.upper() or "FUNDACIÓN" in r.upper() or "FUNDACION" in r.upper():
                            recursos.append("Colaboradores propios")
        
        if recursos:
            # Contar frecuencia de cada recurso
            recursos_counts = pd.Series(recursos).value_counts().reset_index()
            recursos_counts.columns = ['Tipo de Recurso', 'Cantidad']
            
            # Crear gráfico de barras
            fig_recursos = px.bar(
                recursos_counts, 
                y='Tipo de Recurso', 
                x='Cantidad',
                orientation='h',
                title='Tipos de Recurso Humano Disponibles',
                color='Cantidad',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig_recursos, use_container_width=True)
            
            # Conclusión
            st.markdown("""
            <div class="conclusion">
                Los comedores cuentan principalmente con redes de voluntariado y apoyo social (amigos, vecinos) como recurso humano. Esto muestra un modelo basado en la solidaridad y el compromiso comunitario, pero podría representar desafíos para la sostenibilidad a largo plazo.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos suficientes sobre recurso humano disponible.")
    
    # Observaciones generales sobre recurso humano
    if 'OBSERVACIONES' in df.columns:
        st.markdown("#### Observaciones Generales")
        
        obs_generales = df[['OBSERVACIONES', 'NOMBRE_COMEDOR']].dropna(subset=['OBSERVACIONES'])
        
        if not obs_generales.empty:
            for _, row in obs_generales.iterrows():
                if pd.notna(row['OBSERVACIONES']) and row['OBSERVACIONES'].strip():
                    st.markdown(f"""
                    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>{row['NOMBRE_COMEDOR']}:</strong> {row['OBSERVACIONES']}
                    </div>
                    """, unsafe_allow_html=True)

def show_additional_tabs(df):
    """
    Muestra pestañas adicionales para planificación y recursos humanos.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    tabs = st.tabs([
        "Planificación",
        "Recurso Humano"
    ])
    
    # Pestaña 1: Planificación
    with tabs[0]:
        show_planning_tab(df)
    
    # Pestaña 2: Recurso Humano
    with tabs[1]:
        show_human_resources_tab(df)
        """
Módulo que muestra la cuarta parte de la página de potencial como centro de desarrollo de comedores.
Contiene la matriz de evaluación de potencial y conclusiones generales.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

def create_evaluation_matrix(df):
    """
    Crea una matriz de evaluación del potencial de los comedores para ser CEDECO.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    
    Returns:
        pandas.DataFrame: Dataframe con la evaluación de potencial.
    """
    # Crear un sistema simple de puntuación
    if len(df) > 0:
        # Crear columnas para evaluar cada dimensión
        df_eval = df.copy()
        
        # Dimensión 1: Infraestructura
        df_eval['score_infra'] = df_eval['ESPACIO_TALLERES'].apply(lambda x: 1 if x == 'SI' else 0) if 'ESPACIO_TALLERES' in df_eval.columns else 0
        
        # Dimensión 2: Articulación
        df_eval['score_artic'] = df_eval['ARTICULACION_CON_ORGANIZACIONES'].apply(lambda x: 1 if x == 'SI' else 0) if 'ARTICULACION_CON_ORGANIZACIONES' in df_eval.columns else 0
        
        # Dimensión 3: Participación
        df_eval['score_partic'] = df_eval['PARTICIPACION_ACTIVIDADES'].apply(lambda x: 1 if x == 'SI' else 0) if 'PARTICIPACION_ACTIVIDADES' in df_eval.columns else 0
        
        # Dimensión 4: Tecnología
        df_eval['score_tech'] = df_eval['USO_DE_TIC'].apply(lambda x: 1 if pd.notna(x) and x != '' else 0) if 'USO_DE_TIC' in df_eval.columns else 0
        
        # Dimensión 5: Interés en CEDECO
        df_eval['score_interes'] = df_eval['INTERESADO_COMO_CENTRO_DESARROLLO'].apply(lambda x: 1 if x == 'SI' else 0) if 'INTERESADO_COMO_CENTRO_DESARROLLO' in df_eval.columns else 0
        
        # Calcular puntuación total
        score_cols = [col for col in df_eval.columns if col.startswith('score_')]
        df_eval['score_total'] = df_eval[score_cols].sum(axis=1)
        df_eval['potencial'] = df_eval['score_total'].apply(
            lambda x: 'Alto' if x >= 4 else ('Medio' if x >= 2 else 'Bajo')
        )
        
        return df_eval
    
    return None

def show_evaluation_matrix(df):
    """
    Muestra la matriz de evaluación de potencial.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="subsection-header">Matriz de Evaluación de Potencial</div>', unsafe_allow_html=True)
    
    # Obtener la matriz de evaluación
    df_eval = create_evaluation_matrix(df)
    
    if df_eval is not None:
        # Graficar resultados
        potencial_counts = df_eval['potencial'].value_counts().reset_index()
        potencial_counts.columns = ['Nivel de Potencial', 'Cantidad']
        
        # Asignar colores por nivel
        color_map = {'Alto': '#1E40AF', 'Medio': '#3B82F6', 'Bajo': '#93C5FD'}
        
        # Crear gráfico de barras
        fig_potencial = px.bar(
            potencial_counts,
            x='Nivel de Potencial',
            y='Cantidad',
            title='Evaluación de Potencial como CEDECO',
            color='Nivel de Potencial',
            color_discrete_map=color_map
        )
        
        st.plotly_chart(fig_potencial, use_container_width=True)
        
        # Mostrar tabla detallada
        st.markdown("#### Evaluación Detallada por Comedor")
        
        # Preparar tabla para mostrar
        table_cols = ['NOMBRE_COMEDOR', 'score_infra', 'score_artic', 'score_partic', 'score_tech', 'score_interes', 'score_total', 'potencial']
        table_rename = {
            'NOMBRE_COMEDOR': 'Comedor',
            'score_infra': 'Infraestructura',
            'score_artic': 'Articulación',
            'score_partic': 'Participación',
            'score_tech': 'Tecnología',
            'score_interes': 'Interés',
            'score_total': 'Puntuación Total',
            'potencial': 'Potencial'
        }
        
        df_table = df_eval[table_cols].rename(columns=table_rename)
        
        # Aplicar estilo condicional
        def highlight_potencial(val):
            if val == 'Alto':
                return 'background-color: #DBEAFE; color: #1E40AF; font-weight: bold'
            elif val == 'Medio':
                return 'background-color: #EFF6FF; color: #3B82F6'
            else:
                return ''
        
        # Mostrar tabla con estilo
        st.dataframe(df_table.style.applymap(highlight_potencial, subset=['Potencial']))
        
        # Conclusión
        alto_count = potencial_counts[potencial_counts['Nivel de Potencial'] == 'Alto']['Cantidad'].sum() if 'Alto' in potencial_counts['Nivel de Potencial'].values else 0
        porcentaje_alto = round((alto_count / potencial_counts['Cantidad'].sum()) * 100) if potencial_counts['Cantidad'].sum() > 0 else 0
        
        st.markdown(f"""
        <div class="conclusion">
            El {porcentaje_alto}% de los comedores evaluados muestran un alto potencial para convertirse en Centros de Desarrollo Comunitario, según la matriz de evaluación. Estos comedores ya funcionan como espacios de formación, articulación y participación, más allá de la provisión de alimentos.
        </div>
        """, unsafe_allow_html=True)

def show_general_conclusions():
    """
    Muestra las conclusiones generales sobre el potencial como centro de desarrollo.
    """
    st.markdown("""
    <div class="conclusion">
        <strong>Conclusiones principales sobre potencial como centro de desarrollo:</strong>
        <ul>
            <li>Todos los comedores evaluados expresan interés en convertirse en Centros de Desarrollo Comunitario, mostrando motivación y compromiso con la transformación.</li>
            <li>Las principales necesidades identificadas son gestión de alianzas estratégicas, área de financiamiento y capacitación integral.</li>
            <li>Se observa un enfoque en el trabajo con poblaciones vulnerables, especialmente mujeres, y un interés en trascender la asistencia alimentaria hacia el desarrollo integral.</li>
            <li>Los comedores cuentan principalmente con redes de voluntariado y apoyo social como recurso humano, lo que refleja un modelo basado en la solidaridad comunitaria.</li>
            <li>La mayoría de los comedores evaluados muestra un potencial medio-alto para convertirse en CEDECO, lo que sugiere que el proceso de transformación puede construirse sobre bases ya existentes.</li>
        </ul>
        <strong>Recomendaciones clave:</strong>
        <ul>
            <li>Desarrollar un plan de fortalecimiento focalizado en las necesidades específicas de cada comedor, con énfasis en gestión, financiamiento y capacitación.</li>
            <li>Implementar un programa de acompañamiento técnico que potencie las capacidades existentes y atienda las brechas identificadas.</li>
            <li>Facilitar espacios de articulación con entidades públicas y privadas para ampliar las redes de apoyo y sostenibilidad.</li>
            <li>Visibilizar y reconocer el trabajo de los comedores en sus territorios, fortaleciendo su legitimidad y aceptación comunitaria.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    """
Módulo principal que muestra la página de potencial como centro de desarrollo de comedores.
Integra las diferentes partes del análisis.
"""

def show_development_potential(df):
    """
    Muestra la página de potencial como centro de desarrollo de los comedores.
    
    Args:
        df (pandas.DataFrame): Dataframe con los datos a analizar.
    """
    st.markdown('<div class="section-header">Potencial como Centro de Desarrollo</div>', unsafe_allow_html=True)
    st.markdown("Análisis del potencial de transformación de comedores a centros de desarrollo comunitario")
    
    # Parte 1: Interés y necesidades básicas
    show_interest_section(df)
    show_needs_section(df)
    
    # Parte 2: Análisis por áreas clave (Alianzas, Financiamiento, Capacitación, Visibilidad)
    show_areas_tabs(df)
    
    # Parte 3: Análisis adicionales (Planificación, Recursos Humanos)
    show_additional_tabs(df)
    
    # Parte 4: Matriz de evaluación y conclusiones
    show_evaluation_matrix(df)
    show_general_conclusions()
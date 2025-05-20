"""
Módulo que muestra la página de inicio de la aplicación CEDECO.
"""

import streamlit as st

def show_home_page():
    """
    Muestra la página de inicio con información general sobre el proyecto.
    """
    st.markdown('<div class="section-header">Bienvenido al Dashboard de Análisis CEDECO</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Esta aplicación permite analizar los datos recopilados de las visitas a comedores comunitarios 
    para evaluar su potencial como Centros de Desarrollo Comunitario (CEDECO).
    
    ### Sobre el proyecto CEDECO
    
    El proyecto CEDECO busca transformar comedores comunitarios en centros de desarrollo integral
    que no solo brinden alimentación, sino que también:
    
    - Fortalezcan el tejido social en las comunidades
    - Promuevan actividades formativas y recreativas
    - Faciliten la articulación con entidades gubernamentales y privadas
    - Impulsen iniciativas de emprendimiento y desarrollo económico
    """)
    
    # Crear dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="subsection-header">Metodología</div>', unsafe_allow_html=True)
        st.markdown("""
        El proceso de evaluación para convertir comedores en Centros de Desarrollo Comunitario sigue varias etapas:
        
        1. **Identificación**: Selección inicial de comedores comunitarios
        2. **Visita de evaluación**: Profesionales realizan un diagnóstico in situ
        3. **Análisis de datos**: Procesamiento de la información recopilada (este dashboard)
        4. **Selección de CEDECO**: Designación de comedores con mayor potencial
        5. **Implementación**: Fortalecimiento de capacidades y recursos
        6. **Seguimiento**: Monitoreo de resultados e impacto
        """)
        
    with col2:
        st.markdown('<div class="subsection-header">Cómo utilizar este dashboard</div>', unsafe_allow_html=True)
        st.markdown("""
        En el menú lateral izquierdo, selecciona la sección que deseas analizar:
        
        1. **Información Básica**: Datos generales de los comedores y gestoras
        2. **Infraestructura y Funcionamiento**: Espacios físicos y capacidades
        3. **Historia y Participación**: Trayectoria de los comedores
        4. **Uso de Tecnología**: Herramientas tecnológicas que utilizan
        5. **Financiación y Dificultades**: Recursos y desafíos
        6. **Población Atendida**: Grupos poblacionales beneficiados
        7. **Actividades Realizadas**: Programas y frecuencia
        8. **Potencial de Desarrollo**: Evaluación de oportunidades
        
        Cada sección presenta visualizaciones y conclusiones relevantes para la toma de decisiones.
        """)
    
    # Mostrar información sobre la fuente de datos
    st.markdown('<div class="subsection-header">Fuente de datos</div>', unsafe_allow_html=True)
    st.info("Los datos analizados provienen de las visitas realizadas por profesionales del programa a diferentes comedores comunitarios entre mayo 12-14 de 2025.")
    
    # Mostrar información de contacto o créditos
    st.markdown('<div class="subsection-header">Contacto</div>', unsafe_allow_html=True)
    st.markdown("""
    Para más información sobre el proyecto CEDECO o asistencia técnica con esta aplicación, contacte a:
    
    - Equipo de Desarrollo CEDECO
    - Email: info@cedeco.gov.co
    - Tel: (123) 456-7890
    """)
    
    # Agregar un footer
    st.markdown("---")
    st.markdown("<center>© 2025 Proyecto CEDECO - Todos los derechos reservados</center>", unsafe_allow_html=True)
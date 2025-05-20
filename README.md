# Aplicación de Análisis CEDECO

Dashboard de análisis estadístico para evaluar el potencial de comedores comunitarios como Centros de Desarrollo Comunitario (CEDECO).

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cedeco-dashboard.streamlit.app/)

## 📊 Descripción

Esta aplicación Streamlit visualiza y analiza datos recopilados de comedores comunitarios para evaluar su potencial de transformación en Centros de Desarrollo Comunitario. Proporciona análisis detallado en diferentes dimensiones:

- Información básica y distribución geográfica
- Infraestructura y funcionamiento
- Historia y participación comunitaria
- Uso de tecnología y comunicación
- Financiación y dificultades
- Población atendida
- Actividades realizadas
- Evaluación del potencial de desarrollo

## 🔧 Estructura del Proyecto

```
cedeco-app/
├── main.py                  # Archivo principal
├── .gitignore               # Archivos a ignorar en Git
├── requirements.txt         # Dependencias
├── .streamlit/              
│   └── secrets.toml         # Secretos para Streamlit Cloud (no incluido en Git)
├── utils/
│   └── load_data.py         # Funciones para cargar datos 
└── pages/
    ├── home.py              # Página de inicio
    ├── basic_info.py        # Información básica
    ├── infrastructure.py    # Infraestructura
    ├── history.py           # Historia y participación
    ├── technology.py        # Tecnología
    ├── financing.py         # Financiación
    ├── population.py        # Población
    ├── activities.py        # Actividades
    ├── development.py       # Coordinador de desarrollo
    ├── development_pt1.py   # Parte 1: Interés y necesidades
    ├── development_pt2.py   # Parte 2: Áreas clave
    ├── development_pt3.py   # Parte 3: Planificación
    └── development_pt4.py   # Parte 4: Evaluación
```

## 🛠️ Instalación Local

### Requisitos Previos

- Python 3.7+
- pip (gestor de paquetes de Python)
- Git

### Pasos para Instalar

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/cedeco-app.git
   cd cedeco-app
   ```

2. **Crear un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las credenciales de Google Sheets**:
   
   Opción 1: Crear archivo `credentials.json` en la raíz del proyecto con las credenciales de servicio de Google.
   
   Opción 2: Configurar Streamlit Secrets localmente:
   - Crea la carpeta `.streamlit` en la raíz del proyecto si no existe
   - Dentro de esta carpeta, crea un archivo `secrets.toml` con el siguiente formato:
     ```toml
     [gcp_service_account]
     # Aquí van tus credenciales de servicio de Google Cloud...
     
     [sheets]
     spreadsheet_id = "TU_ID_DE_HOJA_DE_CALCULO"
     ```

5. **Ejecutar la aplicación**:
   ```bash
   streamlit run main.py
   ```

## ☁️ Configuración en Streamlit Cloud

1. **Hacer fork o subir el repositorio a GitHub**:
   - Asegúrate de que el archivo `.gitignore` está configurado para excluir `credentials.json` y otros archivos sensibles.

2. **Crear una nueva aplicación en Streamlit Cloud**:
   - Ve a [share.streamlit.io](https://share.streamlit.io/)
   - Inicia sesión con tu cuenta de GitHub
   - Haz clic en "New app"
   - Selecciona tu repositorio, rama y el archivo principal (`main.py`)

3. **Configurar secretos en Streamlit Cloud**:
   - En la configuración de tu aplicación en Streamlit Cloud, ve a la sección "Secrets"
   - Agrega tus credenciales de servicio de Google y el ID de la hoja de cálculo en formato TOML:
     ```toml
     [gcp_service_account]
     type = "service_account"
     project_id = "tu-proyecto-id"
     private_key_id = "tu-private-key-id"
     private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
     client_email = "tu-service-account@tu-proyecto.iam.gserviceaccount.com"
     client_id = "tu-client-id"
     auth_uri = "https://accounts.google.com/o/oauth2/auth"
     token_uri = "https://oauth2.googleapis.com/token"
     auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
     client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
     universe_domain = "googleapis.com"

     [sheets]
     spreadsheet_id = "tu-spreadsheet-id"
     ```

4. **Implementar la aplicación**:
   - Haz clic en "Deploy!" para implementar tu aplicación
   - Streamlit Cloud se encargará de instalar las dependencias y ejecutar la aplicación

## 🔒 Consideraciones de Seguridad

- **Nunca subas** el archivo `credentials.json` o el directorio `.streamlit` a repositorios públicos
- Usa `.gitignore` para excluir estos archivos sensibles
- Para entornos de producción, considera utilizar variables de entorno o servicios de gestión de secretos

## 📊 Fuente de Datos

La aplicación se conecta a una hoja de cálculo de Google Sheets que contiene datos de comedores comunitarios. En caso de error de conexión, utiliza datos de ejemplo para demostración.

## 🛣️ Roadmap

- [ ] Implementar filtros dinámicos para análisis más detallados
- [ ] Agregar funcionalidad de exportación de informes en PDF
- [ ] Mejorar visualizaciones con mapas geoespaciales detallados
- [ ] Implementar panel administrativo para gestión de datos
- [ ] Crear APIs para integración con otros sistemas

## 👥 Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva característica'`)
4. Sube los cambios a tu fork (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.

## 📞 Contacto

Para cualquier consulta o sugerencia, contáctanos en:
- Email: [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)
- GitHub: [tu-usuario](https://github.com/tu-usuario)
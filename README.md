<img width="1019" height="507" alt="Captura de pantalla 2025-11-25 140505" src="https://github.com/user-attachments/assets/f633f518-8bc1-40a5-99f0-60a9cb6718c4" />

# 🚀 Pro Scraper - Scraper Web Profesional

Este es un proyecto de web scraping avanzado y profesional diseñado para extraer datos del sitio web de práctica `books.toscrape.com`. El scraper navega a través del catálogo de libros, accede a la página de detalles de cada uno para extraer información específica (título, precio y stock) y finalmente guarda los datos recopilados en un archivo CSV.

El proyecto está construido con un enfoque en la robustez, el respeto por el servidor, la mantenibilidad y una experiencia de usuario amigable en la consola.

## ✨ Características Principales

- **Deep Crawling**: Navega por la paginación del catálogo y entra en la página de detalle de cada producto para una extracción profunda.
- **Extracción de Datos Detallada**: Extrae el título, precio y la cantidad exacta de stock disponible de cada libro.
- **Manejo de Errores y Reintentos**: Implementa una lógica de reintentos configurable para manejar fallos en las solicitudes HTTP y aumentar la fiabilidad.
- **Rotación de User-Agents**: Utiliza `fake-useragent` para rotar los User-Agents en cada solicitud, simulando tráfico desde diferentes navegadores y reduciendo la probabilidad de bloqueo.
- **Respeto al Servidor (Politeness)**: Incorpora retrasos aleatorios entre solicitudes para no sobrecargar el servidor de destino.
- **Logging Profesional**: Registra eventos importantes, advertencias y errores tanto en un archivo (`logs/scraper.log`) como en la consola, utilizando `rich` para un formato enriquecido y legible.
- **Exportación de Datos**: Guarda todos los datos extraídos en un archivo `data/processed/books_data.csv` para un fácil análisis y uso posterior.
- **Interfaz de Consola Atractiva**: Emplea la librería `rich` para mostrar barras de progreso, tablas de resumen y logs coloreados, mejorando la experiencia de ejecución.
- **Configuración Centralizada**: Permite modificar fácilmente parámetros clave como la URL de destino, los reintentos y los rangos de espera a través del archivo `config/settings.py`.

## 📂 Estructura del Proyecto

```
Pro_scraper/
│
├── .env                  # (Opcional) Para variables de entorno
├── .gitignore            # Archivos ignorados por Git
├── main.py               # Punto de entrada para ejecutar el scraper
├── requeriments.txt      # Dependencias del proyecto
│
├── config/
│   └── settings.py       # Configuraciones principales del scraper
│
├── data/
│   ├── processed/
│   │   └── books_data.csv  # Archivo de salida con los datos
│   └── raw/              # (Opcional) Para guardar HTML crudo
│
├── logs/
│   └── scraper.log       # Archivo de log
│
└── src/
    ├── scraper.py        # Clase principal con la lógica del scraper
    └── utils.py          # Funciones de utilidad (limpieza de datos, etc.)
```

## 🛠️ Instalación

Sigue estos pasos para configurar el entorno y ejecutar el scraper.

**1. Clonar el Repositorio (Opcional)**

Si estás trabajando desde una copia local, puedes omitir este paso.
```bash
git clone <URL-DEL-REPOSITORIO>
cd Pro_scraper
```

**2. Crear un Entorno Virtual**

Es una buena práctica aislar las dependencias del proyecto.
```bash
python -m venv venv
```
Y activarlo:
- En Windows:
  ```bash
  .\venv\Scripts\activate
  ```
- En macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

**3. Instalar Dependencias**

Instala todas las librerías necesarias desde el archivo `requeriments.txt`.
```bash
pip install -r requeriments.txt
pip install rich # Asegúrate de tener rich también
```

## ▶️ Uso

Para ejecutar el scraper, simplemente corre el archivo `main.py` desde la raíz del proyecto:

```bash
python main.py
```

El script comenzará a procesar las páginas, mostrando el progreso en la consola. Al finalizar, encontrarás los datos en `data/processed/books_data.csv` y un registro detallado en `logs/scraper.log`.

## ⚙️ Configuración

Puedes personalizar el comportamiento del scraper modificando el archivo `config/settings.py`.

- `BASE_URL`: La URL del sitio a scrapear.
- `OUTPUT_FILE`: La ruta del archivo CSV de salida.
- `LOG_FILE`: La ruta del archivo de log.
- `MAX_RETRIES`: Número máximo de reintentos por solicitud.
- `DELAY_RANGE`: Tupla que define el rango (mínimo, máximo) de segundos de espera entre solicitudes.

## 📚 Dependencias

- **requests**: Para realizar las solicitudes HTTP.
- **beautifulsoup4**: Para parsear el contenido HTML.
- **pandas**: Para estructurar y guardar los datos en formato CSV.
- **fake-useragent**: Para generar User-Agents aleatorios.
- **rich**: Para crear interfaces de línea de comandos atractivas.
- **python-dotenv**: Para gestionar variables de entorno (opcional).

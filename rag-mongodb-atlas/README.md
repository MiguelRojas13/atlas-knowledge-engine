# RAG System with MongoDB Atlas

Sistema de Recuperación y Generación Aumentada (RAG) utilizando MongoDB Atlas para búsqueda vectorial e híbrida, con integración a Groq para generación de respuestas.

## Características

- 🔍 **Búsqueda Vectorial**: Embeddings de texto e imágenes con MongoDB Atlas Vector Search
- 🔎 **Búsqueda Híbrida**: Combinación de búsqueda vectorial y full-text search
- 🤖 **Integración con Groq**: Generación de respuestas usando LLMs de alta velocidad
- 📊 **Base de Datos**: MongoDB Atlas con colecciones optimizadas
- 🚀 **API REST**: FastAPI para endpoints de búsqueda y RAG
- 📦 **Gestión de Datos**: Scripts para carga y procesamiento de datos

## Requisitos

- Python 3.9+
- MongoDB Atlas Account
- Groq API Key

## Instalación

### 🚀 Inicio Rápido (Recomendado)

```bash
git clone <repository-url>
cd rag-mongodb-atlas

# Opción 1: Con make (recomendado)
make quickstart

# Opción 2: Con script de gestión
./manage.sh quickstart
```

### 📋 Instalación Manual

```bash
# 1. Clonar y entrar al directorio
git clone <repository-url>
cd rag-mongodb-atlas

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales
cp .env.example .env
# Editar .env con MongoDB URI y Groq API Key

# 5. Inicializar
python scripts/init_db.py
python scripts/load_data.py
python scripts/generate_embeddings.py
```

## Configuración

### MongoDB Atlas

1. Crear un cluster en MongoDB Atlas
2. Obtener la URI de conexión
3. Agregar la URI a `.env`

### Groq API

1. Obtener API key de [Groq](https://groq.com)
2. Agregar la key a `.env`

## Uso

### 🎯 Comandos Profesionales

**Makefile (recomendado):**
```bash
make help              # Ver todos los comandos disponibles
make dev               # Ejecutar en modo desarrollo
make run               # Ejecutar en producción
make test              # Ejecutar tests
make clean             # Limpiar archivos temporales
make security-check    # Verificar seguridad
make status            # Ver estado del proyecto
```

**Script de Gestión:**
```bash
./manage.sh help       # Ver ayuda completa
./manage.sh dev        # Ejecutar servidor en desarrollo
./manage.sh status     # Ver estado del proyecto
./manage.sh stop       # Detener servidor
```

### 🚀 Ejecución Rápida

```bash
# Modo desarrollo (auto-reload)
make dev
# o
./manage.sh dev

# Modo producción
make run
# o
./manage.sh run
```

### 💬 Interfaz de Chat Web

Abre tu navegador en: **http://localhost:8000**

Características de la interfaz:
- ✨ Diseño moderno tipo WhatsApp/Telegram
- 🎯 Sugerencias de preguntas pre-cargadas
- 📊 Muestra fuentes consultadas con % de relevancia
- ⚡ Indicador de "escribiendo..." en tiempo real
- 📱 Responsive (funciona en móvil)

**URLs disponibles:**
- `http://localhost:8000/` - Interfaz de Chat
- `http://localhost:8000/docs` - Swagger UI (API REST)
- `http://localhost:8000/redoc` - ReDoc

### 📝 Comandos Manuales

Si prefieres ejecutar comandos directamente:

```bash
# Activar entorno virtual
source venv/bin/activate

# Inicializar base de datos
python scripts/init_db.py

# Cargar datos
python scripts/load_data.py

# Generar embeddings
python scripts/generate_embeddings.py

# Ejecutar servidor
uvicorn main:app --reload
```

## Endpoints

### Búsqueda
```
POST /api/search
{
  "query": "texto de búsqueda",
  "search_type": "vector|hybrid",
  "limit": 10
}
```

### RAG
```
POST /api/rag
{
  "question": "tu pregunta aquí",
  "context_limit": 5
}
```

## Estructura del Proyecto

```
rag-mongodb-atlas/
├── config/          # Configuración y conexión a BD
├── models/          # Modelos de datos y schemas
├── services/        # Lógica de negocio (embeddings, LLM, RAG)
├── api/             # Endpoints FastAPI
├── data/            # Datos crudos y procesados
├── scripts/         # Scripts de inicialización y carga
├── utils/           # Utilidades y helpers
└── tests/           # Tests unitarios
```

## Tests

```bash
pytest tests/
```

## 🔒 Seguridad

### ⚠️ IMPORTANTE: Protección de Credenciales

Este proyecto maneja información sensible. **NUNCA** subas los siguientes archivos a Git:

- ❌ `.env` - Contiene credenciales reales
- ❌ `*.key` - Archivos de claves
- ❌ `credentials.json` - Credenciales
- ❌ `venv/` - Entorno virtual

### Verificación de Seguridad

Antes de hacer commit, ejecuta:

```bash
./verify_security.sh
```

Este script verifica:
- ✅ Que `.env` esté ignorado
- ✅ Que no haya credenciales en archivos staged
- ✅ Que no haya API keys hardcoded en el código
- ✅ Que archivos sensibles estén protegidos

### Qué hacer si subes credenciales por error

1. **Cambia TODAS las credenciales inmediatamente:**
   - Nueva contraseña en MongoDB Atlas
   - Nuevo API key de Groq

2. **Consulta [SECURITY.md](SECURITY.md)** para más detalles

### Archivos de Seguridad

- 📄 [SECURITY.md](SECURITY.md) - Guía completa de seguridad
- 🔧 [verify_security.sh](verify_security.sh) - Script de verificación
- 📋 [.gitignore](.gitignore) - Archivos ignorados por Git

## Licencia

MIT

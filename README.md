

## 📋 Descripción

Sistema inteligente de preguntas y respuestas que combina el poder de las bases de datos NoSQL con técnicas modernas de inteligencia artificial. Permite realizar consultas en lenguaje natural sobre una base de conocimiento diversa compuesta por documentos de texto e imágenes.

El sistema utiliza búsqueda semántica mediante embeddings vectoriales para encontrar información relevante y genera respuestas contextualizadas usando un modelo de lenguaje de última generación.

---

## ✨ Características

- **Búsqueda Semántica**: Encuentra documentos por significado, no solo por palabras clave
- **Soporte Multimodal**: Procesa y busca tanto texto como imágenes
- **Consultas Híbridas**: Combina filtros tradicionales con similaridad vectorial
- **Pipeline RAG Completo**: Recupera contexto relevante y genera respuestas precisas
- **API REST**: Endpoints documentados con FastAPI y Swagger UI
- **Escalable**: Construido sobre MongoDB Atlas con Vector Search nativo

---

## 🛠️ Tecnologías

| Categoría | Tecnología |
|-----------|------------|
| **Base de Datos** | MongoDB Atlas + Vector Search |
| **Backend** | Python 3.11+ / FastAPI |
| **Embeddings Texto** | sentence-transformers (all-MiniLM-L6-v2) |
| **Embeddings Imágenes** | CLIP (clip-vit-base-patch32) |
| **LLM** | Groq API (Llama 3.1) |
| **Validación** | Pydantic |

---

## 🏗️ Arquitectura

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Usuario       │────▶│   FastAPI        │────▶│  MongoDB Atlas  │
│   (Pregunta)    │     │   /rag /search   │     │  Vector Search  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                         │
                               ▼                         ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │   Groq API       │◀────│   Contexto      │
                        │   (Llama 3.1)    │     │   Recuperado    │
                        └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   Respuesta      │
                        │   Generada       │
                        └──────────────────┘
```

---

## 🚀 Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/[nombre-repo].git
cd [nombre-repo]

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Inicializar base de datos
python scripts/init_db.py

# Cargar datos
python scripts/load_data.py

# Iniciar servidor
uvicorn main:app --reload
```

---

## 📡 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/search` | Búsqueda híbrida o vectorial |
| `POST` | `/rag` | Genera respuesta con contexto RAG |
| `GET` | `/health` | Estado del sistema |
| `GET` | `/docs` | Documentación Swagger UI |

---

## 📊 Casos de Uso

1. **Búsqueda Semántica**: *"¿Qué documentos hablan sobre sostenibilidad ambiental?"*
2. **Filtros Híbridos**: *"Artículos en inglés sobre tecnología publicados en 2024"*
3. **Búsqueda Multimodal**: *"Imágenes similares a esta foto de arquitectura"*
4. **RAG Complejo**: *"Explica las principales tendencias en energías renovables según los documentos"*

---

## 📁 Estructura del Proyecto

```
├── config/          # Configuración y conexión a DB
├── models/          # Schemas y estructuras de datos
├── services/        # Lógica de negocio (embeddings, LLM, RAG)
├── api/             # Endpoints FastAPI
├── scripts/         # Scripts de inicialización
├── data/            # Datos raw y procesados
├── utils/           # Helpers y prompts
└── tests/           # Pruebas unitarias
```

---

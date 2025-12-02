# ✅ Instalación Completada

## Estado del Proyecto

### ✅ Archivos de Configuración
- [x] `.env` creado con tus credenciales
- [x] `.env.example` corregido (sin credenciales)
- [x] `.gitignore` configurado

### ✅ Dependencias
- [x] Entorno virtual creado (`venv/`)
- [x] Todas las dependencias instaladas (FastAPI, PyMongo, Groq, etc.)
- [x] PyTorch y modelos de embeddings descargados

### ✅ Base de Datos MongoDB
- [x] Conexión exitosa a MongoDB Atlas
- [x] Colecciones creadas: `documents` y `images`
- [x] Índices de texto creados
- [x] Índices de tags y fechas creados

### ⏳ Pendiente (Importante)
- [ ] **Crear índices vectoriales en MongoDB Atlas UI** (ver instrucciones abajo)
- [ ] Agregar datos en `data/raw/documents/` y `data/raw/images/`
- [ ] Cargar datos: `python scripts/load_data.py`
- [ ] Generar embeddings: `python scripts/generate_embeddings.py`

---

## 🔍 Crear Índices Vectoriales (IMPORTANTE)

Los índices vectoriales deben crearse manualmente en la UI de MongoDB Atlas:

### Pasos:

1. Ve a [MongoDB Atlas](https://cloud.mongodb.com)
2. Selecciona tu cluster
3. Haz clic en **"Search"** en el menú lateral
4. Clic en **"Create Search Index"**
5. Selecciona **"JSON Editor"**
6. Usa la siguiente configuración:

#### Para la colección `documents`:

**Nombre del índice:** `vector_index`
**Database:** `rag_database`
**Colección:** `documents`

```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "type": "knnVector",
        "dimensions": 384,
        "similarity": "cosine"
      }
    }
  }
}
```

#### Para la colección `images`:

**Nombre del índice:** `vector_index`
**Database:** `rag_database`
**Colección:** `images`

```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "type": "knnVector",
        "dimensions": 384,
        "similarity": "cosine"
      }
    }
  }
}
```

7. Espera a que los índices se construyan (puede tomar unos minutos)

---

## 📦 Próximos Pasos

### 1. Agregar Datos

Coloca tus archivos en:
- `data/raw/documents/` - Archivos JSON, CSV o TXT (mínimo 100)
- `data/raw/images/` - Imágenes JPG, PNG, etc. (mínimo 50)

**Formato recomendado para documentos JSON:**
```json
{
  "title": "Título del documento",
  "content": "Contenido completo del documento...",
  "tags": ["tag1", "tag2"],
  "metadata": {
    "author": "Autor",
    "date": "2024-01-01"
  }
}
```

### 2. Cargar Datos a MongoDB

```bash
source venv/bin/activate
python scripts/load_data.py
```

### 3. Generar Embeddings

```bash
python scripts/generate_embeddings.py
```

### 4. Ejecutar la API

```bash
uvicorn main:app --reload
```

La API estará disponible en: http://localhost:8000

**Documentación interactiva:** http://localhost:8000/docs

---

## 🚀 Uso de la API

### Endpoint de Búsqueda

```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "inteligencia artificial",
    "search_type": "hybrid",
    "limit": 5
  }'
```

### Endpoint RAG

```bash
curl -X POST "http://localhost:8000/api/rag" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Qué es la inteligencia artificial?",
    "context_limit": 5,
    "temperature": 0.7
  }'
```

---

## 📊 Comandos Útiles

### Activar entorno virtual
```bash
source venv/bin/activate
```

### Ejecutar tests
```bash
pytest tests/
```

### Ver logs
```bash
tail -f logs/app.log  # Si configuras logging a archivo
```

### Verificar conexión a MongoDB
```bash
python -c "from config.database import mongodb; mongodb.connect_sync(); print('✅ OK')"
```

---

## 🔧 Troubleshooting

### Error: "No module named 'pydantic_settings'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error de conexión a MongoDB
- Verifica que tu IP esté en Network Access de Atlas
- Verifica usuario y contraseña en `.env`
- Verifica que el cluster esté activo

### Error con Groq API
- Verifica que el API key sea válido
- Verifica que tengas cuota disponible en Groq

---

## 📝 Credenciales Configuradas

### MongoDB
- ✅ URI configurada
- ✅ Usuario: jesus
- ✅ Base de datos: rag_database

### Groq
- ✅ API Key configurada
- ✅ Modelo: mixtral-8x7b-32768

### Embeddings
- ✅ Modelo: sentence-transformers/all-MiniLM-L6-v2
- ✅ Dimensión: 384

---

## 🎯 Estado Actual

```
✅ Proyecto creado
✅ Dependencias instaladas
✅ Base de datos conectada
✅ Colecciones creadas
✅ Índices de texto creados
⏳ Falta crear índices vectoriales en Atlas UI
⏳ Falta agregar datos
⏳ Falta generar embeddings
```

---

**Fecha de instalación:** 2025-12-01
**Versión:** 1.0.0

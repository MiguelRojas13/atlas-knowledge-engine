# Directorio de Datos

Este directorio contiene los datos para el sistema RAG.

## Estructura

### raw/
Datos originales sin procesar

#### raw/documents/
- Documentos de texto en formato JSON, CSV o TXT
- Mínimo requerido: 100 documentos
- Formato JSON recomendado:
```json
{
  "title": "Título del documento",
  "content": "Contenido del documento...",
  "tags": ["tag1", "tag2"],
  "metadata": {
    "author": "Autor",
    "date": "2024-01-01"
  }
}
```

#### raw/images/
- Imágenes en formato JPG, PNG o similar
- Mínimo requerido: 50 imágenes
- Incluir archivos de metadatos correspondientes (JSON)

### processed/
Datos procesados listos para cargar en MongoDB
- Documentos con embeddings generados
- Datos validados y formateados

## Carga de Datos

1. Coloca tus archivos originales en `raw/documents/` y `raw/images/`
2. Ejecuta el script de procesamiento:
   ```bash
   python scripts/load_data.py
   ```
3. Genera embeddings:
   ```bash
   python scripts/generate_embeddings.py
   ```

## Formatos Soportados

- **Documentos**: JSON, CSV, TXT
- **Imágenes**: JPG, PNG, JPEG

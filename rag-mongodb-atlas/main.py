"""
Punto de entrada principal de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path

from config.settings import settings
from config.database import mongodb
from api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    # Startup
    print("\n" + "="*70)
    print("🚀 Iniciando RAG MongoDB Atlas API...")
    print("="*70)

    try:
        await mongodb.connect()

        # Validar conexión con MongoDB
        collection = mongodb.get_collection(settings.DOCUMENTS_COLLECTION)
        doc_count = await collection.count_documents({})

        print(f"\n✅ MongoDB Atlas: CONECTADO")
        print(f"   📊 Base de datos: {settings.MONGODB_DB_NAME}")
        print(f"   📄 Documentos disponibles: {doc_count}")
        print(f"   🌐 Servidor: http://localhost:8000")
        print(f"   📚 Documentación: http://localhost:8000/docs")
        print(f"   💬 Chat Interface: http://localhost:8000")
        print("\n" + "="*70 + "\n")

    except Exception as e:
        print(f"\n❌ Error al conectar con MongoDB: {e}")
        print("   Verifica tus credenciales en el archivo .env")
        print("="*70 + "\n")
        raise

    yield

    # Shutdown
    print("\n" + "="*70)
    print("🛑 Deteniendo servidor...")
    await mongodb.disconnect()
    print("✅ Desconectado de MongoDB")
    print("="*70 + "\n")


app = FastAPI(
    title="RAG MongoDB Atlas API",
    description="Sistema RAG con búsqueda vectorial e híbrida usando MongoDB Atlas",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router, prefix="/api")

# Montar archivos estáticos
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/")
async def root():
    """Servir interfaz de chat"""
    index_path = static_path / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "message": "RAG MongoDB Atlas API",
        "version": "1.0.0",
        "docs": "/docs",
        "chat": "/"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if mongodb.client else "disconnected"
    return {
        "status": "healthy",
        "database": db_status
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

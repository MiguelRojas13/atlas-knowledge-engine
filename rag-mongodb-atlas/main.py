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
    await mongodb.connect()
    print(f"✅ Conectado a MongoDB: {settings.MONGODB_DB_NAME}")

    yield

    # Shutdown
    await mongodb.disconnect()
    print("❌ Desconectado de MongoDB")


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

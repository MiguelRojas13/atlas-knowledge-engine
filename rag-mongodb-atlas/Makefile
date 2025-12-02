.PHONY: help install setup run dev test clean load-data generate-embeddings create-indexes security-check docs

# Variables
PYTHON := python3
VENV := venv
BIN := $(VENV)/bin
ACTIVATE := . $(BIN)/activate

help: ## Muestra esta ayuda
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║           RAG MongoDB Atlas - Comandos Disponibles           ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

install: ## Instalar dependencias
	@echo "📦 Instalando dependencias..."
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt
	@echo "✅ Dependencias instaladas"

setup: install ## Configuración inicial completa
	@echo "🔧 Configurando proyecto..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "⚠️  Archivo .env creado. Por favor configura tus credenciales."; \
	else \
		echo "✅ Archivo .env ya existe"; \
	fi
	$(ACTIVATE) && python scripts/init_db.py
	$(ACTIVATE) && python scripts/create_indexes.py
	@echo "✅ Configuración completada"

run: ## Ejecutar servidor (producción)
	@echo "🚀 Iniciando servidor..."
	$(ACTIVATE) && uvicorn main:app --host 0.0.0.0 --port 8000

dev: ## Ejecutar servidor en modo desarrollo (auto-reload)
	@echo "🔄 Iniciando servidor en modo desarrollo..."
	$(ACTIVATE) && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	$(ACTIVATE) && pytest tests/ -v

clean: ## Limpiar archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	@echo "✅ Limpieza completada"

load-data: ## Cargar datos de ejemplo a MongoDB
	@echo "📊 Cargando datos..."
	$(ACTIVATE) && python scripts/load_data.py

generate-embeddings: ## Generar embeddings para documentos
	@echo "🧠 Generando embeddings..."
	$(ACTIVATE) && python scripts/generate_embeddings.py

create-indexes: ## Crear índices en MongoDB
	@echo "📇 Creando índices..."
	$(ACTIVATE) && python scripts/create_indexes.py

security-check: ## Verificar seguridad del repositorio
	@echo "🔒 Verificando seguridad..."
	@./verify_security.sh

docs: ## Abrir documentación de la API
	@echo "📖 Abriendo documentación..."
	@echo "API Docs: http://localhost:8000/docs"
	@echo "ReDoc: http://localhost:8000/redoc"

status: ## Ver estado de la aplicación
	@echo "📊 Estado de la aplicación:"
	@echo ""
	@if [ -d "$(VENV)" ]; then \
		echo "✅ Entorno virtual: Instalado"; \
	else \
		echo "❌ Entorno virtual: No instalado (ejecuta 'make install')"; \
	fi
	@if [ -f ".env" ]; then \
		echo "✅ Archivo .env: Configurado"; \
	else \
		echo "❌ Archivo .env: No existe (ejecuta 'make setup')"; \
	fi
	@echo ""

quickstart: setup load-data generate-embeddings ## Inicio rápido: configurar + cargar datos + generar embeddings
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║                ✅ CONFIGURACIÓN COMPLETADA                    ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Próximos pasos:"
	@echo "1. Crear índices vectoriales en MongoDB Atlas UI"
	@echo "2. Ejecutar: make dev"
	@echo "3. Abrir: http://localhost:8000/docs"
	@echo ""

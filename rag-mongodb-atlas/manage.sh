#!/bin/bash

# Script de gestión profesional para RAG MongoDB Atlas
# Uso: ./manage.sh [comando]

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
VENV="venv"
PYTHON="python3"

# Funciones auxiliares
print_header() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  $1"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar entorno virtual
check_venv() {
    if [ ! -d "$VENV" ]; then
        print_error "Entorno virtual no encontrado"
        print_info "Ejecuta: ./manage.sh install"
        exit 1
    fi
}

# Activar entorno virtual
activate_venv() {
    check_venv
    source $VENV/bin/activate
}

# Comandos

cmd_help() {
    print_header "RAG MongoDB Atlas - Comandos Disponibles"
    cat << EOF
${GREEN}Instalación y Configuración:${NC}
  install              Instalar dependencias
  setup                Configuración inicial completa
  quickstart           Inicio rápido (todo en uno)

${GREEN}Ejecución:${NC}
  run                  Ejecutar servidor (producción)
  dev                  Ejecutar servidor en desarrollo (auto-reload)
  stop                 Detener servidor

${GREEN}Datos:${NC}
  load-data            Cargar datos de ejemplo
  generate-embeddings  Generar embeddings
  create-indexes       Crear índices en MongoDB

${GREEN}Utilidades:${NC}
  test                 Ejecutar tests
  clean                Limpiar archivos temporales
  security             Verificar seguridad
  status               Ver estado del proyecto
  logs                 Ver logs de la aplicación

${GREEN}Ayuda:${NC}
  help                 Mostrar esta ayuda

${YELLOW}Ejemplos:${NC}
  ./manage.sh quickstart    # Primera vez: configura todo
  ./manage.sh dev           # Desarrollar: inicia servidor
  ./manage.sh status        # Ver estado
EOF
}

cmd_install() {
    print_header "Instalando Dependencias"

    print_info "Creando entorno virtual..."
    $PYTHON -m venv $VENV

    print_info "Actualizando pip..."
    source $VENV/bin/activate
    pip install --upgrade pip -q

    print_info "Instalando dependencias..."
    pip install -r requirements.txt

    print_success "Dependencias instaladas correctamente"
}

cmd_setup() {
    print_header "Configuración Inicial"

    if [ ! -d "$VENV" ]; then
        cmd_install
    fi

    activate_venv

    if [ ! -f ".env" ]; then
        print_info "Creando archivo .env..."
        cp .env.example .env
        print_warning "Configura tus credenciales en .env"
        print_info "MongoDB URI y Groq API Key"
    else
        print_success "Archivo .env ya existe"
    fi

    print_info "Inicializando base de datos..."
    python scripts/init_db.py

    print_info "Creando índices..."
    python scripts/create_indexes.py

    print_success "Configuración completada"
}

cmd_quickstart() {
    print_header "Inicio Rápido - Configuración Completa"

    cmd_setup
    cmd_load_data
    cmd_generate_embeddings

    echo ""
    print_header "✅ CONFIGURACIÓN COMPLETADA"
    echo ""
    print_info "Próximos pasos:"
    echo "  1. Crear índices vectoriales en MongoDB Atlas UI"
    echo "  2. Ejecutar: ./manage.sh dev"
    echo "  3. Abrir: http://localhost:8000/docs"
    echo ""
}

cmd_run() {
    print_header "Iniciando Servidor (Producción)"
    activate_venv
    uvicorn main:app --host 0.0.0.0 --port 8000
}

cmd_dev() {
    print_header "Iniciando Servidor (Desarrollo)"
    activate_venv
    print_success "Servidor corriendo en http://localhost:8000"
    print_info "Documentación: http://localhost:8000/docs"
    print_info "Presiona CTRL+C para detener"
    echo ""
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
}

cmd_stop() {
    print_header "Deteniendo Servidor"
    pkill -f "uvicorn main:app" && print_success "Servidor detenido" || print_info "No hay servidor corriendo"
}

cmd_load_data() {
    print_header "Cargando Datos"
    activate_venv
    python scripts/load_data.py
}

cmd_generate_embeddings() {
    print_header "Generando Embeddings"
    activate_venv
    python scripts/generate_embeddings.py
}

cmd_create_indexes() {
    print_header "Creando Índices"
    activate_venv
    python scripts/create_indexes.py
}

cmd_test() {
    print_header "Ejecutando Tests"
    activate_venv
    pytest tests/ -v --color=yes
}

cmd_clean() {
    print_header "Limpiando Archivos Temporales"

    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.log" -delete
    rm -rf .pytest_cache 2>/dev/null || true

    print_success "Limpieza completada"
}

cmd_security() {
    print_header "Verificación de Seguridad"
    ./verify_security.sh
}

cmd_status() {
    print_header "Estado del Proyecto"

    echo "📊 Componentes:"
    echo ""

    # Entorno virtual
    if [ -d "$VENV" ]; then
        print_success "Entorno virtual instalado"
    else
        print_error "Entorno virtual no instalado (./manage.sh install)"
    fi

    # Archivo .env
    if [ -f ".env" ]; then
        print_success "Archivo .env configurado"
    else
        print_error "Archivo .env no existe (./manage.sh setup)"
    fi

    # Datos
    if [ -d "data/raw/documents" ] && [ "$(ls -A data/raw/documents 2>/dev/null)" ]; then
        print_success "Datos de ejemplo disponibles"
    else
        print_warning "Sin datos de ejemplo"
    fi

    # Servidor
    if pgrep -f "uvicorn main:app" > /dev/null; then
        print_success "Servidor corriendo"
        echo "           http://localhost:8000"
    else
        print_info "Servidor detenido"
    fi

    echo ""
}

cmd_logs() {
    print_header "Logs de la Aplicación"

    if pgrep -f "uvicorn main:app" > /dev/null; then
        print_info "Mostrando logs en tiempo real (CTRL+C para salir)"
        tail -f *.log 2>/dev/null || journalctl -f -u rag-api 2>/dev/null || print_info "No hay archivos de log configurados"
    else
        print_error "El servidor no está corriendo"
    fi
}

# Procesar comando
case "${1:-help}" in
    install)
        cmd_install
        ;;
    setup)
        cmd_setup
        ;;
    quickstart)
        cmd_quickstart
        ;;
    run)
        cmd_run
        ;;
    dev)
        cmd_dev
        ;;
    stop)
        cmd_stop
        ;;
    load-data)
        cmd_load_data
        ;;
    generate-embeddings)
        cmd_generate_embeddings
        ;;
    create-indexes)
        cmd_create_indexes
        ;;
    test)
        cmd_test
        ;;
    clean)
        cmd_clean
        ;;
    security)
        cmd_security
        ;;
    status)
        cmd_status
        ;;
    logs)
        cmd_logs
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        print_error "Comando desconocido: $1"
        echo ""
        cmd_help
        exit 1
        ;;
esac

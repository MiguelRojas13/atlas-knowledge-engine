#!/bin/bash

# Script de verificación de seguridad
# Verifica que no haya credenciales expuestas antes de hacer commit

echo "🔍 Verificando seguridad del repositorio..."
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de errores
ERRORS=0
WARNINGS=0

# 1. Verificar que .env esté ignorado
echo "1️⃣  Verificando .gitignore..."
if git check-ignore .env > /dev/null 2>&1; then
    echo -e "${GREEN}✅ .env está ignorado correctamente${NC}"
else
    echo -e "${RED}❌ ERROR: .env NO está ignorado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 2. Verificar que .env.example NO esté ignorado
if ! git check-ignore .env.example > /dev/null 2>&1; then
    echo -e "${GREEN}✅ .env.example se subirá correctamente${NC}"
else
    echo -e "${RED}❌ ERROR: .env.example está ignorado${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 3. Verificar que venv/ esté ignorado
if git check-ignore venv/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ venv/ está ignorado correctamente${NC}"
else
    echo -e "${YELLOW}⚠️  ADVERTENCIA: venv/ NO está ignorado${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "2️⃣  Verificando archivos staged..."

# 4. Verificar si .env está en staging
if git diff --cached --name-only 2>/dev/null | grep -q "^\.env$"; then
    echo -e "${RED}❌ ERROR: .env está en staging!${NC}"
    echo "   Ejecuta: git reset .env"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ .env no está en staging${NC}"
fi

# 5. Buscar patrones peligrosos en archivos staged
echo ""
echo "3️⃣  Buscando credenciales en archivos staged..."

if git diff --cached 2>/dev/null | grep -qE "(mongodb\+srv://[^<][^/]+|gsk_[a-zA-Z0-9]{40,}|password\s*=\s*['\"][^'\"]+|api_key\s*=\s*['\"][^'\"]+)"; then
    echo -e "${RED}❌ ERROR: Posibles credenciales detectadas en staging!${NC}"
    echo ""
    echo "Patrones encontrados:"
    git diff --cached 2>/dev/null | grep -E "(mongodb\+srv://|gsk_|password|api_key)" --color=always | head -5
    echo ""
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ No se detectaron credenciales en staging${NC}"
fi

# 6. Verificar archivos no trackeados
echo ""
echo "4️⃣  Verificando archivos no trackeados..."

SENSITIVE_FILES=(.env .env.local credentials.json secrets.json *.key *.pem)
for file in "${SENSITIVE_FILES[@]}"; do
    if [ -f "$file" ]; then
        if git check-ignore "$file" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $file existe y está ignorado${NC}"
        else
            echo -e "${RED}❌ ERROR: $file existe pero NO está ignorado${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

# 7. Buscar patrones en TODO el código
echo ""
echo "5️⃣  Buscando hardcoded credentials en código fuente..."

# Buscar en archivos Python
if grep -r "mongodb+srv://" --include="*.py" . --exclude-dir=venv --exclude-dir=.git 2>/dev/null | grep -v ".env.example" | grep -v "SECURITY.md" | grep -q .; then
    echo -e "${YELLOW}⚠️  ADVERTENCIA: Se encontraron referencias a mongodb+srv:// en código${NC}"
    grep -r "mongodb+srv://" --include="*.py" . --exclude-dir=venv --exclude-dir=.git 2>/dev/null | grep -v ".env.example" | grep -v "SECURITY.md"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✅ No se encontraron URIs hardcoded${NC}"
fi

# Buscar API keys hardcoded
if grep -r "gsk_" --include="*.py" . --exclude-dir=venv --exclude-dir=.git 2>/dev/null | grep -v ".env.example" | grep -v "SECURITY.md" | grep -q .; then
    echo -e "${YELLOW}⚠️  ADVERTENCIA: Se encontraron posibles API keys en código${NC}"
    grep -r "gsk_" --include="*.py" . --exclude-dir=venv --exclude-dir=.git 2>/dev/null | grep -v ".env.example" | grep -v "SECURITY.md"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✅ No se encontraron API keys hardcoded${NC}"
fi

# Resumen
echo ""
echo "═══════════════════════════════════════"
echo "📊 RESUMEN"
echo "═══════════════════════════════════════"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ PERFECTO: No se encontraron problemas de seguridad${NC}"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  $WARNINGS advertencia(s) encontrada(s)${NC}"
    echo -e "${GREEN}✅ 0 errores críticos${NC}"
    echo ""
    echo "Puedes continuar pero revisa las advertencias"
    exit 0
else
    echo -e "${RED}❌ $ERRORS error(es) crítico(s) encontrado(s)${NC}"
    echo -e "${YELLOW}⚠️  $WARNINGS advertencia(s)${NC}"
    echo ""
    echo "NO hagas commit hasta resolver los errores"
    exit 1
fi

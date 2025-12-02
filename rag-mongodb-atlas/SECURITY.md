# 🔒 Guía de Seguridad del Proyecto

## ✅ Verificación de Credenciales

### Archivos que NUNCA deben subirse a Git:
- ✅ `.env` - Ignorado por `.gitignore`
- ✅ `*.key` - Archivos de claves
- ✅ `*.pem` - Certificados
- ✅ `credentials.json` - Credenciales
- ✅ `secrets.json` - Secretos
- ✅ `venv/` - Entorno virtual

### Archivos que SÍ deben subirse a Git:
- ✅ `.env.example` - Template sin credenciales reales
- ✅ `requirements.txt` - Dependencias
- ✅ Todo el código fuente (`.py`)

## 🔍 Verificación antes de hacer commit

### Comando para verificar qué se va a subir:
```bash
git status
```

### Comando para verificar si un archivo está ignorado:
```bash
git check-ignore .env
# Si retorna el nombre del archivo, está ignorado (✅ BIEN)

git check-ignore .env.example
# Si no retorna nada, NO está ignorado (✅ BIEN - debe subirse)
```

### Ver qué archivos serían trackeados:
```bash
git add --dry-run .
```

## 🚨 Qué hacer si subes credenciales por error

### Si AÚN NO has hecho push:
```bash
# Remover el archivo del staging
git reset .env

# O deshacer el último commit
git reset --soft HEAD~1
```

### Si YA hiciste push:
1. **Cambiar TODAS las credenciales inmediatamente**
   - Nueva contraseña en MongoDB Atlas
   - Nuevo API key de Groq

2. **Remover el archivo del historial de Git:**
```bash
# Remover del historial (⚠️ DESTRUCTIVO)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

3. **Usar herramientas especializadas:**
```bash
# Instalar BFG Repo-Cleaner
# https://rtyley.github.io/bfg-repo-cleaner/
```

## 🛡️ Protección Adicional

### Pre-commit Hook (Opcional)

Crea el archivo `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Verificar si .env está en staging
if git diff --cached --name-only | grep -q "^.env$"; then
    echo "❌ ERROR: Intentando hacer commit de .env"
    echo "Este archivo contiene credenciales y NO debe subirse a Git"
    exit 1
fi

# Verificar patrones peligrosos en archivos staged
if git diff --cached | grep -E "(MONGODB_URI|GROQ_API_KEY|password|secret|token)" --color=always; then
    echo ""
    echo "⚠️  ADVERTENCIA: Se detectaron posibles credenciales"
    echo "Verifica que no estés commitando información sensible"
    read -p "¿Continuar de todas formas? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

exit 0
```

Hacer ejecutable:
```bash
chmod +x .git/hooks/pre-commit
```

## 📝 Mejores Prácticas

### 1. Variables de Entorno
- ✅ Usar siempre `.env` para credenciales
- ✅ Nunca hardcodear credenciales en el código
- ✅ Proporcionar `.env.example` con valores de ejemplo

### 2. Claves API
- ✅ Rotar claves regularmente
- ✅ Usar diferentes claves para dev/prod
- ✅ Limitar permisos de las claves al mínimo necesario

### 3. MongoDB Atlas
- ✅ Usar autenticación con usuario/contraseña
- ✅ Restringir acceso por IP (Network Access)
- ✅ Usar contraseñas fuertes (mínimo 12 caracteres)
- ✅ Habilitar auditoría de accesos

### 4. Groq API
- ✅ No compartir tu API key
- ✅ Monitorear uso de cuota
- ✅ Revocar keys comprometidas inmediatamente

## 🔍 Checklist antes de cada commit

```bash
□ git status
□ Verificar que .env NO aparece
□ Verificar que no hay API keys en código
□ git diff para revisar cambios
□ Buscar patrones: grep -r "mongodb+srv://" . --exclude-dir=.git
□ git add <archivos específicos>
□ git commit -m "mensaje"
```

## 📋 Verificación del .gitignore actual

```bash
# Ver qué archivos están siendo ignorados
git status --ignored

# Verificar archivos específicos
git check-ignore -v .env
git check-ignore -v venv/
git check-ignore -v *.key
```

## 🚀 Patrones del .gitignore

### Credenciales:
```
.env
.env.local
*.env
!.env.example
*.key
*.pem
credentials.json
secrets.json
```

### Archivos temporales:
```
*.tmp
*.temp
.cache/
```

### Base de datos:
```
*.mongodb
*.db
dump/
```

## ⚠️ Señales de Alerta

Si ves esto en `git status`, **NO** hagas commit:
- ❌ `.env`
- ❌ `credentials.json`
- ❌ `*.key`
- ❌ `config.ini` (si tiene credenciales)
- ❌ Archivos con "secret" o "private" en el nombre

## 📞 Contactos de Emergencia

### Si comprometes credenciales:

**MongoDB Atlas:**
- Cambiar password: Database Access → Edit User
- Regenerar connection string

**Groq:**
- Revocar API key: https://console.groq.com/ → API Keys
- Generar nueva key

## 🔐 Almacenamiento Seguro de Credenciales

### Desarrollo Local:
- ✅ `.env` file (ignorado por git)
- ✅ Variables de entorno del sistema
- ✅ Gestor de contraseñas (1Password, Bitwarden)

### Producción:
- ✅ Variables de entorno del servidor
- ✅ Secrets managers (AWS Secrets Manager, HashiCorp Vault)
- ✅ CI/CD secrets (GitHub Secrets, GitLab CI/CD Variables)

---

**Última actualización:** 2025-12-01
**Revisión recomendada:** Cada 3 meses

# 🔒 Checklist de Seguridad - RAG MongoDB Atlas

## ✅ Estado de Seguridad Actual

### Archivos de Configuración
- [x] `.env` existe y contiene credenciales reales
- [x] `.env` está ignorado por Git (no se subirá)
- [x] `.env.example` existe sin credenciales reales
- [x] `.env.example` se subirá a Git como template

### Protecciones del .gitignore
- [x] 70 patrones de exclusión configurados
- [x] `.env` y todas sus variantes ignoradas
- [x] `venv/` ignorado
- [x] `*.key`, `*.pem` ignorados
- [x] `credentials.json`, `secrets.json` ignorados
- [x] Archivos con `*_secret.*`, `*_private.*` ignorados

### Herramientas de Seguridad
- [x] `SECURITY.md` - Guía completa de seguridad
- [x] `verify_security.sh` - Script de verificación automatizada
- [x] `README.md` actualizado con advertencias de seguridad
- [x] `.gitignore` mejorado con patrones de seguridad

## 📋 Checklist Pre-Commit

Ejecuta esto **ANTES DE CADA COMMIT**:

```bash
□ ./verify_security.sh
□ git status
□ Verificar que .env NO aparece en la lista
□ Verificar que venv/ NO aparece en la lista
□ git diff --cached (revisar cambios)
□ Buscar patrones: grep -r "mongodb+srv://" . --exclude-dir=.git --exclude-dir=venv
□ git add <archivos específicos>
□ git commit -m "mensaje descriptivo"
```

## ⚠️ Archivos PROHIBIDOS en Git

### ❌ NUNCA subir:
- `.env`
- `.env.local`
- `*.key`
- `*.pem`
- `credentials.json`
- `secrets.json`
- `venv/`
- Cualquier archivo con credenciales reales

### ✅ SIEMPRE subir:
- `.env.example` (sin credenciales)
- `requirements.txt`
- Código fuente (`.py`)
- Documentación (`.md`)
- `.gitignore`

## 🚀 Comandos de Verificación Rápida

### Verificar que .env está ignorado:
```bash
git check-ignore .env
# Debe retornar: .env
```

### Ver archivos que se van a subir:
```bash
git status
```

### Ver archivos ignorados:
```bash
git status --ignored
```

### Buscar credenciales en código:
```bash
grep -r "mongodb+srv://" . --exclude-dir=venv --exclude-dir=.git
grep -r "gsk_" . --exclude-dir=venv --exclude-dir=.git
```

## 🔍 Script de Verificación Automática

```bash
./verify_security.sh
```

Este script verifica:
- ✅ `.env` está ignorado
- ✅ No hay credenciales en staging
- ✅ No hay API keys hardcoded
- ✅ Archivos sensibles están protegidos
- ✅ `.env.example` no contiene credenciales

## 🚨 Plan de Emergencia

### Si subes .env a Git por error:

#### 1. ANTES del push:
```bash
# Remover del staging
git reset .env

# O deshacer el commit
git reset --soft HEAD~1
```

#### 2. DESPUÉS del push:
```bash
# 1. Cambiar TODAS las credenciales INMEDIATAMENTE:
#    - MongoDB: Database Access → Edit User → Change Password
#    - Groq: https://console.groq.com → API Keys → Revoke

# 2. Remover del historial:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (⚠️ CUIDADO)
git push origin --force --all

# 4. Limpiar refs
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

## 📊 Estadísticas de Seguridad

### Protecciones Activas:
- **70** patrones en `.gitignore`
- **3** archivos de documentación de seguridad
- **1** script de verificación automatizada
- **0** credenciales en código fuente
- **0** credenciales en `.env.example`

### Archivos Sensibles Protegidos:
```
✅ .env                    (credenciales)
✅ venv/                   (3000+ archivos)
✅ *.key                   (claves)
✅ *.pem                   (certificados)
✅ credentials.json        (credenciales)
✅ secrets.json            (secretos)
```

## 🎯 Mejores Prácticas

### 1. Desarrollo Local
- ✅ Usar `.env` para todas las credenciales
- ✅ Nunca hardcodear credenciales en código
- ✅ Rotar credenciales cada 3-6 meses
- ✅ Usar contraseñas fuertes (16+ caracteres)

### 2. Control de Versiones
- ✅ Ejecutar `./verify_security.sh` antes de commit
- ✅ Usar `git add <archivo>` específicamente (no `git add .`)
- ✅ Revisar `git status` antes de commit
- ✅ Revisar `git diff --cached` antes de commit

### 3. Colaboración
- ✅ Compartir `.env.example` con el equipo
- ✅ Nunca compartir `.env` por email/chat
- ✅ Usar gestores de contraseñas para compartir credenciales
- ✅ Documentar qué credenciales necesita cada desarrollador

## 📝 Log de Cambios de Seguridad

### 2025-12-01
- ✅ Creado `.gitignore` con 70 patrones
- ✅ Creado `SECURITY.md` con guía completa
- ✅ Creado `verify_security.sh` para verificación
- ✅ `.env.example` corregido (sin credenciales)
- ✅ README.md actualizado con sección de seguridad
- ✅ Verificación completa pasada exitosamente

## 🔗 Referencias

- [MongoDB Atlas Security](https://www.mongodb.com/docs/atlas/security/)
- [Groq API Security](https://console.groq.com/docs/security)
- [Git Secrets](https://github.com/awslabs/git-secrets)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

---

**Última verificación:** 2025-12-01
**Estado:** ✅ SEGURO
**Próxima revisión:** 2025-03-01

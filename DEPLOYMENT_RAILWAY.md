# Despliegue en Railway.app

Guía paso a paso para desplegar tu WhatsApp Gym Chatbot en Railway.app.

## 📋 Requisitos Previos

- [ ] Cuenta en [Railway.app](https://railway.app)
- [ ] Repositorio en GitHub
- [ ] Todas las credenciales/API keys (WhatsApp, OpenAI, Google, MySQL)

## 🚀 Pasos de Despliegue

### 1. Preparar el Repositorio

```bash
# Asegúrate de que tienes los archivos necesarios:
# - Dockerfile ✓
# - Procfile ✓
# - requirements.txt ✓
# - .env.example ✓

# Commit de archivos de despliegue
git add Dockerfile Procfile .dockerignore
git commit -m "feat: add deployment files for Railway.app"
git push origin main
```

### 2. Crear Proyecto en Railway.app

1. Ve a [railway.app](https://railway.app) y log in con GitHub
2. Click en **"Create a New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Busca y selecciona tu repositorio `WhatsApp_gym_bot_python`
5. Click en **Deploy**

Railway automáticamente detectará:
- El `Dockerfile` para construir la imagen
- Las variables de entorno que necesitas configurar

### 3. Configurar Variables de Entorno

En el dashboard de Railway:

1. Ve a la pestaña **Variables**
2. Añade todas las variables de tu `.env.example`:

```
NODE_ENV=production
WHATSAPP_PHONE_ID=tu_phone_id
WHATSAPP_BUSINESS_ACCOUNT_ID=tu_business_account_id
WHATSAPP_ACCESS_TOKEN=tu_access_token
WEBHOOK_VERIFY_TOKEN=tu_verify_token
OPENAI_API_KEY=tu_openai_key
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret
GOOGLE_REDIRECT_URI=https://[TU_DOMINIO]/auth/google/callback
GOOGLE_FORMS_ID=tu_google_forms_id
GOOGLE_SHEETS_ID=tu_google_sheets_id
DB_HOST=mysql-activate.alwaysdata.net
DB_USER=activate
DB_PASS=Aluminio$01
DB_NAME=activate_chat
DB_PORT=3306
TIMEOUT_MESSAGE_MINUTES=1
GOOGLE_FORMS_URL=https://forms.gle/YA3UTBm8w3nqvVCe8
```

### 4. Obtener tu Dominio Público

1. En el dashboard de Railway, ve a **Settings**
2. Busca la sección **Domains**
3. Railway te asignará un dominio público automáticamente (ej: `gym-chatbot-production.up.railway.app`)

### 5. Actualizar URLs de Webhooks

Necesitas actualizar los webhooks en Meta (WhatsApp):

1. Ve a [developers.facebook.com](https://developers.facebook.com)
2. En tu aplicación de WhatsApp, busca **Webhooks**
3. Actualiza la URL del webhook a: `https://[TU_DOMINIO]/webhook`
4. Verifica que el `WEBHOOK_VERIFY_TOKEN` coincida

### 6. Verificar el Despliegue

```bash
# Probar el health check
curl https://[TU_DOMINIO]/health

# Deberías recibir:
# {"status":"ok","message":"WhatsApp Gym Chatbot is running","environment":"production"}
```

## 🔍 Monitoreo

En el dashboard de Railway puedes ver:
- **Logs**: Todos los output de la aplicación
- **Metrics**: CPU, memoria, peticiones
- **Deployments**: Historial de despliegues
- **Alerts**: Notificaciones de errores

### Ver logs en tiempo real:
```bash
# Con Railway CLI
railway login
railway link  # Selecciona tu proyecto
railway logs --follow
```

## 🔄 Despliegues Automáticos

Cuando hagas push a la rama `main`:
1. GitHub Actions ejecutará los tests (CI/CD pipeline)
2. Si todo pasa, Railway detectará el cambio
3. Automáticamente construirá la imagen y la desplegará
4. Tu aplicación se actualizará sin downtime

## 📊 Agregar Base de Datos MySQL en Railway (Opcional)

Si quieres migrar a MySQL en Railway en lugar de usar tu servidor actual:

1. En el dashboard del proyecto, click **"Create new"**
2. Selecciona **MySQL**
3. Railway generará automáticamente:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - Variables que se inyectarán en tu app
   
4. Necesitarás migrar tus datos y actualizar los scripts de inicialización

## 🆘 Troubleshooting

### La aplicación falla al iniciar

```bash
# Ver los logs detallados
railroad logs -n 100
```

Causas comunes:
- Variables de entorno faltantes o incorrectas
- Credenciales de API expiradas
- Base de datos no accesible

### Webhook no llega a la aplicación

- Verifica que el dominio sea correcto en Meta
- Asegúrate que `NODE_ENV=production` está configurado
- Revisa los logs de Railway

### Errores de conexión a MySQL

- Prueba la conexión localmente primero
- Verifica que `DB_HOST`, `DB_USER`, `DB_PASS` sea correctos
- Asegúrate que el servidor MySQL está activo

## 📚 Recursos Útiles

- [Documentación de Railway](https://docs.railway.app)
- [Referencia de variables de entorno](https://docs.railway.app/guides/variables)
- [Guía de despliegue](https://docs.railway.app/deploy/deployments)
- [CLI de Railway](https://docs.railway.app/cli/installation)

## ✅ Checklist Antes de Ir a Producción

- [ ] Tests pasan localmente (`pytest -v`)
- [ ] Variables de entorno están todas configuradas en Railway
- [ ] Webhook URL actualizada en Meta
- [ ] Health check retorna 200
- [ ] Logs no muestran errores críticos
- [ ] Base de datos está accesible
- [ ] OpenAI API key es válida
- [ ] WhatsApp Business Account está verificada

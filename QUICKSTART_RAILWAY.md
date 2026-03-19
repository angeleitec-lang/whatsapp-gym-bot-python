# 🚀 Desplegar en Railway en 5 minutos

## Paso 1: Preparar (1 min)

```bash
cd WhatsApp_gym_bot_python

# Commit los nuevos archivos de despliegue
git add Dockerfile Procfile .dockerignore railway.json
git commit -m "Add Railway deployment files"
git push
```

## Paso 2: Crear Proyecto en Railway (2 min)

1. Ve a https://railway.app
2. Login con GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Busca y selecciona tu repo `WhatsApp_gym_bot_python`
5. Click **Deploy**

Railway empezará a construir la imagen automáticamente 🏗️

## Paso 3: Configurar Secretos (2 min)

En el dashboard de Railway, ve a **Variables** y copia-pega esto:

```
NODE_ENV=production
WHATSAPP_PHONE_ID=tu_valor
WHATSAPP_BUSINESS_ACCOUNT_ID=tu_valor
WHATSAPP_ACCESS_TOKEN=tu_valor
WEBHOOK_VERIFY_TOKEN=tu_valor
OPENAI_API_KEY=tu_valor
GOOGLE_CLIENT_ID=tu_valor
GOOGLE_CLIENT_SECRET=tu_valor
GOOGLE_REDIRECT_URI=https://[TU_DOMINIO]/auth/google/callback
GOOGLE_FORMS_ID=tu_valor
GOOGLE_SHEETS_ID=1uCjI9Bl70UEhbGTB3EPZZufHbe89O4H3aanZVbNhD6A
GOOGLE_FORMS_URL=https://forms.gle/YA3UTBm8w3nqvVCe8
DB_HOST=mysql-activate.alwaysdata.net
DB_USER=activate
DB_PASS=Aluminio$01
DB_NAME=activate_chat
DB_PORT=3306
TIMEOUT_MESSAGE_MINUTES=1
```

(Reemplaza `tu_valor` con tus credenciales reales y `[TU_DOMINIO]` con el dominio que Railway te asigna)

## Paso 4: Obtener Dominio y Verificar

1. En Railway, ve a **Settings** → **Domains**
2. Copia tu dominio público (ej: `gym-chatbot-production.up.railway.app`)
3. Prueba que funciona:

```bash
curl https://[TU_DOMINIO]/health
```

Deberías ver:
```json
{"status":"ok","message":"WhatsApp Gym Chatbot is running","environment":"production"}
```

## Paso 5: Actualizar Webhook en WhatsApp

1. Ve a https://developers.facebook.com
2. En tu app de WhatsApp → **Configuration** → **Webhooks**
3. Edita la URL a: `https://[TU_DOMINIO]/webhook`
4. Verifica que el token sea el mismo que en Railway

✅ **¡Listo! Tu bot está en producción**

---

## 📊 Monitorear

- **Logs**: Ve a la pestaña **Deployments** en Railway
- **Errores**: Ve a la pestaña **Logs** para ver output en tiempo real
- **Variables**: Las cambias en **Variables** y se actualizan automáticamente

## 🔄 Actualizar el Código

```bash
# Haz cambios localmente
git add .
git commit -m "Update chatbot logic"
git push

# Railway automáticamente detecta el push y redeploya ✨
```

---

**¿Preguntas?** Ver [DEPLOYMENT_RAILWAY.md](DEPLOYMENT_RAILWAY.md) para documentación completa.

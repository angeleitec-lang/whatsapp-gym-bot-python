# WhatsApp Gym Chatbot - Python Version

Una versión en Python del chatbot inteligente para WhatsApp del gimnasio Activate. Especializado en entrenamientos personalizados de fuerza para personas de 50+ años.

## Características

- **Flask API** con webhooks de WhatsApp
- **Base de datos Q&A** con 33 preguntas frecuentes
- **Integración ChatGPT** para respuestas inteligentes y puntuación de clientes
- **Google Sheets API** para actualización automática de datos
- **Google Forms** con Apps Script para recolección de información
- **MySQL** para logging de mensajes y puntuaciones
- **Tests con pytest**
- **Documentación completa**

## Estructura del Proyecto

```
WhatsApp_gym_bot_python/
├── app.py                      # Aplicación Flask principal
├── config.py                   # Configuración centralizada
├── qa_database.py              # Base de datos Q&A (33 FAQs)
├── chatbot_orchestrator.py     # Orquestador principal
├── whatsapp_service.py         # Servicios de WhatsApp API
├── chatgpt_service.py          # Integración con OpenAI
├── database_service.py         # Operaciones MySQL
├── google_sheets_service.py    # Google Sheets API
├── logger.py                   # Sistema de logging
├── test_qa.py                  # Tests unitarios
├── requirements.txt            # Dependencias Python
├── .env.example                # Plantilla de variables de entorno
├── README.md                   # Este archivo
└── docs/                       # Documentación adicional
```

## Instalación

### 1. Clonar el repositorio

```bash
cd /path/to/WhatsApp_gym_bot_python
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## Configuración de Credenciales

Necesitas obtener las siguientes credenciales:

### WhatsApp Business API

- `WHATSAPP_PHONE_ID`: ID del número de teléfono
- `WHATSAPP_BUSINESS_ACCOUNT_ID`: ID de la cuenta de negocio
- `WHATSAPP_ACCESS_TOKEN`: Token de acceso
- `WEBHOOK_VERIFY_TOKEN`: Token secreto para verificación

### Google Cloud

- `GOOGLE_CLIENT_ID`: ID del cliente OAuth
- `GOOGLE_CLIENT_SECRET`: Secreto del cliente
- `GOOGLE_SHEETS_ID`: ID del Google Sheet

### OpenAI

- `OPENAI_API_KEY`: Clave API de OpenAI

### MySQL

- `DB_HOST`: Host de la base de datos
- `DB_USER`: Usuario de MySQL
- `DB_PASS`: Contraseña de MySQL
- `DB_NAME`: Nombre de la base de datos

## Ejecución

### Desarrollo local

```bash
python app.py
```

El servidor estará disponible en `http://localhost:3000`

### Ejecución con Gunicorn (Producción)

```bash
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

## Tests

Ejecutar tests unitarios:

```bash
pytest test_qa.py -v
```

Ejecutar con cobertura:

```bash
pytest test_qa.py --cov
```

## Endpoints

### Health Check

```
GET /health
```

Verifica que el servidor está activo.

### WhatsApp Webhook

```
GET/POST /webhook
```

Endpoint para recibir y verificar mensajes de WhatsApp.

### Google Forms Submission

```
POST /form-submission
```

Endpoint para recibir datos de formularios de Google Forms.

### Test Endpoints (Desarrollo)

```
POST /test/send-message
POST /test/sheets
POST /test/qa
```

## Flujo de Funcionamiento

1. **Mensaje recibido** → WhatsApp webhook
2. **Verificación** → Token secreto
3. **Q&A Search** → Busca en base de datos
4. **ChatGPT Fallback** → Si no hay coincidencia Q&A
5. **Log a base de datos** → Registro de conversación
6. **Respuesta enviada** → WhatsApp API

### Formulario

1. **Usuario completa formulario** → Google Forms
2. **Apps Script webhook** → Envía datos al servidor
3. **Puntuación con ChatGPT** → 0-100 puntos
4. **Actualiza Google Sheets** → Registro de cliente
5. **Email personalizado** → Se genera pero no se envía automáticamente
6. **Confirmación WhatsApp** → Se notifica al usuario

## Base de Datos

### Tablas requeridas

```sql
-- Mensajes
CREATE TABLE messages (
  id INT PRIMARY KEY AUTO_INCREMENT,
  phone_number VARCHAR(20),
  sender VARCHAR(10),
  message_content TEXT,
  message_type VARCHAR(20),
  created_at TIMESTAMP
);

-- Puntuación de clientes
CREATE TABLE clients_scoring (
  id INT PRIMARY KEY AUTO_INCREMENT,
  phone_number VARCHAR(20),
  client_name VARCHAR(100),
  age INT,
  previous_experience VARCHAR(255),
  physical_problems TEXT,
  physical_perception VARCHAR(255),
  objectives TEXT,
  days_per_week INT,
  training_format VARCHAR(100),
  time_availability VARCHAR(100),
  score INT,
  category VARCHAR(20),
  email_sent BOOLEAN,
  created_at TIMESTAMP
);

-- Sesiones de chat
CREATE TABLE chat_sessions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  phone_number VARCHAR(20),
  client_name VARCHAR(100),
  started_at TIMESTAMP,
  last_activity TIMESTAMP
);
```

## Diferencias con la versión TypeScript

- **Framework**: Flask en lugar de Express.js
- **Runtime**: Python 3.8+ en lugar de Node.js
- **Base de datos**: Mismo MySQL
- **APIs externas**: Google Sheets, OpenAI (igual)
- **Tests**: pytest en lugar de Jest

## Troubleshooting

### Error de conexión a WhatsApp API

- Verifica que el token no ha expirado
- Verifica que el PHONE_ID es correcto
- Verifica que el servidor es accesible desde internet

### Error de autenticación con Google

- Verifica que `credentials.json` existe
- Verifica que los scopes están configurados
- Intenta regenerar el `token.pickle`

### Error de base de datos

- Verifica credenciales de MySQL
- Verifica que la base de datos existe
- Verifica que las tablas están creadas

## Deployment

### Alwaysdata con Python

```bash
# SSH a tu servidor
ssh usuario@servidor

# Clonar repositorio
git clone <tu-repo> WhatsApp_gym_bot_python
cd WhatsApp_gym_bot_python

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de configuración
cp .env.example .env
# Editar .env con credenciales

# Instalar supervisor/systemd
# ... instrucciones específicas por hosting

# Iniciar con gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

## Logs

Los logs se imprimen en consola con el formato:

```
2024-01-15 10:30:45 - app - INFO - Message sent successfully to +34612345678
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto es privado para uso de Activate Gym.

## Soporte

Para soporte técnico, contacta al equipo de desarrollo.

---

**Versión**: 1.0.0  
**Lenguaje**: Python 3.8+  
**Framework**: Flask  
**Base de datos**: MySQL  
**Última actualización**: Marzo 2024

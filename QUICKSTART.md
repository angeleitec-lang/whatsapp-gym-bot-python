# Quick Start - WhatsApp Gym Chatbot (Python)

Empieza a ejecutar el chatbot en 5 minutos.

## 1. Setup Inicial (2 minutos)

```bash
# Navegar al directorio
cd /path/to/WhatsApp_gym_bot_python

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Configurar Credenciales (1 minuto)

```bash
# Copiar plantilla de variables de entorno
cp .env.example .env

# Editar .env con tus credenciales
nano .env  # O abre en tu editor preferido
```

Necesitas:

- `WHATSAPP_PHONE_ID` y `WHATSAPP_ACCESS_TOKEN`
- `OPENAI_API_KEY`
- `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`
- Credenciales de base de datos MySQL

## 3. Ejecutar Tests (1 minuto)

```bash
# Ejecutar tests de Q&A
pytest test_qa.py -v

# Con cobertura
pytest test_qa.py --cov
```

## 4. Iniciar el Servidor (1 minuto)

```bash
# Desarrollo local
python app.py

# El servidor estará en: http://localhost:3000
```

## 5. Verificar que funciona

```bash
# En otra terminal:

# Health check
curl http://localhost:3000/health

# Test Q&A
curl -X POST http://localhost:3000/test/qa \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Es seguro entrenar a los 50 años?"}'
```

## Estructura de Directorios

```
WhatsApp_gym_bot_python/
├── app.py                      # Servidor Flask
├── chatbot_orchestrator.py     # Lógica principal
├── whatsapp_service.py         # API de WhatsApp
├── chatgpt_service.py          # Integración OpenAI
├── database_service.py         # MySQL
├── google_sheets_service.py    # Google Sheets
├── qa_database.py              # 33 FAQs
├── config.py                   # Configuración
├── logger.py                   # Logging
├── test_qa.py                  # Tests
├── requirements.txt            # Dependencias
├── .env.example                # Variables de entorno
├── README.md                   # Documentación completa
└── PYTHON_VERSION_SUMMARY.md  # Resumen versión Python
```

## Endpoints Disponibles

### Health & Info

```
GET /health
```

### WhatsApp

```
GET/POST /webhook
```

### Google Forms

```
POST /form-submission
```

### Testing (Desarrollo)

```
POST /test/send-message
  Body: {"phone_number": "+34...", "message": "Hola"}

POST /test/sheets
  Body: {"nombre": "Juan", "edad": 50, ...}

POST /test/qa
  Body: {"question": "¿Cuáles son los beneficios?"}
```

## Troubleshooting

### Error: "ModuleNotFoundError"

```bash
# Asegúrate que el virtual env está activado
source venv/bin/activate
```

### Error: "Connection refused" (MySQL)

```bash
# Verifica que los datos en .env son correctos:
# DB_HOST, DB_USER, DB_PASS, DB_NAME
```

### Error: "Invalid OpenAI API Key"

```bash
# Verifica que OPENAI_API_KEY está correcto en .env
# La clave debe empezar con "sk-proj-"
```

## Desarrollo

### Ejecutar en modo debug

```python
# En app.py, cambiar la última línea a:
if __name__ == '__main__':
    app.run(debug=True)
```

### Ver logs en tiempo real

```bash
# Los logs se imprimirán automáticamente en consola
# Formato: YYYY-MM-DD HH:MM:SS - module - LEVEL - message
```

### Agregar más Q&A

```python
# Editar qa_database.py y agregar a QA_DATABASE
{
    "category": [
        {
            "question": "Tu pregunta?",
            "answer": "Tu respuesta",
            "keywords": ["palabra1", "palabra2"]
        }
    ]
}
```

## Próximos Pasos

1. **Configurar Google Sheets** - Obtener credenciales OAuth
2. **Configurar Google Forms** - Crear Apps Script webhook
3. **Crear base de datos** - Ejecutar schema.sql en MySQL
4. **Configurar WhatsApp** - Verificar webhook
5. **Deployment** - Ver README para instrucciones

## Stack Tecnológico

- **Framework**: Flask 3.0.0
- **Python**: 3.8+
- **Base de datos**: MySQL 8.0+
- **APIs**: WhatsApp Business, OpenAI GPT-3.5, Google Sheets
- **Testing**: pytest 7.4.3

## Documentación Completa

Para más información, consulta:

- `README.md` - Documentación completa
- `PYTHON_VERSION_SUMMARY.md` - Resumen de la versión Python

---

¡Listo para empezar! 🚀

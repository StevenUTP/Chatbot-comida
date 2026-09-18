# Chatbot de comida peruana (texto + audio con Whisper)

Aplicación en Streamlit que responde preguntas sobre comida peruana, ya sea
escribiendo o cargando un audio (transcrito con el modelo Whisper de OpenAI).

## 1. Preparar el entorno

```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate
# Activar (macOS/Linux)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Configurar la API key

1. Copia `.env.example` y renómbralo a `.env`.
2. Reemplaza `colocar_aqui_la_clave_real` por tu API key de OpenAI.
3. Nunca subas el archivo `.env` a un repositorio (ya está en `.gitignore`).

## 3. Ejecutar

```bash
streamlit run app.py
```

Streamlit abrirá el navegador en `http://localhost:8501`.

## 4. Notas sobre el modelo

El código usa `gpt-4o-mini` por defecto (modelo de chat económico y
ampliamente disponible). Si tu cuenta de OpenAI no tiene acceso a ese modelo,
cambia el valor de `OPENAI_CHAT_MODEL` en `.env` por otro modelo de texto
disponible en tu cuenta (por ejemplo `gpt-4.1-mini` o `gpt-5-mini`), sin
necesidad de tocar `app.py`.

Para la transcripción de audio se usa `whisper-1`, tal como pide la práctica.

## 5. Pruebas sugeridas

| Prueba | Entrada | Resultado esperado |
|---|---|---|
| Texto | ¿Qué ingredientes lleva el ají de gallina? | Responde sobre el plato. |
| Texto | ¿Cuál es el origen del ceviche peruano? | Responde sobre gastronomía peruana. |
| Fuera de alcance | ¿Cómo configuro un router Cisco? | Indica que su especialidad es comida peruana. |
| Audio | Grabar: ¿Cómo se prepara una causa limeña? | Whisper transcribe y el chatbot responde. |
| Contexto | Tras preguntar por el ceviche, escribir "¿qué pescado se recomienda?" | Mantiene el contexto de la conversación. |

## 6. Solución de problemas comunes

- **`ModuleNotFoundError`**: confirma que el entorno virtual está activo y
  vuelve a ejecutar `pip install -r requirements.txt`.
- **`OPENAI_API_KEY no encontrada`**: revisa que el archivo se llame
  exactamente `.env` y esté en la misma carpeta que `app.py`.
- **Error 401 / `invalid_api_key`**: genera una nueva clave en tu cuenta de
  OpenAI y actualiza `.env`.
- **Error de cuota/billing**: revisa el saldo o límites de tu cuenta API.
- **Audio no aceptado**: usa formato mp3, wav, m4a o webm.

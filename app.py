import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
# Modelo configurable desde .env. "gpt-4o-mini" es económico y ampliamente
# disponible. Si tu cuenta tiene acceso a otro modelo (p.ej. gpt-5-mini),
# cambia OPENAI_CHAT_MODEL en el archivo .env sin tocar este código.
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
TRANSCRIBE_MODEL = os.getenv("OPENAI_TRANSCRIBE_MODEL", "whisper-1")

if not API_KEY:
    st.error(
        "No se encontró OPENAI_API_KEY. Verifica que exista un archivo .env "
        "con la línea OPENAI_API_KEY=tu_clave_real."
    )
    st.stop()

client = OpenAI(api_key=API_KEY)

st.set_page_config(
    page_title="Chatbot de comida peruana",
    page_icon="🍲",
    layout="centered",
)

st.title("🍲 Chatbot de comida peruana")
st.caption("Consulta por texto o carga un audio.")

SYSTEM_PROMPT = """
Eres un asistente especializado en gastronomía peruana.
Responde únicamente consultas relacionadas con comida peruana:
platos, ingredientes, regiones, preparación, historia culinaria
y recomendaciones gastronómicas.
Si la pregunta no corresponde al tema, indícalo cordialmente
y orienta al usuario a formular una consulta sobre gastronomía peruana.
Responde en español y con explicaciones claras para estudiantes.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def consultar_chatbot(pregunta: str) -> str:
    """Envía la pregunta (y el historial) al modelo de chat y devuelve la respuesta."""
    historial = [{"role": "system", "content": SYSTEM_PROMPT}]
    historial.extend(st.session_state.messages)
    historial.append({"role": "user", "content": pregunta})

    try:
        respuesta = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=historial,
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return (
            "Ocurrió un error al consultar el modelo. "
            f"Detalle técnico: {e}"
        )


# ---------------------------------------------------------------------------
# Parte 1: entrada por texto
# ---------------------------------------------------------------------------
pregunta = st.chat_input("Escribe una pregunta sobre comida peruana")

if pregunta:
    st.session_state.messages.append({"role": "user", "content": pregunta})

    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Generando respuesta..."):
            respuesta = consultar_chatbot(pregunta)
            st.markdown(respuesta)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})


# ---------------------------------------------------------------------------
# Parte 2: carga y transcripción de audio con Whisper
# ---------------------------------------------------------------------------
st.divider()
st.subheader("🎤 Consulta mediante audio")

audio = st.file_uploader(
    "Carga un audio",
    type=["mp3", "wav", "m4a", "webm"],
)

if audio is not None:
    st.audio(audio)

    if st.button("Transcribir y consultar"):
        extension = audio.name.split(".")[-1]
        ruta_temp = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=f".{extension}"
            ) as archivo_temp:
                archivo_temp.write(audio.getbuffer())
                ruta_temp = archivo_temp.name

            with open(ruta_temp, "rb") as archivo_audio:
                transcripcion = client.audio.transcriptions.create(
                    model=TRANSCRIBE_MODEL,
                    file=archivo_audio,
                    language="es",
                )

            texto = transcripcion.text

            st.success("Audio transcrito correctamente.")
            st.write("**Texto transcrito:**")
            st.write(texto)

            st.session_state.messages.append({"role": "user", "content": texto})

            with st.chat_message("user"):
                st.markdown(f"🎤 {texto}")

            with st.chat_message("assistant"):
                with st.spinner("Generando respuesta..."):
                    respuesta = consultar_chatbot(texto)
                    st.markdown(respuesta)

            st.session_state.messages.append(
                {"role": "assistant", "content": respuesta}
            )

        except Exception as e:
            st.error(f"No se pudo transcribir el audio. Detalle técnico: {e}")

        finally:
            if ruta_temp and os.path.exists(ruta_temp):
                os.remove(ruta_temp)


# ---------------------------------------------------------------------------
# Botón para limpiar la conversación
# ---------------------------------------------------------------------------
st.divider()

if st.button("Limpiar conversación"):
    st.session_state.messages = []
    st.rerun()

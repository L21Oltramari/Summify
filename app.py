import streamlit as st
import moviepy as mp
import whisper
import os
import tempfile
import time
import gc
from transformers import pipeline
from keybert import KeyBERT
import traceback
import logging
from contextlib import contextmanager

# Configuração inicial de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração para uploads grandes
MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1 GB

# Gerenciamento seguro de arquivos temporários
@contextmanager
def temporary_file(suffix):
    """Cria um arquivo temporário e garante que ele seja excluído corretamente."""
    temp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    try:
        yield temp.name
    finally:
        time.sleep(3)  # Aguarda 3 segundos para garantir que os arquivos não estejam mais em uso
        try:
            os.remove(temp.name)
        except PermissionError:
            st.warning(f"⚠️ Não foi possível remover {temp.name}, pois ainda está em uso.")
            logger.warning(f"Não foi possível remover {temp.name} devido a um erro de permissão.")

# Função para extrair áudio de vídeo
def extract_audio(input_path, audio_path):
    try:
        with mp.VideoFileClip(input_path) as video:
            if video.audio is None:
                st.error("❌ O arquivo carregado não contém áudio. Por favor, carregue um arquivo válido.")
                return False
            
            st.info("🎵 Extraindo áudio... (Etapa 1/3)")
            video.audio.write_audiofile(audio_path)
            st.success("✅ Extração de áudio concluída!")
        
        return True
    
    except Exception as e:
        logger.error(f"Erro ao extrair áudio: {e}", exc_info=True)
        st.error(f"❌ Erro ao extrair áudio: {e}")
        traceback.print_exc()
        return False

# Carregamento dos modelos com cache
@st.cache_resource
def load_whisper_model():
    logger.info("Carregando modelo Whisper...")
    return whisper.load_model("base")

@st.cache_resource
def load_summarizer_model():
    logger.info("Carregando modelo de Sumarização...")
    return pipeline("summarization", model="facebook/bart-large-cnn")

@st.cache_resource
def load_topic_extractor():
    logger.info("Carregando modelo de Extração de Tópicos...")
    return KeyBERT()

# Função principal de processamento
def process_content(file, selected_language, max_length, min_length):
    with temporary_file(".mp4" if file.type == "video/mp4" else ".mp3") as input_path, temporary_file(".wav") as audio_path:
        try:
            # Salvar arquivo temporariamente
            with open(input_path, "wb") as f:
                f.write(file.getbuffer())

            # Processar o conteúdo
            process_audio_or_video(input_path, audio_path, selected_language, max_length, min_length)

        except Exception as e:
            logger.error(f"Erro durante o processamento: {e}", exc_info=True)
            st.error(f"❌ Ocorreu um erro durante o processamento. Consulte os logs para mais detalhes.")
            traceback.print_exc()

def process_audio_or_video(input_path, audio_path, selected_language, max_length, min_length):
    # Carregar modelos
    whisper_model = load_whisper_model()
    summarizer = load_summarizer_model()
    topic_extractor = load_topic_extractor()

    # Barra de progresso
    progress_bar = st.progress(0)

    # Passo 1: Extração de áudio (caso seja MP4)
    if input_path.endswith(".mp4"):
        extracted = extract_audio(input_path, audio_path)
        if not extracted:
            st.error("🚫 Ocorreu um erro na extração do áudio.")
            raise Exception("Falha ao extrair áudio")
    else:
        # Se for MP3, apenas copiar para o áudio de trabalho
        os.rename(input_path, audio_path)

    progress_bar.progress(33)

    # Passo 2: Transcrição
    st.info(f"📝 Transcrevendo áudio em {selected_language}... (Etapa 2/3)")
    transcript = whisper_model.transcribe(audio_path, language=language_options[selected_language])
    transcribed_text = transcript["text"]
    
    st.subheader("📜 Texto Transcrito:")
    st.text_area("Resultado:", transcribed_text, height=200)
    st.success("✅ Transcrição concluída!")
    progress_bar.progress(66)

    # Passo 3: Resumo
    st.info("📑 Gerando resumo... (Etapa 3/3)")
    summary = summarizer(transcribed_text, max_length=max_length, min_length=min_length, do_sample=False)
    summary_text = summary[0]['summary_text']

    st.subheader("📌 Resumo:")
    st.markdown(f"💡 **{summary_text}**")
    st.success("✅ Resumo gerado com sucesso!")
    progress_bar.progress(80)

    # Passo 4: Extração de Tópicos
    st.info("📚 Extraindo tópicos principais... (Etapa 4/4)")
    topics = topic_extractor.extract_keywords(transcribed_text, top_n=5)  # Extrai 5 tópicos principais
    topics_list = [topic[0] for topic in topics]  # Lista de tópicos

    st.subheader("🎯 Tópicos Principais:")
    st.markdown("\n".join([f"- **{topic}**" for topic in topics_list]))
    st.success("✅ Extração de tópicos concluída!")
    progress_bar.progress(100)

# Interface do aplicativo
st.title("📹 IA para Transcrição, Resumo e Extração de Tópicos de Áudio/Vídeo")

# Upload do arquivo
uploaded_file = st.file_uploader("🎥 Carregue um arquivo de vídeo (MP4) ou áudio (MP3)", type=["mp4", "mp3"])

# Seleção de idioma
language_options = {
    "Português": "pt",
    "Inglês": "en",
    "Espanhol": "es",
    "Francês": "fr",
    "Alemão": "de",
    "Italiano": "it",
}
selected_language = st.selectbox("🗣️ Selecione o idioma do áudio/vídeo:", list(language_options.keys()))

# Parâmetros configuráveis para sumarização
st.subheader("⚙️ Configurações de Resumo")
max_length = st.slider("Tamanho máximo do resumo", 50, 500, 130)
min_length = st.slider("Tamanho mínimo do resumo", 10, 100, 30)

if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("❌ O arquivo é muito grande. O tamanho máximo permitido é 1 GB.")
    else:
        process_content(uploaded_file, selected_language, max_length, min_length)
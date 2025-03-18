import os
import streamlit as st
import tempfile
from vosk import Model, KaldiRecognizer
import json
import wave
from transformers import pipeline, PegasusTokenizer
from keybert import KeyBERT
import traceback
import logging
from moviepy import VideoFileClip, AudioFileClip


# Desabilita o monitoramento de módulos locais para evitar erros com torch.classes
os.environ["STREAMLIT_DISABLE_LOCAL_MODULES"] = "true"


# Configuração inicial de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuração para uploads grandes
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB


# Carregamento dos modelos com cache
@st.cache_resource
def load_summarizer_model():
    logger.info("Carregando modelo de Sumarização (Pegasus)...")
    # Força o uso do tokenizador lento
    tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-large")
    return pipeline("summarization", model="google/pegasus-large", tokenizer=tokenizer)


@st.cache_resource
def load_topic_extractor():
    logger.info("Carregando modelo de Extração de Tópicos...")
    return KeyBERT()


# Função para extrair áudio de MP4 usando MoviePy
def extract_audio_from_mp4(input_path, output_path):
    try:
        video = VideoFileClip(input_path)
        audio = video.audio
        # Garante que o áudio seja mono e tenha taxa de amostragem de 16kHz
        audio.write_audiofile(output_path, codec="pcm_s16le", fps=16000, ffmpeg_params=["-ac", "1"])
        st.success("✅ Extração de áudio concluída!")
    except Exception as e:
        logger.error(f"Erro ao extrair áudio: {e}", exc_info=True)
        st.error(f"❌ Erro ao extrair áudio: {e}")
        traceback.print_exc()
        raise
    finally:
        # Libera os recursos do MoviePy
        if 'video' in locals():
            video.close()
        if 'audio' in locals():
            audio.close()


# Função para transcrever áudio usando Vosk
def transcribe_audio(audio_path, language_model):
    try:
        # Carrega o modelo de linguagem do Vosk
        model = Model(language_model)
        recognizer = KaldiRecognizer(model, 16000)

        # Abre o arquivo WAV
        with wave.open(audio_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getframerate() != 16000:
                raise ValueError("O áudio deve ser mono e ter taxa de amostragem de 16kHz.")

            transcribed_text = ""
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    transcribed_text += result.get("text", "") + " "

            # Finaliza a transcrição
            final_result = json.loads(recognizer.FinalResult())
            transcribed_text += final_result.get("text", "")

        return transcribed_text.strip()
    except Exception as e:
        logger.error(f"Erro ao transcrever áudio: {e}", exc_info=True)
        st.error(f"❌ Erro ao transcrever áudio: {e}")
        traceback.print_exc()
        raise


# Função para dividir o texto em partes menores
def split_text_into_chunks(text, max_chunk_length=1000):
    """
    Divide o texto em partes menores para processamento.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_chunk_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# Função principal de processamento
def process_content(file, selected_language):
    try:
        # Cria um arquivo temporário para armazenar o áudio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            if file.type == "video/mp4":
                st.info("🎥 Extraindo áudio do vídeo MP4... (Etapa 1/4)")
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
                    temp_video.write(file.getbuffer())
                    video_path = temp_video.name

                # Extrai o áudio do vídeo
                extract_audio_from_mp4(video_path, temp_wav.name)

                # Fecha o arquivo temporário do vídeo e remove-o
                try:
                    os.remove(video_path)
                except PermissionError as e:
                    logger.warning(f"Não foi possível remover o arquivo temporário: {video_path}. Erro: {e}")

            else:
                # Se for MP3, converte diretamente para WAV
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
                    temp_mp3.write(file.getbuffer())
                    mp3_path = temp_mp3.name

                # Converte MP3 para WAV (usando MoviePy)
                audio_clip = AudioFileClip(mp3_path)
                # Garante que o áudio seja mono e tenha taxa de amostragem de 16kHz
                audio_clip.write_audiofile(temp_wav.name, codec="pcm_s16le", fps=16000, ffmpeg_params=["-ac", "1"])
                audio_clip.close()  # Libera os recursos do MoviePy
                os.remove(mp3_path)  # Remove o arquivo temporário de MP3

            audio_path = temp_wav.name

        # Transcreve o áudio
        st.info(f"📝 Transcrevendo áudio em {selected_language}... (Etapa 2/4)")
        transcript = transcribe_audio(audio_path, language_models[selected_language])
        st.subheader("📜 Texto Transcrito:")
        st.text_area("Resultado:", transcript, height=200)
        st.success("✅ Transcrição concluída!")

        # Verifica se o texto transcrito é válido
        if not transcript.strip():
            st.error("❌ O áudio não contém texto reconhecível. Não é possível gerar um resumo.")
            return

        # Carrega os modelos
        summarizer = load_summarizer_model()
        topic_extractor = load_topic_extractor()

        progress_bar = st.progress(0)

        # Divide o texto em partes menores
        st.info("📑 Gerando resumo... (Etapa 3/4)")
        chunks = split_text_into_chunks(transcript, max_chunk_length=1000)  # Ajuste o tamanho do bloco
        summaries = []

        for i, chunk in enumerate(chunks):
            # Verifica se o bloco de texto é válido
            if len(chunk.split()) < 10:  # Ignora blocos muito curtos
                logger.warning(f"Bloco de texto muito curto (ignorado): {chunk}")
                continue

            summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
            summaries.append(summary[0]['summary_text'])
            progress_bar.progress((i + 1) / len(chunks))

        full_summary = " ".join(summaries)

        st.subheader("📌 Resumo Completo:")
        st.markdown(f"💡 *{full_summary}*")
        st.success("✅ Resumo gerado com sucesso!")
        progress_bar.progress(66)

        # Extrai tópicos principais
        st.info("📚 Extraindo tópicos principais... (Etapa 4/4)")
        topics = topic_extractor.extract_keywords(full_summary, top_n=5)
        topics_list = [topic[0] for topic in topics]

        st.subheader("🎯 Tópicos Principais:")
        st.markdown("\n".join([f"- *{topic}*" for topic in topics_list]))
        st.success("✅ Extração de tópicos concluída!")
        progress_bar.progress(100)

    except Exception as e:
        logger.error(f"Erro durante o processamento: {e}", exc_info=True)
        st.error(f"❌ Ocorreu um erro durante o processamento. Consulte os logs para mais detalhes.")
        traceback.print_exc()


# Interface do aplicativo
st.title("🎙️ IA para Transcrição, Resumo e Extração de Tópicos de Áudio/Vídeo")

uploaded_file = st.file_uploader("🎵 Carregue um arquivo de áudio (MP3) ou vídeo (MP4)", type=["mp3", "mp4"])

language_options = {
    "Português": "pt",
    "Inglês": "en",
    "Espanhol": "es",
}
selected_language = st.selectbox("🗣️ Selecione o idioma do áudio/vídeo:", list(language_options.keys()))

# Mapeamento de idiomas para modelos do Vosk (use caminhos absolutos)
language_models = {
    "Português": r"C:\Users\PC\OneDrive\Documentos\GitHub\Summify\static\models\model-pt",
    "Inglês": r"C:\Users\PC\OneDrive\Documentos\GitHub\Summify\static\models\model-en",
    "Espanhol": r"C:\Users\PC\OneDrive\Documentos\GitHub\Summify\static\models\model-es",
}

if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("❌ O arquivo é muito grande. O tamanho máximo permitido é 500 MB.")
    else:
        process_content(uploaded_file, selected_language)
# Summify ️

Summify é uma ferramenta poderosa e fácil de usar para transcrição, resumo e extração de tópicos de arquivos de áudio e vídeo. Utilizando inteligência artificial de ponta e bibliotecas open-source como Vosk, Transformers e KeyBERT, Summify permite que você transforme conteúdo multimídia em texto útil e conciso.

## Funcionalidades Principais ✨

* **Transcrição de Alta Qualidade:** Transcreva áudio e vídeo com precisão usando o modelo Whisper da OpenAI.
* **Resumo Automático:** Obtenha resumos concisos e informativos com o modelo google/pegasus-large , especialmente projetado para documentos longos.
* **Extração de Tópicos Chave:** Identifique os principais temas e palavras-chave com KeyBERT.
* **Suporte Multilíngue:** Transcreva e resuma em vários idiomas, incluindo português, inglês e espanhol (com suporte adicional via modelos do Vosk)
* **Interface Amigável:** Interface simples e intuitiva construída com Streamlit.
* **Processamento de Arquivos Grandes:** Suporta uploads de arquivos de até 500 MB .

## Como Usar 

1.  **Instalação:**
    
    ```bash
    git clone [https://github.com/L21Oltramari/Summify.git](https://www.google.com/search?q=https://github.com/L21Oltramari/Summify.git)
    cd Summify
    pip install -r requirements.txt
    ```
    
2.  **Execução:**
    
    ```bash
    streamlit run app.py
    ```
    
3.  **Acesse o aplicativo no seu navegador:** O Streamlit fornecerá um link local para acessar a interface do Summify.
4.  **Carregue seu arquivo:** Selecione um arquivo de vídeo (MP4) ou áudio (MP3).
5.  **Selecione o idioma:** Escolha o idioma do conteúdo do seu arquivo.
6.  **Clique em "Processar":** Aguarde enquanto o Summify transcreve, resume e extrai os tópicos do seu arquivo.

## Requisitos ⚙️

* Python 3.7+
* Bibliotecas listadas em `requirements.txt` (instaladas via `pip`).
* GPU (opcional, mas recomendada para melhor desempenho com o modelo Pegasus).

## Contribuição 

Contribuições são bem-vindas! Se você tiver sugestões de melhorias ou correções de bugs, por favor, abra uma issue ou envie um pull request.

## Licença 

Este projeto é licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

## Autor ‍

* [L21Oltramari](https://github.com/L21Oltramari)
* [Linkedin](https://www.linkedin.com/in/leonardo-oltramari-317761165/)

## Agradecimentos 

* À equipe da Vosk pelo modelo de transcrição de alta qualidade.
* À equipe da Hugging Face pela biblioteca Transformers e o modelo google/pegasus-large .
* À equipe do KeyBERT pela ferramenta de extração de tópicos.
* A comunidade Streamlit pelo framework de interface web.

## Links Úteis 
 
* [Repositório do projeto](https://github.com/L21Oltramari/Summify)
* [Issues](https://github.com/L21Oltramari/Summify/issues)

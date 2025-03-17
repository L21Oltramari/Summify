📹 IA para Transcrição, Resumo e Extração de Tópicos de Áudio/Vídeo
Este aplicativo utiliza Inteligência Artificial para transcrever áudios/vídeos, gerar resumos do conteúdo transcrito e extrair os tópicos mais importantes discutidos no material. A interface é desenvolvida com Streamlit , e as funcionalidades são alimentadas por modelos avançados de IA como Whisper , BART e KeyBERT .

🚀 Funcionalidades Principais
Transcrição Automática : Converte áudio/vídeo em texto usando o modelo Whisper .
Resumo do Conteúdo : Gera um resumo conciso do texto transcrito com base nos parâmetros configuráveis (tamanho máximo e mínimo).
Extração de Tópicos : Identifica os principais tópicos discutidos no conteúdo utilizando o modelo KeyBERT .
Compatibilidade Multilíngue : Suporta vários idiomas, incluindo português, inglês, espanhol, francês, alemão e italiano.
Interface Amigável : Interface web simples e intuitiva construída com Streamlit .
🛠️ Requisitos e Instalação
Pré-requisitos
Python 3.8 ou superior instalado.
FFmpeg instalado e configurado no sistema (necessário para processamento de áudio/vídeo).
Instalação
Clone o repositório :

1 git clone https://github.com/seu-usuario/nome-do-repositorio.git
2 cd nome-do-repositorio

Crie um ambiente virtual (opcional, mas recomendado) :

1 python -m venv venv

Ative o ambiente virtual:
No Windows:
cmd

1 .\venv\Scripts\activate
No Linux/Mac:
bash

1 source venv/bin/activate
Instale as dependências :
bash

1 pip install -r requirements.txt

Instale o FFmpeg :
No Windows: Baixe e instale o FFmpeg e adicione-o ao PATH.
No Linux:
bash

1 sudo apt install ffmpeg

No Mac:
bash

1 brew install ffmpeg

Execute o aplicativo :
bash
1 streamlit run app.py
📋 Estrutura do Projeto

1 nome-do-repositorio/
2 ├── app.py                  # Código principal do aplicativo
3 ├── README.md               # Documentação do projeto
4 ├── requirements.txt        # Lista de dependências do projeto
5 └── logs/                   # Diretório para armazenar logs (opcional)


🎥 Como Usar
Carregue um arquivo :
Clique no botão "Carregar arquivo" e selecione um vídeo (MP4) ou áudio (MP3).
O tamanho máximo permitido é 1 GB .
Selecione o idioma :
Escolha o idioma do áudio/vídeo na lista suspensa.
Configure os parâmetros de resumo :
Use os sliders para ajustar o tamanho máximo e mínimo do resumo.
Visualize os resultados :
Após o processamento, o aplicativo exibirá:
Texto transcrito : A transcrição completa do áudio/vídeo.
Resumo : Um resumo conciso do conteúdo.
Tópicos principais : Os principais temas discutidos no material.
🔧 Dependências
As seguintes bibliotecas Python são usadas neste projeto:

streamlit: Para criar a interface web.
moviepy: Para extrair áudio de vídeos.
whisper: Para transcrever áudio/vídeo.
transformers: Para gerar resumos usando o modelo BART.
keybert: Para extrair palavras-chave/tópicos.
tempfile: Para gerenciar arquivos temporários.
logging: Para registrar logs detalhados.
Você pode instalar todas as dependências executando:

bash

1 pip install -r requirements.txt

⚙️ Configuração Avançada
Parâmetros Personalizáveis
Tamanho máximo do arquivo : Altere o valor de MAX_FILE_SIZE no código para aumentar ou diminuir o limite de upload.
Modelos de IA : Substitua os modelos whisper, facebook/bart-large-cnn ou KeyBERT por outros modelos compatíveis, se necessário.
Logs
O aplicativo registra logs detalhados para facilitar a depuração. Você pode encontrar os logs no console ou configurar um arquivo de log adicionando:

python

1 logging.basicConfig(filename='logs/app.log', level=logging.INFO)

🌐 Implantação (Deploy)
Você pode implantar este aplicativo em plataformas como:

Streamlit Cloud :
Conecte seu repositório GitHub ao Streamlit Cloud .
O Streamlit cuidará automaticamente do deploy.
Hugging Face Spaces :
Faça upload do código para um repositório no Hugging Face Spaces .
Configure o ambiente conforme as instruções da plataforma.
Heroku/AWS/GCP :
Use serviços de nuvem como Heroku, AWS ou Google Cloud para hospedar o aplicativo.

📝 Licença
Este projeto está licenciado sob a MIT License . Consulte o arquivo LICENSE para obter mais detalhes.

🤝 Contribuição
Contribuições são bem-vindas! Se você deseja melhorar o projeto, siga estas etapas:

Faça um fork do repositório.
Crie uma branch para sua modificação:
bash

1 git checkout -b feature/nova-funcionalidade
Envie um pull request explicando suas alterações.

📞 Contato
Para dúvidas, sugestões ou relatórios de bugs, entre em contato:
E-mail : oltramari515@gmail.com
LinkedIn : https://www.linkedin.com/in/leonardo-oltramari-317761165/
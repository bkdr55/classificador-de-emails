# 📧 Classificador de Emails com IA

Sistema inteligente de classificação e resposta automática de emails desenvolvido para empresas do setor financeiro. Utiliza Inteligência Artificial para classificar emails em **Produtivo** ou **Improdutivo** e gerar respostas automáticas adequadas.

## 🚀 Funcionalidades

- ✅ **Classificação Automática**: Identifica se um email é produtivo (requer ação) ou improdutivo (não requer ação imediata)
- ✅ **Geração de Respostas**: Cria respostas automáticas profissionais baseadas na categoria
- ✅ **Múltiplos Formatos**: Suporta upload de arquivos `.txt` e `.pdf` ou inserção direta de texto
- ✅ **Interface Moderna**: Design responsivo e intuitivo com animações suaves
- ✅ **Histórico**: Armazena as últimas análises realizadas
- ✅ **NLP Avançado**: Pré-processamento de texto com remoção de stop words e lemmatização

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **Transformers (Hugging Face)**: Modelos de IA para classificação
- **NLTK**: Processamento de linguagem natural
- **PyPDF2**: Extração de texto de arquivos PDF
- **OpenAI API**: Para respostas mais sofisticadas

### Frontend
- **HTML5/CSS3**: Interface moderna e responsiva
- **JavaScript (Vanilla)**: Interatividade e comunicação com API
- **Font Awesome**: Ícones
- **Google Fonts (Inter)**: Tipografia moderna

## 📦 Instalação

### Pré-requisitos
- Python 3.11+
- pip

### Passos

1. **Clone o repositório**:
```bash
git clone <seu-repositorio>
cd desafio-oul
```

2. **Crie um ambiente virtual**:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente** (opcional):
Crie um arquivo `.env` na raiz do projeto:
```
OPENAI_API_KEY=sua_chave_aqui
```

5. **Execute a aplicação**:
```bash
python main.py
```

A aplicação estará disponível em `http://localhost:5000`

### Opção 2: Railway

1. Conecte seu repositório ao Railway
2. Configure o comando de start: `gunicorn main:app --bind 0.0.0.0:$PORT`
3. Adicione variáveis de ambiente

## 📋 Como Usar

1. **Acesse a aplicação** através do navegador
2. **Escolha o método de entrada**:
   - **Upload de Arquivo**: Arraste e solte ou clique para selecionar um arquivo `.txt` ou `.pdf`
   - **Inserir Texto**: Cole ou digite o conteúdo do email diretamente
3. **Clique em "Analisar Email"**
4. **Visualize os resultados**:
   - Categoria identificada (Produtivo/Improdutivo)
   - Nível de confiança da classificação
   - Resposta automática sugerida
5. **Copie a resposta** usando o botão de cópia
6. **Acesse o histórico** para ver análises anteriores
7. **Passo a Passo detalhado** acesse `INICIAR.md`

### 📧 Testar com Exemplos

Use os arquivos em `examples/` para testar:
- `examples/email_produtivo.txt` - deve classificar como Produtivo
- `examples/email_improdutivo.txt` - deve classificar como Improdutivo

## 🎯 Categorias de Classificação

### Produtivo
Emails que requerem uma ação ou resposta específica:
- Solicitações de suporte técnico
- Atualizações sobre casos em aberto
- Dúvidas sobre o sistema
- Requisições de informações
- Problemas reportados

### Improdutivo
Emails que não necessitam de uma ação imediata:
- Mensagens de felicitações
- Agradecimentos genéricos
- Cumprimentos
- Mensagens informativas sem solicitação

## 🔧 Arquitetura

```
desafio-oul/
├── main.py              # Backend Flask principal
├── requirements.txt     # Dependências Python
├── README.md            # Documentação principal
├── Triagem.py          # Prompt iniciação ia
├── templates/          # Templates HTML
│   └── index.html       # Interface web
├── static/             # Arquivos estáticos
│   ├── style.css        # Estilos modernos
│   └── script.js        # Lógica frontend
├── tests/              # Scripts de teste
│   ├── test_api.py
│   ├── test_openai_simple.py
│   └── README.md
├── docs/               # Documentação
│   ├── INSTALL.md      # Guia de instalação
│   ├── DEPLOY.md       # Guia de deploy
|   ├── INICIAR.md      # Guia de iniciação do projeto
│   └── configurar_openai.md
├── examples/           # Exemplos de emails
│   ├── email_produtivo.txt
│   └── email_improdutivo.txt
└── uploads/            # Pasta temporária para uploads
```

📁 Veja `ESTRUTURA.md` para detalhes completos da organização do projeto.

## 🧠 Algoritmo de Classificação

O sistema utiliza uma abordagem híbrida:

1. **Pré-processamento NLP**:
   - Tokenização
   - Remoção de stop words
   - Lemmatização
   - Normalização de texto

2. **Classificação**:
   - Análise de palavras-chave específicas
   - Modelo de IA (Hugging Face Transformers)
   - Combinação de resultados para maior precisão

3. **Geração de Resposta**:
   - Templates profissionais (fallback)
   - OpenAI GPT (quando configurado) para respostas mais sofisticadas

## 📝 Licença

Este projeto foi desenvolvido como parte de um desafio técnico.

## 👨‍💻 Autor

Desenvolvido com ❤️ para automatizar a classificação de emails.

---

**Nota**: Para melhor performance, configure uma chave da OpenAI API no arquivo `.env`. Sem ela, o sistema utilizará templates de resposta pré-definidos.

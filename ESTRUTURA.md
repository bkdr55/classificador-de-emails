# 📁 Estrutura do Projeto

## Organização de Pastas

```
desafio-oul/
│
├── 📄 Arquivos Principais
│   ├── main.py              # Backend Flask - aplicação principal
│   ├── requirements.txt     # Dependências Python
│   ├── README.md            # Documentação principal
│   ├── Procfile             # Configuração Heroku
│   ├── runtime.txt          # Versão Python
│   ├── app.json             # Configuração Render
│   ├── .gitignore           # Arquivos ignorados pelo Git
│   ├── iniciar.bat          # Script de inicialização (Windows)
│   └── run.py               # Script alternativo de execução
│
├── 📁 templates/            # Templates HTML
│   └── index.html           # Interface web principal
│
├── 📁 static/              # Arquivos estáticos (CSS, JS)
│   ├── style.css            # Estilos da interface
│   └── script.js            # Lógica JavaScript
│
├── 📁 tests/               # Scripts de teste
│   ├── README.md            # Documentação dos testes
│   ├── test_api.py          # Teste completo da API
│   ├── test_openai_simple.py # Teste simplificado OpenAI
│   ├── test_openai.py       # Teste completo OpenAI
│   ├── test_server.py       # Teste do servidor
│   └── fix_nltk.py          # Fix recursos NLTK
│
├── 📁 docs/                # Documentação
│   ├── INSTALL.md           # Guia de instalação
│   ├── DEPLOY.md            # Guia de deploy
|   ├── INICIAR.md           # Guia de iniciação do projeto
│   └── configurar_openai.md # Configuração OpenAI
│
├── 📁 examples/             # Exemplos de emails
│   ├── README.md            # Documentação dos exemplos
│   ├── email_produtivo.txt  # Email produtivo (exemplo)
│   └── email_improdutivo.txt # Email improdutivo (exemplo)
│
└── 📁 uploads/              # Pasta temporária (criada automaticamente)
    └── (arquivos temporários de upload)
```

## Descrição das Pastas

### 📄 Raiz do Projeto
Contém os arquivos principais de configuração e execução da aplicação.

### 📁 templates/
Templates HTML renderizados pelo Flask. Contém a interface web.

### 📁 static/
Arquivos estáticos servidos diretamente (CSS, JavaScript, imagens).

### 📁 tests/
Todos os scripts de teste do projeto. Execute para validar funcionalidades.

### 📁 docs/
Documentação adicional do projeto (guias, tutoriais, resumos).

### 📁 examples/
Exemplos de emails para testar o classificador.

### 📁 uploads/
Pasta criada automaticamente para armazenar temporariamente arquivos enviados.

## Convenções

- **Arquivos principais**: Na raiz do projeto
- **Testes**: Pasta `tests/`
- **Documentação**: Pasta `docs/`
- **Exemplos**: Pasta `examples/`
- **Templates**: Pasta `templates/`
- **Estáticos**: Pasta `static/`

## Executar Testes

```bash
# Teste da API
python tests/test_api.py

# Teste OpenAI
python tests/test_openai_simple.py
```

## Acessar Documentação

- **Instalação**: `docs/INSTALL.md`
- **Deploy**: `docs/DEPLOY.md`
- **OpenAI**: `docs/configurar_openai.md`

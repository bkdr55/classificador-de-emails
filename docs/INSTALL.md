# 🚀 Guia Rápido de Instalação

## Passo a Passo

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Nota**: A primeira execução pode demorar alguns minutos enquanto o NLTK baixa os recursos necessários e o Hugging Face baixa o modelo de IA.

### 2. Executar a Aplicação

```bash
python main.py
```

### 3. Acessar no Navegador

Abra: `http://localhost:5000`

## ⚙️ Configuração Opcional

### OpenAI API (Para respostas mais sofisticadas)

1. Crie um arquivo `.env` na raiz do projeto
2. Adicione sua chave:
```
OPENAI_API_KEY=sua_chave_aqui
```

**Sem a chave OpenAI**: O sistema funcionará normalmente usando templates de resposta pré-definidos.

## 🌐 Deploy Rápido (Heroku)

1. **Instalar Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Login**:
```bash
heroku login
```

3. **Criar app**:
```bash
heroku create seu-app-nome
```

4. **Deploy**:
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

5. **Abrir app**:
```bash
heroku open
```

## 📝 Testando a Aplicação

### Exemplo de Email Produtivo:
```
Prezados,

Gostaria de solicitar uma atualização sobre o status da minha requisição #12345.
Preciso saber quando será resolvido o problema reportado.

Atenciosamente,
João Silva
```

### Exemplo de Email Improdutivo:
```
Olá,

Desejo um feliz natal e um próspero ano novo para toda a equipe!

Obrigado,
Maria Santos
```

## ⚠️ Solução de Problemas

### Erro: "NLTK data not found"
O NLTK tentará baixar automaticamente. Se falhar, execute:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Erro: "Model not loading"
O modelo do Hugging Face será baixado na primeira execução. Certifique-se de ter conexão com internet.

### Porta já em uso
Altere a porta no `main.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

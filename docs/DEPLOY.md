# 🚀 Guia de Deploy na Nuvem

Este guia apresenta as melhores opções para hospedar sua aplicação gratuitamente.

## 🌟 Opção 1: Render (Recomendado - Mais Fácil)

### Passos:

1. **Acesse**: https://render.com
2. **Crie uma conta** (pode usar GitHub)
3. **Clique em "New +" → "Web Service"**
4. **Conecte seu repositório GitHub**
5. **Configure**:
   - **Name**: `classificador-emails`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app --bind 0.0.0.0:$PORT`
6. **Adicione variáveis de ambiente** (se necessário):
   - `OPENAI_API_KEY`: sua chave (opcional)
7. **Clique em "Create Web Service"**

✅ **Vantagens**: Grátis, fácil, deploy automático

---

## 🌟 Opção 2: Heroku

### Pré-requisitos:
- Conta no Heroku
- Heroku CLI instalado

### Passos:

1. **Instalar Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Login**:
```bash
heroku login
```

3. **Criar aplicação**:
```bash
heroku create seu-app-nome
```

4. **Configurar variáveis** (opcional):
```bash
heroku config:set OPENAI_API_KEY=sua_chave
```

5. **Deploy**:
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

6. **Abrir**:
```bash
heroku open
```

✅ **Vantagens**: Confiável, bem documentado

---

## 🌟 Opção 3: Railway

### Passos:

1. **Acesse**: https://railway.app
2. **Conecte GitHub**
3. **Clique em "New Project" → "Deploy from GitHub repo"**
4. **Selecione seu repositório**
5. **Railway detecta automaticamente** e faz o deploy
6. **Adicione variáveis de ambiente** se necessário

✅ **Vantagens**: Muito fácil, deploy automático

---

## 🌟 Opção 4: Fly.io

### Passos:

1. **Instalar Fly CLI**: https://fly.io/docs/getting-started/installing-flyctl/

2. **Login**:
```bash
fly auth login
```

3. **Criar app**:
```bash
fly launch
```

4. **Deploy**:
```bash
fly deploy
```

✅ **Vantagens**: Boa performance, global

---

## ⚙️ Configurações Importantes

### Porta Dinâmica
O código já está configurado para usar a porta fornecida pelo ambiente:
```python
port = int(os.environ.get('PORT', 5000))
```

### Gunicorn
Para produção, sempre use Gunicorn:
```bash
gunicorn main:app --bind 0.0.0.0:$PORT
```

### Variáveis de Ambiente
- `PORT`: Definida automaticamente pela plataforma
- `OPENAI_API_KEY`: Opcional, para respostas mais sofisticadas

---

## 📝 Checklist de Deploy

- [ ] Código commitado no GitHub
- [ ] `requirements.txt` atualizado
- [ ] `Procfile` criado (para Heroku)
- [ ] `runtime.txt` criado (para Heroku)
- [ ] Variáveis de ambiente configuradas
- [ ] Teste local funcionando
- [ ] Link da aplicação funcionando

---

## 🐛 Solução de Problemas

### Erro: "Application error"
- Verifique os logs: `heroku logs --tail` ou no dashboard
- Certifique-se de que todas as dependências estão no `requirements.txt`

### Erro: "Module not found"
- Verifique se todas as bibliotecas estão listadas
- Execute `pip freeze > requirements.txt` localmente

### Erro: "Port already in use"
- A plataforma define a porta automaticamente
- Não precisa especificar porta no código de produção

### Erro: "NLTK data not found"
- O código baixa automaticamente na primeira execução
- Pode demorar alguns minutos no primeiro deploy

---

## 🎯 Recomendação Final

**Para iniciantes**: Use **Render** - é o mais simples e direto.

**Para projetos profissionais**: Use **Heroku** - mais recursos e documentação.

**Para máxima simplicidade**: Use **Railway** - deploy automático perfeito.

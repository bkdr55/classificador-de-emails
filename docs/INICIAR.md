# 🚀 Como Iniciar o Projeto

## ⚡ Início Rápido (3 passos)

### 1️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

**⏱️ Primeira vez:** Pode demorar 2-5 minutos (baixa modelos de IA)

### 2️⃣ Iniciar o Servidor

**Opção A - Windows (Mais fácil):**
```bash
iniciar.bat
```

**Opção B - Python direto:**
```bash
python main.py
```

**Opção C - Script Python:**
```bash
python run.py
```

### 3️⃣ Acessar no Navegador

Abra: **http://localhost:5000**

---

## 📋 Passo a Passo Detalhado

### Pré-requisitos
- ✅ Python 3.11 ou superior
- ✅ pip instalado
- ✅ Conexão com internet (primeira execução)

### Instalação Completa

1. **Verificar Python:**
```bash
python --version
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Iniciar servidor:**
```bash
python main.py
```

4. **Aguardar mensagens:**
```
Carregando modelos de IA...
Modelo de classificação carregado!
OpenAI não configurado - usando modelo local
🚀 Iniciando servidor Flask...
📡 Servidor será iniciado em: http://localhost:5000
```

5. **Acessar:** http://localhost:5000

---

## 🎯 Testar a Aplicação

### Opção 1: Upload de Arquivo
1. Acesse http://localhost:5000
2. Clique em "Upload de Arquivo"
3. Selecione um arquivo `.txt` ou `.pdf`
4. Clique em "Analisar Email"

### Opção 2: Inserir Texto
1. Acesse http://localhost:5000
2. Clique em "Inserir Texto"
3. Cole ou digite o conteúdo do email
4. Clique em "Analisar Email"

### Exemplos para Testar

**Email Produtivo:**
```
Prezados,

Gostaria de solicitar uma atualização sobre o status da minha requisição #12345.
Preciso saber quando será resolvido o problema reportado.

Atenciosamente,
João Silva
```

**Email Improdutivo:**
```
Olá equipe,

Desejo um feliz natal e um próspero ano novo para toda a equipe!

Obrigado,
Maria Santos
```

---

## ⚙️ Configuração Opcional

### OpenAI API (Respostas mais sofisticadas)

1. Crie arquivo `.env` na raiz:
```
OPENAI_API_KEY=sua_chave_aqui
```

2. Reinicie o servidor

**Sem OpenAI:** Sistema funciona normalmente com templates.

---

## 🛑 Parar o Servidor

No terminal onde o servidor está rodando:
- Pressione **Ctrl + C**

---

## ⚠️ Problemas Comuns

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Porta 5000 já em uso"
- Feche outros programas usando a porta
- Ou altere a porta no `main.py`

### "NLTK data not found"
O sistema baixa automaticamente. Se falhar:
```bash
python tests/fix_nltk.py
```

### Servidor não inicia
1. Verifique se Python está instalado: `python --version`
2. Verifique se dependências estão instaladas: `pip list`
3. Veja os erros no terminal

---

## 📚 Mais Informações

- **Instalação detalhada:** `docs/INSTALL.md`
- **Deploy na nuvem:** `docs/DEPLOY.md`
- **Estrutura do projeto:** `ESTRUTURA.md`

---

## ✅ Checklist de Início

- [ ] Python 3.11+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Servidor iniciado (`python main.py`)
- [ ] Acessou http://localhost:5000
- [ ] Testou com um email

**Pronto! 🎉**

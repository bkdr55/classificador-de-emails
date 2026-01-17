# 🧪 Testes

Esta pasta contém todos os scripts de teste do projeto.

## Arquivos

### `test_api.py`
Teste completo da API REST:
- Health check
- Classificação com texto
- Classificação com arquivo

**Uso:**
```bash
python tests/test_api.py
```

### `test_openai_simple.py`
Teste simplificado da integração com OpenAI:
- Verifica configuração da OpenAI
- Testa geração de respostas
- Compara respostas com/sem OpenAI

**Uso:**
```bash
python tests/test_openai_simple.py
```

### `test_openai.py`
Teste completo da integração OpenAI (versão detalhada).

**Uso:**
```bash
python tests/test_openai.py
```

### `test_server.py`
Script para testar e iniciar o servidor com tratamento de erros.

**Uso:**
```bash
python tests/test_server.py
```

### `fix_nltk.py`
Script para baixar todos os recursos necessários do NLTK.

**Uso:**
```bash
python tests/fix_nltk.py
```

## Executar Todos os Testes

```bash
# Teste básico da API
python tests/test_api.py

# Teste da OpenAI
python tests/test_openai_simple.py
```

## Requisitos

Certifique-se de que o servidor está rodando antes de executar os testes:

```bash
python main.py
```

Ou em outro terminal:
```bash
python tests/test_server.py
```

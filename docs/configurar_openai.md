# 🔑 Como Configurar a OpenAI API

## Status Atual
- ❌ OpenAI não está configurada no servidor
- ✅ Aplicação funciona com templates padrão

## Opção 1: Arquivo .env (Recomendado)

1. **Crie um arquivo `.env` na raiz do projeto** com:
```
OPENAI_API_KEY=sua_chave_aqui
```

2. **Reinicie o servidor** para carregar a chave

## Opção 2: Variável de Ambiente do Sistema

No PowerShell:
```powershell
$env:OPENAI_API_KEY = "sua_chave_aqui"
python main.py
```

## Opção 3: Variável de Ambiente Permanente (Windows)

1. Abra "Variáveis de Ambiente" no Windows
2. Adicione `OPENAI_API_KEY` com sua chave
3. Reinicie o servidor

## Como Obter uma Chave da OpenAI

1. Acesse: https://platform.openai.com/api-keys
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave gerada

## Testar se Está Funcionando

Execute:
```bash
python test_openai_simple.py
```

Ou verifique o health check:
```bash
curl http://localhost:5000/api/health
```

Se `openai_configured: true`, está funcionando!

## Diferença entre Respostas

- **Template Padrão**: Respostas pré-definidas, mais curtas
- **OpenAI GPT**: Respostas geradas dinamicamente, mais elaboradas e contextuais

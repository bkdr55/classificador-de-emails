"""
Script simples para testar OpenAI API
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("TESTE DA INTEGRACAO OPENAI")
print("=" * 60)

# Verificar chave
key = os.getenv('OPENAI_API_KEY')
if key:
    masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
    print(f"\nChave OpenAI encontrada: {masked}")
else:
    print("\nAVISO: Chave OpenAI nao encontrada no .env")

# Testar health
print("\n[1/3] Testando health check...")
try:
    r = requests.get(f"{BASE_URL}/api/health", timeout=5)
    health = r.json()
    print(f"   Status: {health['status']}")
    print(f"   Classificador IA: {health['classifier_loaded']}")
    print(f"   OpenAI Configurado: {health['openai_configured']}")
    openai_ok = health['openai_configured']
except Exception as e:
    print(f"   ERRO: {e}")
    openai_ok = False

# Testar classificação
print("\n[2/3] Testando classificacao...")
email = """Prezados,

Gostaria de solicitar uma atualizacao urgente sobre o status da minha requisicao #12345.
O problema reportado ainda nao foi resolvido e esta afetando minhas operacoes.

Preciso de uma resposta o quanto antes.

Atenciosamente,
Joao Silva"""

try:
    r = requests.post(
        f"{BASE_URL}/api/classify",
        json={"text": email},
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    if r.status_code == 200:
        data = r.json()
        print(f"   Categoria: {data['category']}")
        print(f"   Confianca: {data['confidence']}%")
        print(f"\n[3/3] Resposta gerada ({len(data['response'])} caracteres):")
        print("   " + "-" * 56)
        for line in data['response'].split('\n'):
            if line.strip():
                print(f"   {line}")
        print("   " + "-" * 56)
        
        # Verificar se parece ser da OpenAI
        if len(data['response']) > 250 and 'Prezado' in data['response']:
            print("\n>>> RESPOSTA LONGA - Provavelmente da OpenAI!")
        else:
            print("\n>>> RESPOSTA CURTA - Usando template padrao")
        
        if openai_ok:
            print("\n>>> OpenAI esta configurada e funcionando!")
        else:
            print("\n>>> AVISO: OpenAI nao esta configurada no servidor")
            print("   Reinicie o servidor apos criar o arquivo .env")
    else:
        print(f"   ERRO: {r.status_code}")
        print(f"   {r.text}")
except Exception as e:
    print(f"   ERRO: {e}")

print("\n" + "=" * 60)

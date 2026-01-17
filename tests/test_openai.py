"""
Script para testar a integração com OpenAI API
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000"

def test_health():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check OK")
            print(f"   Status: {data['status']}")
            print(f"   Classificador IA: {data['classifier_loaded']}")
            print(f"   OpenAI Configurado: {data['openai_configured']}")
            return data['openai_configured']
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def test_classify_with_openai():
    """Testa classificação com email produtivo"""
    print("\n" + "=" * 60)
    print("📧 TESTE 1: Email Produtivo")
    print("=" * 60)
    
    email_produtivo = """
    Prezados,
    
    Gostaria de solicitar uma atualização urgente sobre o status da minha requisição #12345.
    O problema reportado na semana passada ainda não foi resolvido e está afetando minhas operações.
    
    Preciso de uma resposta o quanto antes.
    
    Atenciosamente,
    João Silva
    Cliente ID: 789456
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/classify",
            json={"text": email_produtivo},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Classificação realizada com sucesso!")
            print(f"\n📊 Resultados:")
            print(f"   Categoria: {data['category']}")
            print(f"   Confiança: {data['confidence']}%")
            print(f"\n💬 Resposta Gerada:")
            print("   " + "-" * 56)
            for line in data['response'].split('\n'):
                print(f"   {line}")
            print("   " + "-" * 56)
            
            # Verificar se a resposta parece ser da OpenAI (mais elaborada)
            if len(data['response']) > 200:
                print("\n✨ Resposta parece ser da OpenAI (mais elaborada)")
            else:
                print("\n📝 Resposta parece ser template padrão")
            
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_classify_improductive():
    """Testa classificação com email improdutivo"""
    print("\n" + "=" * 60)
    print("📧 TESTE 2: Email Improdutivo")
    print("=" * 60)
    
    email_improdutivo = """
    Olá equipe,
    
    Desejo um feliz natal e um próspero ano novo para toda a equipe!
    
    Agradeço pelo excelente atendimento durante todo o ano.
    
    Obrigado,
    Maria Santos
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/classify",
            json={"text": email_improdutivo},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Classificação realizada com sucesso!")
            print(f"\n📊 Resultados:")
            print(f"   Categoria: {data['category']}")
            print(f"   Confiança: {data['confidence']}%")
            print(f"\n💬 Resposta Gerada:")
            print("   " + "-" * 56)
            for line in data['response'].split('\n'):
                print(f"   {line}")
            print("   " + "-" * 56)
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_openai_key():
    """Verifica se a chave da OpenAI está configurada"""
    print("=" * 60)
    print("🔑 Verificando configuração da OpenAI")
    print("=" * 60)
    
    key = os.getenv('OPENAI_API_KEY')
    if key:
        # Mostrar apenas os primeiros e últimos caracteres
        masked_key = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
        print(f"✅ Chave OpenAI encontrada: {masked_key}")
        return True
    else:
        print("⚠️  Chave OpenAI não encontrada no arquivo .env")
        print("   A aplicação usará templates de resposta padrão")
        return False

def main():
    print("\n" + "=" * 60)
    print("🧪 TESTE DA INTEGRAÇÃO OPENAI")
    print("=" * 60)
    
    # Verificar chave
    has_key = check_openai_key()
    
    # Testar health
    print("\n")
    openai_configured = test_health()
    
    if has_key and not openai_configured:
        print("\n⚠️  AVISO: Chave encontrada no .env mas servidor não detectou.")
        print("   Reinicie o servidor para carregar a chave.")
    
    # Testar classificação
    if openai_configured or has_key:
        print("\n" + "=" * 60)
        print("🚀 Testando geração de respostas...")
        print("=" * 60)
        
        test1 = test_classify_with_openai()
        test2 = test_classify_improductive()
        
        print("\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES")
        print("=" * 60)
        print(f"Teste 1 (Produtivo): {'✅ PASSOU' if test1 else '❌ FALHOU'}")
        print(f"Teste 2 (Improdutivo): {'✅ PASSOU' if test2 else '❌ FALHOU'}")
        
        if openai_configured:
            print("\n✨ OpenAI está configurada e sendo usada!")
        else:
            print("\n📝 Usando templates padrão (OpenAI não configurada)")
    else:
        print("\n💡 Para usar OpenAI:")
        print("   1. Crie um arquivo .env na raiz do projeto")
        print("   2. Adicione: OPENAI_API_KEY=sua_chave_aqui")
        print("   3. Reinicie o servidor")

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("❌ Biblioteca 'requests' não encontrada.")
        print("   Instale com: pip install requests")
        exit(1)
    
    main()

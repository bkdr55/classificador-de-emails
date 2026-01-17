"""
Script de teste rápido para verificar se a API está funcionando
Execute: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check OK")
            print(f"   Status: {response.json()}")
            return True
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        print("   Certifique-se de que o servidor está rodando (python main.py)")
        return False

def test_classify_text():
    """Testa classificação com texto direto"""
    print("\n🔍 Testando classificação com texto...")
    
    # Email produtivo
    email_produtivo = """
    Prezados,
    
    Gostaria de solicitar uma atualização sobre o status da minha requisição #12345.
    Preciso saber quando será resolvido o problema reportado.
    
    Atenciosamente,
    João Silva
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/classify",
            json={"text": email_produtivo},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Classificação OK")
            print(f"   Categoria: {data['category']}")
            print(f"   Confiança: {data['confidence']}%")
            print(f"   Resposta: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Classificação falhou: {response.status_code}")
            print(f"   Erro: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_classify_file():
    """Testa classificação com arquivo"""
    print("\n🔍 Testando classificação com arquivo...")
    
    try:
        # Criar arquivo de teste temporário
        test_file_path = "test_email.txt"
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("Olá, desejo um feliz natal para toda a equipe!")
        
        with open(test_file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/api/classify", files=files)
        
        # Remover arquivo de teste
        import os
        os.remove(test_file_path)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Classificação de arquivo OK")
            print(f"   Categoria: {data['category']}")
            return True
        else:
            print(f"❌ Classificação de arquivo falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("=" * 50)
    print("🧪 TESTE DA API - Classificador de Emails")
    print("=" * 50)
    
    results = []
    
    # Teste 1: Health check
    results.append(("Health Check", test_health()))
    
    # Teste 2: Classificação com texto
    if results[0][1]:  # Só testa se health check passou
        results.append(("Classificação (Texto)", test_classify_text()))
        results.append(("Classificação (Arquivo)", test_classify_file()))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema funcionando perfeitamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("❌ Biblioteca 'requests' não encontrada.")
        print("   Instale com: pip install requests")
        exit(1)
    
    main()

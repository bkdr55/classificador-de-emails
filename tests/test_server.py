"""
Script para testar e iniciar o servidor com tratamento de erros
"""
import sys
import os
import traceback

print("=" * 60)
print("Iniciando servidor Flask...")
print("=" * 60)

try:
    # Importar o app
    print("\n[1/3] Importando aplicação...")
    from main import app
    print("✅ Aplicação importada com sucesso!")
    
    # Verificar se o app foi criado
    print("\n[2/3] Verificando configuração...")
    if app is None:
        raise Exception("App não foi criado corretamente")
    print("✅ App configurado!")
    
    # Iniciar servidor
    print("\n[3/3] Iniciando servidor...")
    print("=" * 60)
    print("🌐 Servidor rodando em: http://localhost:5000")
    print("⏹️  Pressione Ctrl+C para parar")
    print("=" * 60)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\n⏹️  Servidor interrompido pelo usuário")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ ERRO ao iniciar servidor:")
    print(f"   {str(e)}")
    print("\n📋 Detalhes do erro:")
    traceback.print_exc()
    sys.exit(1)

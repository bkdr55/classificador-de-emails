"""
Script simplificado para rodar a aplicação
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main import app
    print("=" * 50)
    print("🚀 Iniciando servidor Flask...")
    print("=" * 50)
    print("📡 Acesse: http://localhost:5000")
    print("⏹️  Pressione Ctrl+C para parar")
    print("=" * 50)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
except Exception as e:
    print(f"❌ Erro ao iniciar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

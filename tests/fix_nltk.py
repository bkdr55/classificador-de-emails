"""
Script para baixar todos os recursos necessários do NLTK
Execute: python fix_nltk.py
"""
import nltk

print("=" * 60)
print("Baixando recursos do NLTK...")
print("=" * 60)

resources = ['punkt', 'punkt_tab', 'stopwords', 'wordnet']

for resource in resources:
    try:
        print(f"\n📦 Baixando {resource}...")
        nltk.download(resource, quiet=False)
        print(f"✅ {resource} baixado com sucesso!")
    except Exception as e:
        print(f"⚠️  Erro ao baixar {resource}: {e}")

print("\n" + "=" * 60)
print("✅ Recursos do NLTK prontos!")
print("=" * 60)

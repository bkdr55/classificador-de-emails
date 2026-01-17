import os
import sys
import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    # O Heroku define a porta na variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Baixar recursos do NLTK
print("Baixando recursos do NLTK...")
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        pass

# Baixar punkt_tab (versão mais recente)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    try:
        nltk.download('punkt_tab', quiet=True)
    except Exception as e:
        print(f"Aviso: Não foi possível baixar punkt_tab: {e}")

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

print("Recursos do NLTK prontos!")

# Inicializar componentes de NLP
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('portuguese') + stopwords.words('english'))

# Inicializar modelos de IA
print("Carregando modelos de IA...")
try:
    # Modelo para classificação de sentimento/texto (adaptado para produtivo/improdutivo)
    classifier = pipeline(
        "text-classification",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=-1  # CPU
    )
    print("Modelo de classificação carregado!")
except Exception as e:
    print(f"Erro ao carregar modelo de classificação: {e}")
    classifier = None

# Configurar OpenAI (opcional, para respostas mais sofisticadas)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    openai.api_key = openai_api_key
    print("OpenAI configurado!")
else:
    print("OpenAI não configurado - usando modelo local")


def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """Extrai texto de um arquivo PDF"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        raise Exception(f"Erro ao ler PDF: {str(e)}")


def preprocess_text(text):
    """
    Pré-processa o texto usando técnicas de NLP:
    - Remove caracteres especiais
    - Remove stop words
    - Aplica lemmatização
    """
    # Converter para minúsculas
    text = text.lower()
    
    # Remover caracteres especiais, mantendo espaços e pontuação básica
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Tokenizar - tentar português, se falhar usar inglês
    try:
        tokens = nltk.word_tokenize(text, language='portuguese')
    except LookupError:
        # Se não tiver tokenizer português, usar inglês ou split simples
        try:
            tokens = nltk.word_tokenize(text)
        except:
            # Fallback: split simples por espaços
            tokens = text.split()
    
    # Remover stop words e aplicar lemmatização
    processed_tokens = [
        lemmatizer.lemmatize(token) 
        for token in tokens 
        if token not in stop_words and len(token) > 2
    ]
    
    return ' '.join(processed_tokens)


def classify_email(text):
    """
    Classifica o email como Produtivo ou Improdutivo usando IA
    """
    if not classifier:
        # Fallback: classificação baseada em palavras-chave
        return classify_with_keywords(text)
    
    try:
        # Usar o modelo de classificação
        result = classifier(text[:512])  # Limitar tamanho para o modelo
        
        # Adaptar resultado do modelo de sentimento para nossa classificação
        # Analisar palavras-chave para determinar se é produtivo
        productive_keywords = [
            'solicitação', 'requisição', 'suporte', 'problema', 'erro', 'ajuda',
            'atualização', 'status', 'caso', 'ticket', 'dúvida', 'questão',
            'arquivo', 'documento', 'urgente', 'importante', 'ação', 'resolver'
        ]
        
        unproductive_keywords = [
            'feliz natal', 'feliz ano novo', 'parabéns', 'agradecimento',
            'obrigado', 'obrigada', 'cumprimento', 'saudações', 'saudação'
        ]
        
        text_lower = text.lower()
        productive_score = sum(1 for keyword in productive_keywords if keyword in text_lower)
        unproductive_score = sum(1 for keyword in unproductive_keywords if keyword in text_lower)
        
        # Se há palavras-chave claras, usar elas
        if productive_score > unproductive_score and productive_score > 0:
            return "Produtivo", 0.85
        elif unproductive_score > productive_score and unproductive_score > 0:
            return "Improdutivo", 0.85
        
        # Caso contrário, usar o modelo de sentimento como base
        # Sentimentos negativos/neutros tendem a ser produtivos (requerem ação)
        # Sentimentos muito positivos podem ser improdutivos (cumprimentos)
        label = result[0]['label'] if isinstance(result, list) else result.get('label', '')
        score = result[0]['score'] if isinstance(result, list) else result.get('score', 0.5)
        
        # Lógica adaptada: se o texto é curto e muito positivo, provavelmente é improdutivo
        if len(text.split()) < 20 and 'POSITIVE' in str(label).upper():
            return "Improdutivo", min(score + 0.1, 0.95)
        else:
            return "Produtivo", min(score + 0.1, 0.95)
            
    except Exception as e:
        print(f"Erro na classificação com IA: {e}")
        return classify_with_keywords(text)


def classify_with_keywords(text):
    """Classificação baseada em palavras-chave (fallback)"""
    text_lower = text.lower()
    
    productive_keywords = [
        'solicitação', 'requisição', 'suporte', 'problema', 'erro', 'ajuda',
        'atualização', 'status', 'caso', 'ticket', 'dúvida', 'questão',
        'arquivo', 'documento', 'urgente', 'importante', 'ação', 'resolver',
        'preciso', 'necessito', 'gostaria', 'poderia', 'favor'
    ]
    
    unproductive_keywords = [
        'feliz natal', 'feliz ano novo', 'parabéns', 'agradecimento',
        'obrigado', 'obrigada', 'cumprimento', 'saudações', 'saudação',
        'bom dia', 'boa tarde', 'boa noite', 'feliz', 'aniversario'
    ]
    
    productive_count = sum(1 for keyword in productive_keywords if keyword in text_lower)
    unproductive_count = sum(1 for keyword in unproductive_keywords if keyword in text_lower)
    
    if productive_count > unproductive_count:
        confidence = min(0.7 + (productive_count * 0.05), 0.95)
        return "Produtivo", confidence
    elif unproductive_count > 0:
        confidence = min(0.7 + (unproductive_count * 0.05), 0.95)
        return "Improdutivo", confidence
    else:
        # Padrão: se não há palavras-chave claras, considerar produtivo (requer análise)
        return "Produtivo", 0.6


def generate_response(text, category):
    """
    Gera uma resposta automática baseada na categoria do email
    """
    if openai_api_key:
        try:
            return generate_response_openai(text, category)
        except Exception as e:
            print(f"Erro ao gerar resposta com OpenAI: {e}")
            return generate_response_template(category)
    else:
        return generate_response_template(category)


def generate_response_openai(text, category):
    """Gera resposta usando OpenAI GPT"""
    try:
        prompt = f"""Você é um assistente de atendimento de uma empresa financeira.
        
Email recebido:
{text[:500]}

Categoria: {category}

Gere uma resposta profissional e adequada em português brasileiro. 
Se for Produtivo, a resposta deve ser útil e direta ao ponto.
Se for Improdutivo, a resposta deve ser cordial e breve.

Resposta:"""

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente profissional de atendimento."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro na geração com OpenAI: {e}")
        return generate_response_template(category)


def generate_response_template(category):
    """Gera resposta usando templates (fallback)"""
    if category == "Produtivo":
        return """Prezado(a),

Agradecemos pelo contato. Recebemos sua solicitação e nossa equipe está analisando o caso.

Em breve entraremos em contato com mais informações ou atualizações sobre o status da sua requisição.

Caso tenha urgência, por favor, entre em contato através dos nossos canais prioritários.

Atenciosamente,
Equipe de Atendimento"""
    else:
        return """Prezado(a),

Agradecemos sua mensagem e os votos de felicidade.

É um prazer poder contar com você como nosso cliente.

Desejamos um excelente dia!

Atenciosamente,
Equipe de Atendimento"""


@app.route('/')
def index():
    """Rota principal - serve a interface web"""
    return render_template('index.html')


@app.route('/api/classify', methods=['POST'])
def classify():
    """Endpoint para classificar email e gerar resposta"""
    try:
        # Verificar se há arquivo ou texto direto
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extrair texto do arquivo
                if filename.endswith('.pdf'):
                    text = extract_text_from_pdf(filepath)
                else:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text = f.read()
                
                # Remover arquivo após processamento
                os.remove(filepath)
            else:
                return jsonify({'error': 'Formato de arquivo não permitido. Use .txt ou .pdf'}), 400
        
        elif 'text' in request.json:
            text = request.json['text']
        else:
            return jsonify({'error': 'Nenhum conteúdo fornecido'}), 400
        
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'Texto vazio'}), 400
        
        # Pré-processar texto
        processed_text = preprocess_text(text)
        
        # Classificar email
        category, confidence = classify_email(text)
        
        # Gerar resposta
        response = generate_response(text, category)
        
        return jsonify({
            'success': True,
            'category': category,
            'confidence': round(confidence * 100, 2),
            'response': response,
            'original_text': text[:200] + '...' if len(text) > 200 else text
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao processar: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'classifier_loaded': classifier is not None,
        'openai_configured': openai_api_key is not None
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Iniciando servidor Flask...")
    print("=" * 60)
    
    port = int(os.environ.get('PORT', 5000))
    
    print(f"📡 Servidor será iniciado em: http://localhost:{port}")
    print(f"📡 Também disponível em: http://127.0.0.1:{port}")
    print("⏹️  Pressione Ctrl+C para parar o servidor")
    print("=" * 60 + "\n")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=port, use_reloader=False)
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

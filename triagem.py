import os
import json
import openai

def processar_triagem_email(texto_email):
    """
    Função para triar e-mails usando IA (OpenAI).
    Classifica o e-mail em PRODUTIVO ou IMPRODUTIVO e sugere uma resposta automática.

    Args:
        texto_email (str): O conteúdo do e-mail a ser analisado.

    Returns:
        dict: Dicionário contendo 'categoria' e 'resposta_sugerida', ou erro em caso de falha.
    """
    # Obter chave da API do ambiente
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return {
            "erro": "Chave da API OpenAI não configurada. Defina OPENAI_API_KEY no ambiente."
        }

    # Configurar OpenAI
    openai.api_key = api_key

    # Mensagem do sistema para orientar a IA
    system_message = (
        "Você é um assistente de triagem financeira especializado em classificar e-mails de clientes. "
        "Seja criterioso: classifique como PRODUTIVO apenas e-mails que exigem ação concreta, como suporte, dúvidas operacionais, envio de documentos ou status de requisições. "
        "Não classifique pedidos legítimos de clientes como IMPRODUTIVO, mesmo que sejam educados. "
        "IMPRODUTIVO são apenas felicitações, agradecimentos irrelevantes ou mensagens não relacionadas ao negócio. "
        "Para cada e-mail, gere uma resposta curta, profissional e em português brasileiro. "
        "Retorne APENAS um objeto JSON válido com as chaves 'categoria' (PRODUTIVO ou IMPRODUTIVO) e 'resposta_sugerida' (string)."
    )

    # Prompt do usuário com o texto do e-mail
    user_message = f"Analise o seguinte e-mail e forneça a classificação e resposta sugerida:\n\n{texto_email}"

    try:
        # Chamada para a API OpenAI com formato JSON forçado
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Ou gpt-4 se disponível
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,  # Limite para resposta concisa
            temperature=0.3,  # Baixa variabilidade para consistência
            response_format={"type": "json_object"}  # Força saída JSON
        )

        # Extrair e parsear a resposta JSON
        resposta_json = response.choices[0].message.content.strip()
        resultado = json.loads(resposta_json)

        # Validar se as chaves esperadas estão presentes
        if "categoria" not in resultado or "resposta_sugerida" not in resultado:
            raise ValueError("Resposta da IA não contém as chaves obrigatórias.")

        return resultado

    except openai.APIError as e:
        return {
            "erro": f"Erro na API OpenAI: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "erro": f"Erro ao parsear resposta JSON: {str(e)}"
        }
    except Exception as e:
        return {
            "erro": f"Erro inesperado: {str(e)}"
        }

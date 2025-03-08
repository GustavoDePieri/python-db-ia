import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API da OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_embedding(text: str) -> list:
    """
    Gera um embedding para o texto usando o modelo de embeddings da OpenAI.
    
    Args:
        text: O texto para gerar o embedding
        
    Returns:
        Uma lista de floats representando o embedding do texto
    """
    try:
        # Utiliza o modelo text-embedding-ada-002 para criar embeddings
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        
        # Extrai o vetor de embedding da resposta
        embedding = response.data[0].embedding
        return embedding
    
    except Exception as e:
        print(f"Erro ao gerar embedding: {e}")
        # Retorna uma lista vazia em caso de erro
        return []

def generate_text(prompt: str, max_tokens: int = 500) -> str:
    """
    Gera texto usando o modelo GPT da OpenAI.
    
    Args:
        prompt: O texto de entrada para gerar a resposta
        max_tokens: Número máximo de tokens na resposta
        
    Returns:
        O texto gerado pelo modelo
    """
    try:
        # Usa o modelo gpt-3.5-turbo para gerar texto
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil especializado em ajudar com anotações e estudos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        # Extrai o texto gerado
        generated_text = response.choices[0].message.content
        return generated_text
    
    except Exception as e:
        print(f"Erro ao gerar texto: {e}")
        return f"Erro na geração de texto: {str(e)}"

def summarize_text(text: str, max_tokens: int = 200) -> str:
    """
    Gera um resumo do texto fornecido.
    
    Args:
        text: O texto para resumir
        max_tokens: Número máximo de tokens no resumo
        
    Returns:
        O resumo gerado
    """
    prompt = f"Por favor, resuma o seguinte texto de forma concisa e objetiva:\n\n{text}"
    return generate_text(prompt, max_tokens)

def expand_text(text: str, max_tokens: int = 500) -> str:
    """
    Expande o texto fornecido com mais detalhes e explicações.
    
    Args:
        text: O texto para expandir
        max_tokens: Número máximo de tokens na expansão
        
    Returns:
        O texto expandido
    """
    prompt = f"Por favor, expanda este texto com mais detalhes, exemplos e explicações:\n\n{text}"
    return generate_text(prompt, max_tokens) 
import os
from typing import Optional
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "notes_app")

# Cliente global do MongoDB
client: Optional[AsyncIOMotorClient] = None
db = None

async def connect_to_mongo():
    """Estabelece conexão com o MongoDB."""
    global client, db
    try:
        client = AsyncIOMotorClient(MONGODB_URI)
        # Verifica se a conexão está funcionando
        await client.admin.command('ping')
        print("Conexão com MongoDB estabelecida com sucesso!")
        
        # Configura o banco de dados
        db = client[DB_NAME]
        
        # Cria índice de texto para pesquisas
        await db.notes.create_index("title")
        await db.notes.create_index("content")
        
        # Cria índice vetorial para pesquisas semânticas
        # Nota: MongoDB 5.0+ com Atlas é necessário para índices vetoriais
        try:
            await db.command({
                "createIndexes": "notes",
                "indexes": [
                    {
                        "name": "vector_index",
                        "key": {"embedding": "vector"},
                        "vectorOptions": {"dimensions": 1536, "similarity": "cosine"}
                    }
                ]
            })
            print("Índice vetorial criado com sucesso!")
        except Exception as e:
            print(f"Aviso: Não foi possível criar índice vetorial: {e}")
            print("Isso pode acontecer se você não estiver usando MongoDB Atlas ou uma versão compatível.")
    
    except ConnectionFailure as e:
        print(f"Falha ao conectar com MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Fecha a conexão com o MongoDB."""
    global client
    if client:
        client.close()
        print("Conexão com MongoDB encerrada.")

# Funções para operações CRUD
async def insert_document(collection_name: str, document: dict):
    """Insere um documento em uma coleção."""
    result = await db[collection_name].insert_one(document)
    return result.inserted_id

async def find_document(collection_name: str, query: dict):
    """Busca um documento em uma coleção."""
    return await db[collection_name].find_one(query)

async def find_documents(collection_name: str, query: dict = None, limit: int = 100):
    """Busca múltiplos documentos em uma coleção."""
    if query is None:
        query = {}
    cursor = db[collection_name].find(query).limit(limit)
    return await cursor.to_list(length=limit)

async def update_document(collection_name: str, query: dict, update_data: dict):
    """Atualiza um documento em uma coleção."""
    result = await db[collection_name].update_one(query, {"$set": update_data})
    return result.modified_count

async def delete_document(collection_name: str, query: dict):
    """Remove um documento de uma coleção."""
    result = await db[collection_name].delete_one(query)
    return result.deleted_count

async def vector_search(collection_name: str, vector: list, limit: int = 5):
    """Realiza uma pesquisa vetorial."""
    try:
        # Consulta de similaridade vetorial
        pipeline = [
            {
                "$search": {
                    "index": "vector_index",
                    "knnBeta": {
                        "vector": vector,
                        "path": "embedding",
                        "k": limit
                    }
                }
            },
            {
                "$project": {
                    "title": 1,
                    "content": 1,
                    "score": {"$meta": "searchScore"}
                }
            }
        ]
        
        cursor = db[collection_name].aggregate(pipeline)
        return await cursor.to_list(length=limit)
    
    except Exception as e:
        print(f"Erro na pesquisa vetorial: {e}")
        # Fallback para pesquisa normal se a vetorial falhar
        return await find_documents(collection_name, limit=limit) 
from fastapi import APIRouter, HTTPException, Body, Query, Path
from fastapi.encoders import jsonable_encoder
from typing import List, Dict, Any
from bson import ObjectId
from datetime import datetime

from .models import NoteCreate, NoteUpdate, NoteOut, SearchQuery, AIRequest
from ..db.mongodb import (
    insert_document, 
    find_document, 
    find_documents, 
    update_document, 
    delete_document,
    vector_search
)
from ..ai.openai_service import get_embedding, summarize_text, expand_text

router = APIRouter()

# Definição da coleção
COLLECTION_NAME = "notes"

# Rotas para gerenciamento de notas

@router.post("/notes/", response_model=Dict[str, str])
async def create_note(note: NoteCreate = Body(...)):
    """
    Cria uma nova nota com título, conteúdo e tags.
    
    Também gera um embedding para o conteúdo da nota usando a API da OpenAI.
    """
    note_dict = note.dict()
    
    # Adiciona timestamps
    now = datetime.now()
    note_dict["created_at"] = now
    note_dict["updated_at"] = now
    
    # Gera embedding para busca semântica
    text_for_embedding = f"{note.title} {note.content}"
    embedding = get_embedding(text_for_embedding)
    note_dict["embedding"] = embedding
    
    # Insere no banco de dados
    note_id = await insert_document(COLLECTION_NAME, note_dict)
    
    return {"id": str(note_id), "message": "Nota criada com sucesso"}


@router.get("/notes/", response_model=List[NoteOut])
async def read_notes(skip: int = Query(0), limit: int = Query(100)):
    """
    Recupera uma lista de notas.
    """
    notes = await find_documents(COLLECTION_NAME, {}, limit=limit)
    
    # Converte ObjectId para string para serialização
    for note in notes:
        note["id"] = str(note.pop("_id"))
    
    return notes


@router.get("/notes/{note_id}", response_model=NoteOut)
async def read_note(note_id: str = Path(...)):
    """
    Recupera uma nota específica pelo ID.
    """
    try:
        # Verifica se o ID é válido
        object_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    # Busca a nota no banco de dados
    note = await find_document(COLLECTION_NAME, {"_id": object_id})
    
    if note is None:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    
    # Converte ObjectId para string para serialização
    note["id"] = str(note.pop("_id"))
    
    return note


@router.put("/notes/{note_id}", response_model=Dict[str, str])
async def update_note(note_id: str = Path(...), note_update: NoteUpdate = Body(...)):
    """
    Atualiza uma nota existente pelo ID.
    
    Atualiza também o embedding se o título ou conteúdo for modificado.
    """
    try:
        # Verifica se o ID é válido
        object_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    # Busca a nota no banco de dados
    existing_note = await find_document(COLLECTION_NAME, {"_id": object_id})
    
    if existing_note is None:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    
    # Prepara os dados para atualização
    update_data = {k: v for k, v in note_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.now()
    
    # Atualiza embedding se o título ou conteúdo foi alterado
    if "title" in update_data or "content" in update_data:
        title = update_data.get("title", existing_note["title"])
        content = update_data.get("content", existing_note["content"])
        text_for_embedding = f"{title} {content}"
        embedding = get_embedding(text_for_embedding)
        update_data["embedding"] = embedding
    
    # Atualiza no banco de dados
    modified_count = await update_document(COLLECTION_NAME, {"_id": object_id}, update_data)
    
    if modified_count == 0:
        raise HTTPException(status_code=400, detail="Falha ao atualizar nota")
    
    return {"message": "Nota atualizada com sucesso"}


@router.delete("/notes/{note_id}", response_model=Dict[str, str])
async def delete_note(note_id: str = Path(...)):
    """
    Remove uma nota pelo ID.
    """
    try:
        # Verifica se o ID é válido
        object_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    # Remove do banco de dados
    deleted_count = await delete_document(COLLECTION_NAME, {"_id": object_id})
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    
    return {"message": "Nota removida com sucesso"}


# Rotas para pesquisa e processamento de IA

@router.post("/search/", response_model=List[Dict[str, Any]])
async def search_notes(search_query: SearchQuery = Body(...)):
    """
    Realiza uma pesquisa semântica nas notas.
    
    Usa embedding para encontrar notas semanticamente similares à consulta.
    """
    # Gera embedding para a consulta
    embedding = get_embedding(search_query.query)
    
    # Realiza busca vetorial
    results = await vector_search(COLLECTION_NAME, embedding, limit=search_query.limit)
    
    # Processa resultados para retorno
    formatted_results = []
    for note in results:
        if "_id" in note:
            note["id"] = str(note.pop("_id"))
        formatted_results.append(note)
    
    return formatted_results


@router.post("/ai/summarize/", response_model=Dict[str, str])
async def ai_summarize(request: AIRequest = Body(...)):
    """
    Gera um resumo do texto fornecido usando IA.
    """
    summary = summarize_text(request.text, request.max_tokens)
    return {"result": summary}


@router.post("/ai/expand/", response_model=Dict[str, str])
async def ai_expand(request: AIRequest = Body(...)):
    """
    Expande o texto fornecido com mais detalhes usando IA.
    """
    expanded = expand_text(request.text, request.max_tokens)
    return {"result": expanded} 
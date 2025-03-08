from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import os
from dotenv import load_dotenv

# Importações dos módulos da aplicação
from .db.mongodb import connect_to_mongo, close_mongo_connection
from .api.routes import router as api_router

# Carrega variáveis de ambiente
load_dotenv()

# Configura a aplicação FastAPI
app = FastAPI(title="Aplicação de Notas com IA")

# Configura arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Registra os eventos de inicialização e encerramento
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Inclui as rotas da API
app.include_router(api_router, prefix="/api")

# Rota principal
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para pesquisa semântica
@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

# Rota para criação de notas
@app.get("/create", response_class=HTMLResponse)
async def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

# Executa o servidor se o arquivo for executado diretamente
if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run("app.main:app", host=host, port=port, reload=True) 
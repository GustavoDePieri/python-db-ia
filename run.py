"""
Script para iniciar o servidor da aplicação de Notas com IA
"""
import uvicorn

if __name__ == "__main__":
    # Executa a aplicação com auto-recarregamento ativado
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True) 
# Aplicação de Notas com IA e MongoDB Vector Search

Este projeto é uma aplicação didática que demonstra:
- Integração com banco de dados MongoDB (incluindo busca vetorial)
- Integração com APIs de IA (OpenAI)
- Roteamento de páginas com FastAPI
- Implantação na Vercel

## Estrutura do Projeto

```
.
├── app/                    # Diretório principal da aplicação
│   ├── api/                # Endpoints da API
│   ├── db/                 # Conexão e operações com MongoDB
│   ├── ai/                 # Integração com serviços de IA
│   ├── templates/          # Templates HTML para renderização
│   ├── static/             # Arquivos estáticos (CSS, JS)
│   └── main.py             # Ponto de entrada da aplicação
├── .env                    # Variáveis de ambiente (não incluir no git)
├── .env.example            # Exemplo de variáveis de ambiente
├── requirements.txt        # Dependências do projeto
└── vercel.json             # Configuração para deploy na Vercel
```

## Como executar localmente

1. Clone este repositório
   ```
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado)
   ```
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` baseado no `.env.example` e adicione suas credenciais
   ```
   cp .env.example .env
   # Edite o arquivo .env com suas credenciais
   ```

5. Execute o servidor local:
   ```
   python run.py
   ```
   ou
   ```
   uvicorn app.main:app --reload
   ```

6. Acesse http://localhost:8000 no navegador

## Configuração do MongoDB Atlas para Busca Vetorial

Para que a funcionalidade de busca semântica funcione corretamente, é necessário:

1. Criar uma conta no [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Configurar um cluster (o plano gratuito M0 é suficiente para testes)
3. Adicionar um usuário e definir as regras de acesso à rede
4. Obter a string de conexão e configurar no arquivo `.env`
5. O índice vetorial será criado automaticamente pela aplicação

## Funcionalidades

- Criação, edição e exclusão de notas
- Armazenamento de dados no MongoDB
- Pesquisa semântica usando embeddings e busca vetorial
- Geração de resumos e expansão de conteúdo com IA
- Interface web simples para interação

## Implantação na Vercel

Para implantar na Vercel:
1. Crie uma conta na Vercel
2. Conecte seu repositório GitHub
3. Configure as variáveis de ambiente na plataforma
4. Implante o aplicativo

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes. 
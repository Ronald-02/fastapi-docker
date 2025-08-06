  ### API de Gestão de Atletas

Este projeto é uma API REST desenvolvida com FastAPI e PostgreSQL, utilizando Docker e SQLAlchemy assíncrono. O objetivo é gerenciar atletas, centros de treinamento e categorias com funcionalidades completas de CRUD e relacionamento entre tabelas via UUID.

Principais funcionalidades:
	•	Cadastro de atletas (individual ou múltiplos)
	•	Listagem com paginação e filtros por nome, CPF, centro de treinamento e categoria
	•	Atualização e remoção de atletas por ID
	•	Relacionamentos entre as tabelas utilizando UUIDs
	•	Mensagens de erro personalizadas com tratamento de exceções
	•	Documentação automática via Swagger (http://localhost:8000/docs)

Tecnologias utilizadas:
	•	FastAPI
	•	PostgreSQL
	•	Docker e Docker Compose
	•	SQLAlchemy (modo assíncrono)
	•	Alembic
	•	FastAPI Pagination

Execução do projeto:
	1.	Clone o repositório
	2.	Crie um arquivo .env com:
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres
	3.	Execute o comando:
docker-compose up –build
	4.	Acesse o Swagger para testar os endpoints:
http://localhost:8000/docs

Status:
	•	Projeto rodando localmente com sucesso via Docker
	•	Endpoints GET, POST, PUT e DELETE funcionando
	•	Testado via Swagger e Postman

   Endpoints
	•	GET /atletas: Lista todos os atletas com filtros e paginação
	•	POST /atletas: Cria um ou mais atletas
	•	PUT /atletas/{id}: Atualiza um atleta existente
	•	DELETE /atletas/{id}: Remove um atleta

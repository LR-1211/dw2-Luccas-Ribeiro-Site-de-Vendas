# Backend README.md

# Loja Escolar - Backend

Este documento fornece informações sobre a configuração e uso do backend do sistema de vendas "Loja Escolar".

## Tecnologias Utilizadas

- Python
- FastAPI ou Flask
- SQLite
- SQLAlchemy

## Estrutura do Projeto

```
/backend
  ├── app.py          # Ponto de entrada da aplicação
  ├── models.py       # Definições dos modelos de dados
  ├── database.py     # Configuração do banco de dados
  ├── seed.py         # Script para popular o banco de dados
  ├── requirements.txt # Dependências do projeto
  ├── README.md       # Documentação do backend
  └── REPORT.md       # Relatório técnico
```

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd loja-escolar/backend
   ```

2. Crie um ambiente virtual e ative-o:
   ```
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate     # Para Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Execução

Para iniciar o servidor, execute o seguinte comando:

```
python app.py
```

O servidor estará disponível em `http://localhost:8000`.

## Endpoints da API

- `GET /health` - Verifica se o servidor está funcionando.
- `GET /produtos` - Lista todos os produtos com opções de busca e ordenação.
- `GET /produtos/{id}` - Obtém detalhes de um produto específico.
- `POST /produtos` - Cria um novo produto.
- `PUT /produtos/{id}` - Atualiza um produto existente.
- `DELETE /produtos/{id}` - Remove um produto.
- `POST /cupom/validar` - Valida um cupom de desconto.
- `POST /carrinho/confirmar` - Confirma um pedido e atualiza o estoque.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.
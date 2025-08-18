# Loja Escolar

Este projeto é um mini-sistema de vendas para uma loja escolar, permitindo a visualização e compra de produtos escolares. O sistema é dividido em duas partes principais: o front-end, que é responsável pela interface do usuário, e o back-end, que gerencia a lógica de negócios e a persistência de dados.

## Estrutura do Projeto

```
loja-escolar
├── frontend
│   ├── index.html       # Estrutura HTML principal do site
│   ├── styles.css       # Estilos CSS para o site
│   └── scripts.js       # Código JavaScript para operações CRUD e funcionalidades do carrinho
├── backend
│   ├── app.py           # Ponto de entrada da aplicação FastAPI/Flask
│   ├── models.py        # Modelos SQLAlchemy para o banco de dados
│   ├── database.py      # Conexão e configuração do banco de dados
│   ├── seed.py          # Script para popular o banco de dados com produtos
│   ├── requirements.txt  # Pacotes Python necessários para o backend
│   ├── README.md        # Documentação específica do backend
│   └── REPORT.md        # Relatório técnico do projeto
├── .gitignore           # Arquivos e diretórios a serem ignorados pelo Git
└── tests.http           # Coleção de requisições HTTP para testar os endpoints da API
```

## Tecnologias Utilizadas

- **Front-end:** HTML5, CSS3, JavaScript (ES6+)
- **Back-end:** Python (FastAPI ou Flask)
- **Banco de Dados:** SQLite (via SQLAlchemy)
- **Ferramentas:** VS Code, Git/GitHub, Thunder Client/Insomnia

## Como Executar o Projeto

1. Clone o repositório:
   ```
   git clone <URL do repositório>
   cd loja-escolar
   ```

2. Instale as dependências do backend:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Execute o script de seed para popular o banco de dados:
   ```
   python seed.py
   ```

4. Inicie o servidor:
   ```
   python app.py
   ```

5. Abra o arquivo `index.html` no seu navegador para acessar a interface do usuário.

## Funcionalidades

- Visualização de produtos em um catálogo responsivo.
- Adição de produtos ao carrinho de compras.
- Validação de cupons de desconto.
- Formulário de administração para gerenciamento de produtos.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
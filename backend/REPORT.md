# Arquitetura do Sistema de Vendas Web

Este relatório técnico descreve a arquitetura e os detalhes do sistema de vendas web "Loja Escolar", incluindo as tecnologias utilizadas, peculiaridades implementadas e exemplos de validações.

## Arquitetura

O sistema é composto por um front-end e um back-end que se comunicam através de uma API REST. A arquitetura é organizada da seguinte forma:

- **Front-end**: Implementado em HTML, CSS e JavaScript, responsável pela interface do usuário e interações.
- **Back-end**: Desenvolvido em Python utilizando FastAPI ou Flask, gerenciando a lógica de negócios e a comunicação com o banco de dados.
- **Banco de Dados**: Utiliza SQLite como sistema de gerenciamento de banco de dados, com SQLAlchemy para a manipulação de dados.

### Fluxo de Dados

1. O usuário interage com a interface do front-end.
2. O front-end faz requisições à API do back-end.
3. O back-end processa as requisições, interage com o banco de dados e retorna as respostas ao front-end.
4. O front-end atualiza a interface com os dados recebidos.

## Tecnologias e Versões Usadas

- **Front-end**:
  - HTML5
  - CSS3 (Flex/Grid)
  - JavaScript (ES6+)

- **Back-end**:
  - Python
  - FastAPI ou Flask
  - SQLAlchemy

- **Banco de Dados**:
  - SQLite

## Prompts Utilizados

- O prompt foi utilizado para gerar a estrutura do projeto, incluindo a definição de arquivos e suas respectivas funções.

## Peculiaridades Implementadas

1. **Acessibilidade**: Implementação de atributos ARIA e navegação por teclado para garantir que o sistema seja utilizável por todos.
2. **Validações Customizadas**: Validações de entrada no front-end e no back-end para garantir a integridade dos dados.
3. **Ordenação Persistida**: A ordenação dos produtos é mantida no localStorage para melhorar a experiência do usuário.

## Exemplos de Validações

- **Front-end**: Validação do formulário de produto para garantir que os campos obrigatórios sejam preenchidos corretamente.
- **Back-end**: Validação de cupom para garantir que o desconto só seja aplicado quando o subtotal for maior ou igual a R$ 50,00.

## Como Rodar

1. Clone o repositório.
2. Instale as dependências do back-end com `pip install -r requirements.txt`.
3. Execute o servidor back-end com `python app.py`.
4. Abra o arquivo `index.html` no navegador para acessar o front-end.

## Limitações e Melhorias Futuras

- Implementar autenticação para a seção de administração.
- Adicionar testes automatizados para garantir a qualidade do código.
- Melhorar a responsividade do front-end para dispositivos móveis.
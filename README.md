# BeMaker - Back-End API

Este repositório contém a API de Back-End do projeto **BeMaker**, desenvolvida durante o estágio curricular orientado pela **Unijuí (Universidade Regional do Noroeste do Estado do Rio Grande do Sul)**. 

O sistema foi projetado sob o paradigma de **Arquitetura Serverless Orientada a Eventos**, garantindo alta escalabilidade, isolamento de recursos e baixo custo operacional. Toda a construção da API seguiu práticas rigorosas de qualidade de código e testes automatizados.

---

## Tecnologias e Ferramentas

O ecossistema do Back-End foi construído utilizando as seguintes tecnologias:

* **Linguagem Principal:** Python
* **Ambiente e Dependências:** Pipenv (Ambiente virtual e gerenciamento estrito de pacotes)
* **Framework de Testes:** Pytest (Abordagem de Desenvolvimento Orientado a Testes - TDD)
* **Banco de Dados:** MongoDB (Modelagem NoSQL flexível e orientada a documentos)
* **Arquitetura:** Serverless
* **Integração Front-End:** Projetada para comunicação assíncrona com aplicação Angular

---

## Diferenciais Técnicos e Arquitetura

### ☁️ Arquitetura Serverless & Orientada a Eventos
A aplicação foi estruturada para rodar de forma distribuída (utilizando funções como microsserviços), eliminando a necessidade de gerenciamento e provisionamento manual de servidores (Serverless). As funções respondem diretamente a gatilhos e eventos HTTP de forma sob demanda.

### Desenvolvimento Orientado a Testes (TDD)
A integridade das regras de negócio, contratos de dados e fluxos de persistência no MongoDB foram assegurados pela escrita prévia de testes automatizados com o **Pytest**. O ecossistema de testes garante regressão zero e valida cenários de erro e sucesso da aplicação.

### Isolamento de Ambiente com Pipenv
A consistência entre os ambientes de desenvolvimento e produção foi blindada através do uso do **Pipenv**, gerando arquivos deterministicos `Pipfile.lock` que evitam conflitos de dependências.

<div align="center">

# ✂️ BarberFlow

### Gestão inteligente para barbearias

Plataforma em desenvolvimento para centralizar agendamentos, clientes, serviços, barbeiros, pagamentos e informações gerenciais de uma barbearia.

![Python](https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API_REST-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Banco_de_Dados-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge\&logo=react\&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178C6?style=for-the-badge\&logo=typescript\&logoColor=white)
![Status](https://img.shields.io/badge/Status-Release_0.1_em_desenvolvimento-yellow?style=for-the-badge)

</div>

---

## 📌 Sobre o projeto

O **BarberFlow** é uma plataforma de gestão desenvolvida para organizar a operação diária de barbearias.

O projeto nasceu da necessidade de substituir controles espalhados entre:

* WhatsApp;
* agendas de papel;
* cadernos;
* planilhas;
* anotações financeiras;
* controles informais de estoque.

A proposta não é criar apenas um agendador, mas uma base de gestão capaz de apoiar decisões sobre clientes, atendimentos, faturamento e desempenho da operação.

---

## 🎯 Problemas que o sistema busca resolver

Barbearias que trabalham sem uma plataforma centralizada podem enfrentar:

* horários duplicados;
* esquecimentos e faltas;
* dificuldade para remarcar atendimentos;
* ausência de histórico dos clientes;
* falta de visão sobre faturamento;
* controle precário de pagamentos;
* dificuldade para analisar o desempenho dos barbeiros;
* falta de controle sobre produtos e estoque;
* dependência excessiva de conversas no WhatsApp.

O BarberFlow busca reunir essas informações em um único ambiente.

---

## 👥 Perfis de usuário

### Administrador

Responsável pela gestão da barbearia.

Poderá:

* cadastrar funcionários;
* cadastrar serviços;
* visualizar relatórios;
* acompanhar o caixa;
* gerenciar estoque;
* configurar horários;
* consultar indicadores.

### Barbeiro

Responsável pelos atendimentos.

Poderá:

* visualizar sua agenda;
* confirmar atendimentos;
* cadastrar clientes;
* remarcar horários;
* registrar pagamentos;
* consultar seu histórico.

### Cliente

Poderá:

* criar uma conta;
* consultar serviços;
* agendar horários;
* cancelar agendamentos;
* visualizar o histórico;
* atualizar seus dados.

---

## 🚀 Escopo do MVP

A primeira versão do BarberFlow está planejada para incluir:

* autenticação;
* cadastro de clientes;
* cadastro de barbeiros;
* cadastro de serviços;
* agenda;
* criação de agendamentos;
* cancelamento e remarcação;
* registro de pagamentos;
* dashboard básico;
* controle financeiro simplificado.

Funcionalidades como integração com WhatsApp, aplicativo mobile, inteligência artificial, emissão de notas fiscais e programa de fidelidade não fazem parte do escopo inicial.

---

## 🏗️ Arquitetura

O projeto adota a estratégia de **monólito modular**.

Isso significa que existe uma única aplicação backend, mas organizada em módulos independentes.

```text
BarberFlow API
├── auth
├── users
├── customers
├── barbers
├── services
├── appointments
├── payments
├── finance
└── dashboard
```

Essa abordagem busca equilibrar:

* simplicidade de desenvolvimento;
* separação de responsabilidades;
* facilidade de manutenção;
* possibilidade de evolução futura;
* menor complexidade operacional.

---

## 🔄 Fluxo da aplicação

```text
Frontend React
      ↓
API REST FastAPI
      ↓
Services
      ↓
Repositories
      ↓
PostgreSQL
```

Exemplo de criação de agendamento:

```text
POST /appointments
        ↓
Route
        ↓
AppointmentService
        ↓
AppointmentRepository
        ↓
PostgreSQL
```

---

## 🧱 Organização do backend

Cada módulo deverá seguir uma estrutura semelhante:

```text
customers/
├── models.py
├── schemas.py
├── repository.py
├── service.py
├── routes.py
└── tests/
```

### Responsabilidades

| Camada          | Responsabilidade             |
| --------------- | ---------------------------- |
| `models.py`     | Modelos e tabelas do banco   |
| `schemas.py`    | Validação de entrada e saída |
| `repository.py` | Acesso ao banco de dados     |
| `service.py`    | Regras de negócio            |
| `routes.py`     | Endpoints HTTP               |
| `tests/`        | Testes do módulo             |

A regra principal da arquitetura é:

```text
Rotas não contêm regras de negócio.
```

As rotas recebem a requisição, validam os dados, chamam o serviço e retornam a resposta.

---

## 🛠️ Tecnologias

### Backend

* Python;
* FastAPI;
* SQLAlchemy;
* Pydantic;
* Alembic;
* Uvicorn;
* JWT;
* Passlib;
* Pytest.

### Frontend planejado

* React;
* TypeScript;
* Vite;
* Axios.

### Infraestrutura

* PostgreSQL;
* Docker;
* Docker Compose;
* GitHub.

---

## 📁 Estrutura atual

```text
BarberFlow/
├── backend/
│   ├── alembic/
│   ├── src/
│   │   ├── modules/
│   │   ├── shared/
│   │   └── main.py
│   ├── tests/
│   ├── alembic.ini
│   └── requirements.txt
├── docs/
├── .env.example
└── README.md
```

> A estrutura continuará evoluindo conforme os módulos da Release 0.1 forem implementados.

---

## ✅ Estado atual da implementação

Já existem elementos iniciais como:

* aplicação FastAPI;
* endpoint de verificação de saúde;
* configurações por variáveis de ambiente;
* conexão com PostgreSQL;
* configuração do SQLAlchemy;
* configuração inicial do Alembic;
* modelo de usuário;
* perfis de acesso;
* enums de agendamento e pagamento;
* mixins de auditoria;
* soft delete;
* teste automatizado do endpoint de saúde.

Endpoint disponível:

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok",
  "app": "BarberFlow",
  "environment": "development"
}
```

Autenticação em desenvolvimento:

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@example.com&password=sua_senha
```

Rotas de usuários:

```http
GET  /api/v1/users/me
GET  /api/v1/users       # somente ADMIN
POST /api/v1/users       # somente ADMIN
```

Rotas de clientes, disponíveis para `ADMIN` e `BARBER`:

```http
GET    /api/v1/customers
POST   /api/v1/customers
GET    /api/v1/customers/{id}
PATCH  /api/v1/customers/{id}
DELETE /api/v1/customers/{id}
```

A listagem aceita pesquisa e paginação com `q`, `offset` e `limit`.

Rotas de barbeiros:

```http
GET   /api/v1/barbers
POST  /api/v1/barbers                         # somente ADMIN
GET   /api/v1/barbers/{id}
PATCH /api/v1/barbers/{id}                    # somente ADMIN
GET   /api/v1/barbers/{id}/unavailabilities
POST  /api/v1/barbers/{id}/unavailabilities  # somente ADMIN
```

As jornadas usam dias da semana de `0` (segunda-feira) a `6` (domingo).

Rotas do catálogo de serviços:

```http
GET  /api/v1/service-categories
POST /api/v1/service-categories       # somente ADMIN
GET    /api/v1/services
POST   /api/v1/services               # somente ADMIN
GET    /api/v1/services/{id}
PATCH  /api/v1/services/{id}          # somente ADMIN
DELETE /api/v1/services/{id}          # somente ADMIN
```

Preços são armazenados como valores decimais e a duração é informada em minutos.

Rotas de agendamentos da Sprint 2:

```http
GET   /api/v1/appointments?starts_at=...&ends_at=...
GET   /api/v1/appointments/availability?barber_id=...&date=...&service_ids=...
POST  /api/v1/appointments
GET   /api/v1/appointments/{id}
PATCH /api/v1/appointments/{id}/reschedule
PATCH /api/v1/appointments/{id}/cancel
PATCH /api/v1/appointments/{id}/status
```

Os horários recebidos devem conter fuso horário. Internamente, todas as datas são
armazenadas em UTC e validadas contra `APP_TIMEZONE`.

Rotas de pagamentos da Sprint 3:

```http
POST /api/v1/appointments/{id}/payment
GET  /api/v1/appointments/{id}/payment
```

Cada atendimento aceita um único pagamento integral. O desconto é registrado
separadamente e o pagamento cria uma entrada financeira na mesma transação.

Rotas financeiras, disponíveis somente para `ADMIN`:

```http
POST /api/v1/finance/transactions
GET  /api/v1/finance/transactions?starts_at=...&ends_at=...
GET  /api/v1/finance/summary?starts_at=...&ends_at=...
POST /api/v1/finance/transactions/{id}/corrections
```

Movimentações financeiras são imutáveis. Erros são corrigidos por um
contralançamento vinculado ao registro original.

Dashboard administrativo:

```http
GET /api/v1/dashboard/summary?starts_at=...&ends_at=...
```

O resumo apresenta faturamento recebido, atendimentos concluídos, novos clientes,
serviços mais vendidos e o barbeiro com maior faturamento no período.

---

## 🚀 Como executar o backend

### Pré-requisitos

* Python 3.11 ou superior;
* PostgreSQL;
* Git.

### Clone o repositório

```bash
git clone https://github.com/ONestoDev/BarberFlow.git
```

### Acesse o projeto

```bash
cd BarberFlow
```

### Crie o ambiente virtual

Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Instale as dependências

```bash
pip install -r backend/requirements.txt
```

### Configure as variáveis de ambiente

Crie o arquivo `.env` usando o modelo `.env.example`.

```env
APP_NAME=BarberFlow
APP_ENV=development
APP_TIMEZONE=America/Sao_Paulo
APPOINTMENT_SLOT_INTERVAL_MINUTES=15

DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/barberflow

JWT_SECRET=substitua_por_uma_chave_segura
JWT_ALGORITHM=HS256
JWT_EXPIRES_IN_MINUTES=60
```

### Prepare o banco e crie o administrador inicial

Com o PostgreSQL em execução:

```powershell
cd backend
..\.venv\Scripts\alembic.exe upgrade head
..\.venv\Scripts\python.exe -m src.scripts.create_admin --name "Administrador" --email admin@example.com
```

A senha será solicitada de forma interativa e não ficará registrada no histórico do terminal.

### Execute a API

```powershell
uvicorn src.main:app --reload
```

A documentação automática ficará disponível em:

```text
http://localhost:8000/docs
```

---

## 🧪 Testes

Execute a partir da raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Com relatório de cobertura:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=src
```

---

## 🗃️ Banco de dados

A arquitetura prevê entidades como:

* usuários;
* clientes;
* barbeiros;
* categorias de serviço;
* serviços;
* agendamentos;
* serviços do agendamento;
* pagamentos;
* transações financeiras;
* configurações;
* registros de auditoria.

As migrações serão gerenciadas com Alembic.

Exemplo:

```bash
alembic upgrade head
```

---

## 🔐 Segurança

A aplicação está planejada para usar:

* autenticação JWT;
* controle de acesso baseado em perfil;
* hash de senhas;
* rotas protegidas;
* soft delete;
* registro de auditoria.

Perfis previstos:

```text
ADMIN
BARBER
CUSTOMER
```

---

## 🗺️ Roadmap

### Situação das sprints

- **Sprint 0:** descoberta, requisitos e arquitetura — concluída.
- **Sprint 1:** autenticação, usuários, clientes, barbeiros e serviços — concluída.
- **Sprint 2:** agenda e ciclo do atendimento — concluída.
- **Sprint 3:** pagamentos e financeiro — concluída.
- **Sprint 4:** dashboard e indicadores — concluída.
- **Sprint 5:** frontend administrativo — próxima, pausada antes do início.

### Release 0.1

* [x] visão do produto;
* [x] definição do MVP;
* [x] requisitos;
* [x] regras de negócio;
* [x] arquitetura inicial;
* [x] base do backend;
* [x] conexão com banco;
* [x] endpoint de saúde;
* [x] autenticação;
* [x] usuários;
* [x] clientes;
* [x] barbeiros;
* [x] serviços;
* [x] agendamentos;
* [x] pagamentos;
* [x] financeiro;
* [x] dashboard;
* [ ] frontend inicial;
* [ ] Docker Compose;
* [ ] testes de integração.

### Evoluções futuras

* controle de estoque;
* notificações;
* programa de fidelidade;
* integração com WhatsApp;
* aplicativo mobile;
* multiempresa;
* relatórios avançados;
* integrações financeiras.

---

## 📚 Documentação

A pasta `docs` contém decisões e materiais de planejamento, incluindo:

* visão do produto;
* problema de negócio;
* requisitos;
* regras de negócio;
* definição do MVP;
* arquitetura;
* módulos;
* riscos;
* roadmap;
* decisões técnicas.

---

## ⚠️ Status do projeto

O BarberFlow está em desenvolvimento.

A arquitetura e o escopo estão documentados, mas vários módulos ainda não foram implementados.

Portanto, o projeto ainda não deve ser considerado uma solução pronta para uso comercial ou produção.

---

## 👨‍💻 Autor

Desenvolvido por **Ernesto — ONestoDev**.

[![GitHub](https://img.shields.io/badge/GitHub-ONestoDev-181717?style=for-the-badge\&logo=github)](https://github.com/ONestoDev)

---

## 📄 Licença

Defina uma licença e adicione o arquivo `LICENSE` antes da distribuição pública do projeto.

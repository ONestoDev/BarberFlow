# Arquitetura Inicial

> **"Arquitetura não é escolher tecnologia. Arquitetura é organizar decisões para reduzir riscos."**
>

Essa frase será nossa base.

Não vamos escolher ferramentas porque estão na moda.

Vamos escolher o que resolve o problema da V1 com qualidade e simplicidade.

---

# 1. Tipo de Arquitetura

Adotaremos um:

# Monólito Modular

Isso significa que teremos uma única aplicação backend, mas organizada em módulos bem separados.

```
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

## Por que não microsserviços agora?

Porque para a V1 seria excesso de complexidade.

Microsserviços exigem:

- comunicação entre serviços;
- autenticação distribuída;
- observabilidade mais complexa;
- deploys independentes;
- mensageria;
- tolerância a falhas;
- gestão de infraestrutura mais avançada.

Para um MVP, isso atrapalharia mais do que ajudaria.

## Por que não um projeto totalmente simples?

Porque também não queremos um código bagunçado.

O monólito modular nos dá equilíbrio:

```
Simples para desenvolver

↓

Organizado para manter

↓

Possível de evoluir
```

# Arquitetura Geral

```
Usuário
   ↓
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

Fluxo completo:

```
Tela de Agendamento

↓

POST /appointments

↓

AppointmentController

↓

AppointmentService

↓

AppointmentRepository

↓

PostgreSQL
```

---

# 4. Camadas do Backend

Usaremos uma Clean Architecture simplificada.

```
backend/

└── src/

    ├── modules/
    │   ├── auth/
    │   ├── users/
    │   ├── customers/
    │   ├── barbers/
    │   ├── services/
    │   ├── appointments/
    │   ├── payments/
    │   ├── finance/
    │   └── dashboard/
    │
    ├── shared/
    │   ├── database/
    │   ├── security/
    │   ├── exceptions/
    │   ├── config/
    │   └── utils/
    │
    └── main.py
```

---

# 5. Estrutura de cada módulo

Cada módulo seguirá o mesmo padrão.

Exemplo: `customers`

```
customers/

├── models.py
├── schemas.py
├── repository.py
├── service.py
├── routes.py
└── tests/
```

## Responsabilidade de cada arquivo

### `models.py`

Representa as tabelas do banco.

---

### `schemas.py`

Define entrada e saída da API.

Exemplo:

```
CustomerCreate
CustomerResponse
CustomerUpdate
```

---

### `repository.py`

Acessa o banco.

Exemplo:

```
buscar_por_id
listar
salvar
atualizar
```

---

### `service.py`

Contém regras de negócio.

Exemplo:

```
não permitir cliente sem nome
não permitir agendamento em horário ocupado
```

---

### `routes.py`

Define os endpoints HTTP.

Exemplo:

```
GET /customers
POST /customers
PUT /customers/{id}
DELETE /customers/{id}
```

---

# 6. Regra de Ouro do Backend

Quero deixar isso muito claro.

```
Controller/Route não contém regra de negócio.
```

A rota apenas:

- recebe a requisição;
- valida o schema;
- chama o service;
- retorna resposta.

A regra fica no service.

O banco fica no repository.

Essa separação será mantida durante todo o projeto.

---

# 7. Estrutura do Frontend

```
frontend/

└── src/

    ├── components/
    ├── pages/
    ├── layouts/
    ├── services/
    ├── hooks/
    ├── contexts/
    ├── routes/
    ├── types/
    ├── utils/
    └── main.tsx
```

---

# 8. Páginas da V1

```
Login

Dashboard

Clientes

Barbeiros

Serviços

Agenda

Pagamentos

Financeiro

Configurações
```

---

# 9. Componentes principais

```
Button
Input
Modal
Table
Card
Sidebar
Header
Badge
Alert
Calendar
```

Não criaremos uma biblioteca de UI complexa.

Apenas componentes reutilizáveis necessários para a V1.

---

# 10. Comunicação Frontend → Backend

Teremos um arquivo central:

```
frontend/src/services/api.ts
```

Responsável por configurar o Axios.

```
importaxiosfrom"axios";

exportconstapi=axios.create({
  baseURL:import.meta.env.VITE_API_URL,
});
```

O token JWT será enviado nas requisições protegidas.

---

# 11. Banco de Dados

Na próxima sprint faremos o modelo completo.

Mas a arquitetura inicial já prevê as principais entidades:

```
users
customers
barbers
service_categories
services
appointments
appointment_services
payments
financial_transactions
business_settings
audit_logs
```

A presença de `appointment_services` vem da regra:

> Um atendimento pode conter mais de um serviço.
>

Essa decisão nasceu das regras de negócio, não do banco.

---

# 12. Autenticação e Autorização

Usaremos:

```
JWT + RBAC
```

Perfis:

```
ADMIN
BARBER
CUSTOMER
```

Na V1:

- cada usuário possui um perfil;
- rotas privadas exigem token;
- algumas rotas exigem permissões específicas.

---

# 13. Testes

Teremos testes em três níveis:

```
unit
integration
e2e
```

Para a V1, foco principal:

- regras de agendamento;
- conflitos de horário;
- login;
- permissões;
- pagamentos;
- cálculo financeiro.

---

# 14. Docker

Estrutura prevista:

```
docker-compose.yml

services:
  backend
  frontend
  postgres
```

Na fase de deploy, adicionaremos:

```
nginx
```

---

# 15. Estrutura do Repositório

```
barberflow/

├── backend/
├── frontend/
├── database/
├── docker/
├── docs/
├── tests/
├── .github/
├── docker-compose.yml
├── README.md
└── LICENSE
```

Essa estrutura segue o padrão que definimos no Módulo 14. 🚀 MÓDULO 14 — MASTERCLASS DE PROJETOS FULL STACK P 38a365ecbc80802883f9c8e3c143b466.md

---

# 16. Decisões Arquiteturais Registradas

Até agora temos:

```
DEC-001 — Monólito Modular
DEC-002 — RBAC
DEC-003 — Multiempresa no Futuro
DEC-004 — Soft Delete
DEC-005 — Performance antes de Otimização
DEC-006 — Simplicidade
DEC-007 — Máquina de Estados
DEC-008 — Histórico Imutável
DEC-009 — MVP orientado por Casos de Uso
DEC-010 — Fluxos antes de Telas
DEC-011 — Escopo Protegido
DEC-012 — Roadmap Orientado por Valor
DEC-013 — FastAPI como Backend da V1
DEC-014 — PostgreSQL como Banco Principal
DEC-015 — React + TypeScript no Frontend
```

---

# 17. Riscos Técnicos Iniciais

Todo projeto profissional deve identificar riscos cedo.

## Risco 1 — Agenda ficar complexa demais

Mitigação:

Começar com agenda diária e semanal simples.

---

## Risco 2 — Financeiro crescer fora do escopo

Mitigação:

Na V1, financeiro será fluxo de caixa básico.

---

## Risco 3 — Multiempresa contaminar a V1

Mitigação:

Preparar arquitetura, mas não implementar multiempresa agora.

---

## Risco 4 — Frontend virar um dashboard pesado

Mitigação:

Criar apenas indicadores úteis para o MVP.

---

# 18. Critério para iniciar a Sprint 1

A Sprint 1 pode começar quando tivermos:

- visão do produto definida;
- requisitos definidos;
- regras de negócio definidas;
- MVP fechado;
- arquitetura inicial definida.

Status:
```
✅ Pronto
```
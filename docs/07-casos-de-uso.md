# Casos de Uso

> **"Os requisitos dizem o que o sistema faz. Os casos de uso mostram como ele é utilizado."**
>

A partir daqui vamos começar a enxergar o BarberFlow funcionando.

---

# O que é um Caso de Uso?

É a descrição de uma interação completa entre um usuário e o sistema para atingir um objetivo.

Exemplo:

> "Cadastrar Cliente"
>

Não basta dizer isso.

Precisamos responder:

- Quem faz?
- Quando faz?
- O que acontece?
- O que pode dar errado?
- Qual o resultado?

---

# Como documentaremos?

Todos seguirão exatamente este padrão.

```
Nome

Objetivo

Atores

Pré-condições

Fluxo Principal

Fluxos Alternativos

Fluxos de Exceção

Pós-condições

Regras Relacionadas
```

Esse padrão é inspirado na UML, mas simplificado para ser realmente útil no dia a dia.

---

# UC-001 — Login

## Objetivo

Permitir que um usuário autenticado acesse o sistema.

---

## Atores

- Administrador
- Barbeiro
- Cliente

---

## Pré-condições

- Usuário cadastrado.
- Usuário ativo.

---

## Fluxo Principal

```
Usuário acessa a tela de login

↓

Informa e-mail

↓

Informa senha

↓

Sistema valida credenciais

↓

Sistema gera JWT

↓

Sistema redireciona para o Dashboard
```

---

## Fluxos Alternativos

Senha incorreta.

↓

Sistema informa:

```
Usuário ou senha inválidos.
```

---

Usuário inativo.

↓

Sistema informa:

```
Sua conta está desativada.
```

---

## Pós-condição

Usuário autenticado.

---

## Requisitos relacionados

RF-001 ao RF-006

RN-001 ao RN-004

---

# UC-002 — Cadastro de Cliente

Este será um dos casos de uso mais frequentes.

---

## Objetivo

Cadastrar um novo cliente.

---

## Ator

Administrador

ou

Barbeiro.

---

## Pré-condições

Usuário autenticado.

---

## Fluxo Principal

```
Seleciona

Clientes

↓

Novo Cliente

↓

Preenche Nome

↓

Telefone

↓

Email (Opcional)

↓

Observações

↓

Salvar

↓

Sistema valida

↓

Sistema grava

↓

Mensagem de sucesso
```

---

## Fluxos Alternativos

Telefone já cadastrado.

↓

Sistema pergunta:

```
Deseja abrir o cadastro existente?
```

Essa decisão melhora muito a experiência do usuário e evita duplicidades.

---

## Fluxos de Exceção

Nome vazio.

↓

Sistema impede salvar.

---

Telefone inválido.

↓

Sistema solicita correção.

---

## Pós-condição

Cliente disponível para novos agendamentos.

---

# UC-003 — Criar Agendamento

Agora chegamos ao caso de uso mais importante do sistema.

---

## Objetivo

Reservar um horário para um cliente.

---

## Ator

Administrador.

Barbeiro.

Cliente (quando habilitado).

---

## Pré-condições

- Cliente ativo.
- Serviço ativo.
- Barbeiro ativo.

---

## Fluxo Principal

```
Agenda

↓

Selecionar Dia

↓

Selecionar Horário

↓

Selecionar Barbeiro

↓

Selecionar Cliente

↓

Selecionar Serviço

↓

Confirmar

↓

Sistema valida

↓

Sistema cria atendimento

↓

Agenda atualizada
```

---

## Fluxos Alternativos

Horário ocupado.

↓

Sistema apresenta opções disponíveis.

---

Barbeiro indisponível.

↓

Sistema permite selecionar outro profissional.

---

## Fluxos de Exceção

Cliente desativado.

↓

Não permite agendar.

---

Serviço desativado.

↓

Não aparece na lista.

---

## Pós-condição

Atendimento criado com status:

```
AGENDADO
```

---

# UC-004 — Cancelar Agendamento

---

## Objetivo

Cancelar um atendimento.

---

## Fluxo Principal

```
Abrir Agendamento

↓

Cancelar

↓

Sistema solicita confirmação

↓

Motivo

↓

Confirmar

↓

Status alterado

↓

Horário liberado
```

---

## Fluxos Alternativos

Usuário desistiu.

↓

Nada acontece.

---

## Fluxos de Exceção

Atendimento já concluído.

↓

Sistema impede cancelamento.

---

## Pós-condição

Status:

```
CANCELADO
```

---

# UC-005 — Registrar Pagamento

---

## Objetivo

Registrar pagamento do atendimento.

---

## Fluxo Principal

```
Abrir Atendimento

↓

Registrar Pagamento

↓

Selecionar Forma

↓

Informar Desconto

↓

Confirmar

↓

Sistema registra

↓

Atualiza Financeiro

↓

Atualiza Dashboard
```

---

## Fluxos Alternativos

Pagamento parcial.

↓

**Não suportado na V1.**

Essa decisão simplifica a primeira versão.

---

## Fluxos de Exceção

Valor inválido.

↓

Sistema bloqueia operação.

---

## Pós-condição

Pagamento registrado.

---

# UC-006 — Consultar Dashboard

Esse é o principal caso de uso do Administrador.

---

## Objetivo

Visualizar indicadores do negócio.

---

## Fluxo Principal

```
Login

↓

Dashboard

↓

Selecionar Período

↓

Sistema calcula indicadores

↓

Exibe:

Faturamento

Lucro

Clientes

Atendimentos

Serviços mais vendidos
```

---

## Fluxos Alternativos

Sem movimentação.

↓

Dashboard exibe:

```
Nenhum dado encontrado para o período.
```

---

# Mapa Geral dos Casos de Uso

```
                    BARBERFLOW

                           │

        ┌──────────────────┼─────────────────┐

        │                  │                 │

   Administrador       Barbeiro        Cliente

        │                  │                 │

        ├── Login          │                 │

        ├── Dashboard      │                 │

        ├── Clientes       ├── Agenda        ├── Login

        ├── Agenda         ├── Atendimento   ├── Agendar

        ├── Financeiro     ├── Pagamentos    ├── Cancelar

        ├── Relatórios     │                 └── Histórico

        └── Configurações
```

---

# Priorização dos Casos de Uso

Agora vamos definir o que entra na V1.

## Essenciais (MVP)

| Caso de Uso | V1 |
| --- | --- |
| Login | ✅ |
| Cadastro de Cliente | ✅ |
| Cadastro de Barbeiro | ✅ |
| Cadastro de Serviço | ✅ |
| Criar Agendamento | ✅ |
| Cancelar Agendamento | ✅ |
| Registrar Pagamento | ✅ |
| Dashboard | ✅ |

---

## Pós-MVP (V1.1 e V1.2)

| Caso de Uso | Versão |
| --- | --- |
| Recuperação de senha | V1.1 |
| Upload de foto | V1.1 |
| Notificações | V1.1 |
| Portal do Cliente | V1.2 |
| Relatórios avançados | V1.2 |
| Programa de fidelidade | V2.0 |
| Multiempresa | V2.0 |

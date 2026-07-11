# Requisitos Funcionais

> **"Se o código responde à pergunta 'como?', os requisitos respondem à pergunta 'o quê?'."**
>

Este documento será o **contrato do produto**.

Tudo que desenvolvermos daqui para frente deverá existir porque está especificado aqui.

E tudo que estiver aqui deverá existir no sistema.

É a nossa principal fonte de verdade.

---

# O que é um requisito funcional?

Um requisito funcional descreve uma funcionalidade que o sistema deve oferecer.

Exemplo:

> O sistema deve permitir cadastrar clientes.
>

Isso é um requisito.

Já:

> O sistema deve responder em menos de dois segundos.
>

Isso **não** é funcional.

É um requisito não funcional.

---

# Como vamos escrever?

Não quero uma lista enorme e desorganizada.

Vamos separar por módulos.

Assim como faremos no código.

```
Sistema

↓

Módulos

↓

Funcionalidades

↓

Requisitos
```

Isso facilitará muito a evolução do projeto.

---

# 📂 Módulo 1 — Autenticação

## Objetivo

Permitir acesso seguro ao sistema.

---

### RF-001

O sistema deve permitir login utilizando e-mail e senha.

---

### RF-002

O sistema deve validar as credenciais.

---

### RF-003

O sistema deve gerar um token JWT após autenticação.

---

### RF-004

O sistema deve impedir acesso às áreas protegidas sem autenticação.

---

### RF-005

O sistema deve permitir logout.

---

### RF-006

O sistema deve permitir alteração de senha.

---

# 📂 Módulo 2 — Usuários

Agora começa uma decisão importante.

Todo barbeiro será um usuário.

Todo administrador será um usuário.

Cliente também será um usuário.

Ou seja:

```
Usuário

↓

Administrador

Barbeiro

Cliente
```

Essa decisão simplificará bastante nossa autenticação.

---

### RF-007

Cadastrar usuário.

---

### RF-008

Editar usuário.

---

### RF-009

Desativar usuário.

(Não excluir.)

---

### RF-010

Pesquisar usuários.

---

### RF-011

Alterar perfil de acesso.

---

# 📂 Módulo 3 — Clientes

Este é um dos módulos mais importantes.

---

### RF-012

Cadastrar cliente.

---

### RF-013

Editar cliente.

---

### RF-014

Pesquisar cliente.

---

### RF-015

Visualizar histórico.

---

### RF-016

Desativar cliente.

---

### RF-017

Registrar observações.

Exemplo:

```
Cliente prefere tesoura.

Cliente possui alergia.

Cliente gosta da barba mais baixa.
```

Essas informações agregam muito valor ao atendimento.

---

# 📂 Módulo 4 — Barbeiros

---

### RF-018

Cadastrar barbeiro.

---

### RF-019

Editar barbeiro.

---

### RF-020

Definir especialidades.

---

### RF-021

Definir horário de trabalho.

---

### RF-022

Visualizar agenda.

---

# 📂 Módulo 5 — Serviços

---

### RF-023

Cadastrar serviço.

---

### RF-024

Editar serviço.

---

### RF-025

Definir duração.

---

### RF-026

Definir preço.

---

### RF-027

Ativar/Inativar serviço.

---

### RF-028

Organizar serviços por categoria.

---

# 📂 Módulo 6 — Agenda

Aqui está o coração do sistema.

---

### RF-029

Criar agendamento.

---

### RF-030

Cancelar agendamento.

---

### RF-031

Reagendar atendimento.

---

### RF-032

Listar horários disponíveis.

---

### RF-033

Bloquear horários indisponíveis.

---

### RF-034

Evitar conflito de horários.

Este requisito será uma regra crítica do sistema.

---

# 📂 Módulo 7 — Pagamentos

---

### RF-035

Registrar pagamento.

---

### RF-036

Informar forma de pagamento.

Exemplos:

- PIX
- Dinheiro
- Cartão

---

### RF-037

Registrar desconto.

---

### RF-038

Registrar observações.

---

# 📂 Módulo 8 — Dashboard

Este módulo responde às perguntas do dono da barbearia.

---

### RF-039

Exibir faturamento do dia.

---

### RF-040

Quantidade de atendimentos.

---

### RF-041

Serviços mais vendidos.

---

### RF-042

Barbeiro com maior faturamento.

---

### RF-043

Quantidade de novos clientes.

---

# 📂 Módulo 9 — Financeiro

---

### RF-044

Registrar entrada.

---

### RF-045

Registrar saída.

---

### RF-046

Consultar fluxo de caixa.

---

### RF-047

Consultar lucro.

---

### RF-048

Filtrar por período.

---

# Resumo

Até aqui já temos **48 requisitos funcionais**.

Observe algo interessante.

Ainda não falamos sobre:

- FastAPI
- React
- PostgreSQL
- Docker

E isso é proposital.

Porque...

## A tecnologia não define o produto.

O produto define a tecnologia.

Essa é uma mudança de mentalidade muito importante.

---

# O que ainda está faltando?

Embora tenhamos uma boa base, quero adicionar alguns requisitos que considero essenciais para um SaaS moderno e que complementam o material original.

## 📂 Módulo 10 — Auditoria e Histórico

### RF-049

Registrar data e hora de criação dos registros.

### RF-050

Registrar data e hora da última atualização.

### RF-051

Registrar qual usuário realizou operações críticas (cadastros, alterações e exclusões lógicas).

> **Por quê?** Isso facilita auditoria e investigação de problemas, além de ser uma prática comum em sistemas corporativos.
>

---

## 📂 Módulo 11 — Configurações

### RF-052

Permitir configurar horários de funcionamento da barbearia.

### RF-053

Permitir configurar dias de folga e feriados.

### RF-054

Permitir configurar intervalos entre atendimentos.

> **Por quê?** Essas configurações impactam diretamente a agenda e evitam que regras fiquem "presas" no código.
>
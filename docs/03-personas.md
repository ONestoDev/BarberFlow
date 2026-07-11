# Personas

> **"Se você tenta construir um sistema para todo mundo, acaba construindo um sistema para ninguém."**
>

Uma das maiores falhas em projetos de software é desenvolver funcionalidades sem saber quem realmente irá utilizá-las.

Hoje vamos definir **quem são nossos usuários**.

---

# Antes de criar as personas...

Quero estabelecer uma regra.

Não vamos criar personas fictícias apenas para preencher documentação.

Cada persona deve responder:

- Quem utiliza o sistema?
- Qual seu objetivo?
- Quais dores possui?
- O que espera do sistema?
- Como mede sucesso?

Essas respostas irão influenciar decisões durante todo o projeto.

---

# Nosso ecossistema

Antes de detalhar as personas, precisamos visualizar quem participa do sistema.

```
                  BarberFlow

                        │

        ┌───────────────┼───────────────┐

        │               │               │

     Administrador   Barbeiro      Cliente
```

Esses três perfis são suficientes para a V1.

Nada além disso.

---

# 👑 Persona 1 — Administrador

## Quem é?

É o proprietário da barbearia.

Pode ser:

- dono único;
- sócio;
- gerente responsável.

---

## Objetivo

Administrar toda a empresa.

---

## Responsabilidades

- cadastrar funcionários;
- cadastrar serviços;
- acompanhar faturamento;
- controlar estoque;
- configurar horários;
- acompanhar indicadores.

---

## Principais dores

Hoje ele sofre porque:

- agenda é desorganizada;
- não sabe o lucro real;
- esquece pagamentos;
- perde clientes;
- não possui relatórios.

---

## Como mede sucesso?

Quando consegue responder rapidamente perguntas como:

- Quanto faturei hoje?
- Qual barbeiro atendeu mais?
- Quanto entrou via PIX?
- Qual serviço vendeu mais?

---

## Funcionalidades mais importantes

Para ele, prioridade máxima:

```
Dashboard

↓

Financeiro

↓

Agenda

↓

Clientes

↓

Funcionários
```

---

# ✂️ Persona 2 — Barbeiro

Quem realmente usa o sistema o dia inteiro.

---

## Objetivo

Atender clientes.

Não administrar empresa.

---

## Responsabilidades

- visualizar agenda;
- iniciar atendimento;
- finalizar atendimento;
- cadastrar clientes;
- remarcar horários.

---

## Principais dores

- agenda confusa;
- horários duplicados;
- esquecer cliente;
- demora para localizar informações.

---

## Como mede sucesso?

Ele quer:

> Abrir o sistema e saber imediatamente:
>

```
Quem será o próximo cliente?
```

Nada além disso.

---

## Funcionalidades prioritárias

```
Agenda

↓

Cliente

↓

Serviços

↓

Pagamento
```

Perceba que ele praticamente não utiliza o Dashboard Administrativo.

---

# 👤 Persona 3 — Cliente

A pessoa que agenda.

---

## Objetivo

Marcar um horário rapidamente.

---

## Responsabilidades

Praticamente nenhuma.

Ele apenas deseja:

- agendar;
- cancelar;
- remarcar;
- acompanhar histórico.

---

## Dores

As maiores são:

- demora para responder no WhatsApp;
- esquecer horário;
- dificuldade para remarcar.

---

## Como mede sucesso?

Em menos de dois minutos ele deve conseguir:

```
Entrar

↓

Escolher barbeiro

↓

Escolher serviço

↓

Escolher horário

↓

Confirmar
```

Fim.

Quanto menos passos melhor.

---

# Comparando as Personas

| Persona | Objetivo principal | Funcionalidade mais importante |
| --- | --- | --- |
| 👑 Administrador | Gerenciar a empresa | Dashboard |
| ✂️ Barbeiro | Atender clientes | Agenda |
| 👤 Cliente | Agendar atendimento | Agendamento |

Essa tabela parece simples, mas ela será consultada várias vezes ao longo do projeto.

---

# O que aprendemos com isso?

Uma decisão de UX importante aparece imediatamente.

O Dashboard do Administrador NÃO pode ser igual ao Dashboard do Barbeiro.

Exemplo.

Administrador:

```
Faturamento

Lucro

Financeiro

Relatórios

Estoque
```

---

Barbeiro:

```
Próximo cliente

Agenda de hoje

Histórico

Atendimento
```

Perceba que são produtos diferentes dentro do mesmo sistema.

---

# Jornada de cada usuário

Agora vamos desenhar rapidamente o fluxo de cada persona.

---

## Administrador

```
Login

↓

Dashboard

↓

Financeiro

↓

Clientes

↓

Funcionários

↓

Relatórios
```

---

## Barbeiro

```
Login

↓

Agenda

↓

Seleciona Cliente

↓

Realiza Atendimento

↓

Finaliza Atendimento
```

---

## Cliente

```
Login

↓

Escolhe Serviço

↓

Escolhe Barbeiro

↓

Escolhe Horário

↓

Confirma Agendamento
```

---
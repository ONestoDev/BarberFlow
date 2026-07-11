# Regras de Negócio

> **"Regras de negócio não pertencem ao banco de dados, ao frontend ou ao backend. Elas pertencem ao domínio."**
>

Esse documento será o que mais consultaremos durante o desenvolvimento.

---

# Antes de começar...

Quero definir algo importante.

Uma regra de negócio **não é** uma funcionalidade.

Exemplo:

❌

```
Cadastrar Cliente
```

Isso é uma funcionalidade.

Agora:

✔️

```
Não permitir dois clientes no mesmo horário com o mesmo barbeiro.
```

Isso é uma regra de negócio.

Percebe a diferença?

---

# O domínio do nosso sistema

Depois da Sprint anterior conseguimos identificar os grandes módulos.

Agora precisamos descobrir suas regras.

```
Usuários

↓

Clientes

↓

Barbeiros

↓

Serviços

↓

Agenda

↓

Pagamento

↓

Financeiro
```

Vamos definir as regras de cada um.

---

# 👤 Usuários

## RN-001

Todo usuário deverá possuir exatamente um perfil na V1.

Perfis:

```
ADMIN

BARBEIRO

CLIENTE
```

---

## RN-002

Usuários desativados não poderão realizar login.

---

## RN-003

O e-mail será único.

Nunca poderão existir dois usuários com o mesmo e-mail.

---

## RN-004

A senha nunca será armazenada em texto puro.

---

# 👥 Clientes

## RN-005

Todo cliente deverá possuir pelo menos:

- nome;
- telefone.

O e-mail será opcional na V1.

**Justificativa:** muitas barbearias trabalham apenas com WhatsApp.

---

## RN-006

Clientes não serão removidos fisicamente.

Apenas desativados.

---

## RN-007

O histórico do cliente nunca poderá ser apagado.

Mesmo que ele deixe de frequentar a barbearia.

---

## RN-008

Um cliente poderá possuir observações internas.

Exemplo:

```
Prefere atendimento com João.

Gosta de barba marcada.

É alérgico a determinado produto.
```

Essas observações não serão visíveis ao cliente.

---

# ✂️ Barbeiros

## RN-009

Todo barbeiro deverá possuir agenda própria.

---

## RN-010

Cada barbeiro definirá seus horários de trabalho.

Exemplo:

```
08:00 às 18:00
```

---

## RN-011

Horários de almoço deverão bloquear automaticamente novos agendamentos.

---

## RN-012

Um barbeiro poderá estar temporariamente indisponível.

Exemplos:

- férias;
- licença;
- treinamento.

---

# 💈 Serviços

## RN-013

Todo serviço deverá possuir duração.

Exemplo:

```
Corte

30 minutos
```

---

## RN-014

Todo serviço deverá possuir preço.

---

## RN-015

Serviços poderão ser desativados, mas nunca removidos se já tiverem sido utilizados em atendimentos.

Isso preserva o histórico financeiro.

---

## RN-016

Um atendimento poderá conter mais de um serviço.

Exemplo:

```
Corte

+

Barba

+

Sobrancelha
```

Essa regra impactará diretamente a modelagem do banco de dados. Em vez de um único serviço por atendimento, teremos uma relação que permita múltiplos serviços.

---

# 📅 Agenda

Aqui está o núcleo do produto.

---

## RN-017

Não poderá existir conflito de horário.

Exemplo:

```
João

09:00

Corte
```

Enquanto esse atendimento estiver ativo, outro cliente não poderá ser agendado para o mesmo barbeiro no mesmo horário.

---

## RN-018

O horário deverá respeitar a duração do serviço.

Exemplo:

```
09:00

↓

Corte

↓

30 minutos

↓

Fim

09:30
```

Se o próximo horário disponível for às 09:30, ele não poderá ser ocupado por outro atendimento iniciado às 09:15.

---

## RN-019

Agendamentos cancelados liberarão automaticamente o horário.

---

## RN-020

Atendimentos concluídos não poderão ser editados.

Apenas consultados.

Caso seja necessário corrigir informações financeiras ou administrativas, isso será feito por operações específicas e registradas em auditoria.

---

## RN-021

Um cliente poderá possuir vários agendamentos futuros.

Não existe limite.

---

## RN-022

O sistema permitirá reagendamento.

Ao reagendar:

- o horário antigo será liberado;
- o novo horário será validado antes da confirmação.

---

## RN-023

O sistema deverá registrar o status do atendimento.

Estados da V1:

```
AGENDADO

↓

CONFIRMADO

↓

EM_ATENDIMENTO

↓

CONCLUÍDO
```

ou

```
AGENDADO

↓

CANCELADO
```

Essa máquina de estados evitará mudanças inconsistentes.

---

# 💳 Pagamentos

## RN-024

Todo pagamento estará vinculado a um atendimento.

Na V1 não haverá pagamentos avulsos.

---

## RN-025

O pagamento poderá ocorrer antes ou depois do atendimento.

Isso cobre diferentes formas de operação da barbearia.

---

## RN-026

Formas de pagamento aceitas na V1:

- Dinheiro
- PIX
- Cartão de Débito
- Cartão de Crédito

---

## RN-027

Um atendimento poderá receber desconto.

Mas:

O desconto deverá ficar registrado.

Nunca substituir o valor original do serviço.

Isso é importante para relatórios futuros.

---

# 💰 Financeiro

## RN-028

Toda entrada deverá possuir origem.

Exemplo:

```
Atendimento

Venda de Produto
```

---

## RN-029

Toda saída deverá possuir categoria.

Exemplos:

- aluguel;
- energia;
- água;
- fornecedores.

---

## RN-030

Nenhuma movimentação financeira poderá ser excluída.

Caso haja erro, será criada uma movimentação corretiva, preservando o histórico.

Essa prática é comum em sistemas financeiros para garantir rastreabilidade.

---

# 📊 Dashboard

## RN-031

Todos os indicadores serão calculados a partir dos dados reais do sistema.

Nenhum valor será digitado manualmente.

---

## RN-032

Indicadores deverão considerar filtros por período.

Exemplos:

- hoje;
- semana;
- mês;
- intervalo personalizado.

---

# 🔔 Notificações (Preparação para futuras versões)

Embora não implementemos notificações na V1, vamos preparar o domínio.

## RN-033

Eventos importantes deverão ser registrados.

Exemplos:

- agendamento criado;
- atendimento cancelado;
- pagamento registrado.

No futuro, esses eventos poderão gerar e-mails, mensagens ou integrações sem alterar as regras centrais do sistema.

---

# 📌 Regras Gerais

## RN-034

Toda alteração crítica deverá registrar:

- usuário responsável;
- data;
- hora.

---

## RN-035

Todas as datas serão armazenadas em UTC.

A apresentação para o usuário será convertida conforme a configuração da aplicação.

Essa decisão evita problemas com horário de verão e facilita futuras expansões.

---

## RN-036

O sistema nunca deverá confiar apenas nas validações do frontend.

Toda regra de negócio será validada novamente no backend.

Essa é uma regra de ouro em aplicações web.

---

# 📊 Máquina de Estados do Atendimento

Uma das decisões mais importantes até agora.

```
                 AGENDADO
                 /      \
                /        \
        CANCELADO     CONFIRMADO
                           │
                           ▼
                    EM_ATENDIMENTO
                           │
                           ▼
                      CONCLUÍDO
```

### Regras

- Não é possível voltar de **CONCLUÍDO** para **AGENDADO**.
- Um atendimento **CANCELADO** não pode ser concluído.
- Apenas atendimentos **CONFIRMADOS** podem entrar em **EM_ATENDIMENTO**.

Essa máquina de estados será implementada no backend e testada automaticamente.
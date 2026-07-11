# MVP (Minimum Viable Product)

> **"MVP não significa produto incompleto. Significa o menor produto capaz de entregar valor."**
>

Nosso objetivo não é fazer um sistema pequeno.

É fazer um sistema **enxuto, mas completo**.

---

# O que é sucesso para a V1?

Quero definir isso antes de qualquer coisa.

Uma barbearia deverá conseguir utilizar o BarberFlow durante um dia inteiro de trabalho sem precisar recorrer a:

- WhatsApp para organizar agenda;
- Caderno para controlar atendimentos;
- Planilhas para acompanhar faturamento.

Se conseguirmos isso...

**A V1 foi um sucesso.**

---

# Objetivo da Versão 1.0

> Permitir que uma barbearia gerencie clientes, agenda, serviços e pagamentos em um único sistema, com segurança, simplicidade e confiabilidade.
>

Essa frase será nosso guia.

---

# Escopo do MVP

Vamos dividir em módulos.

---

# 🔐 Autenticação

## Entregaremos

- Login
- Logout
- JWT
- Controle de acesso por perfil (RBAC)

---

## Não entregaremos

- Login com Google
- Login com Facebook
- MFA (autenticação em dois fatores)
- Recuperação de senha por e-mail

Esses itens ficam para versões futuras.

---

# 👥 Usuários

## Entregaremos

- Cadastro
- Edição
- Desativação
- Perfis

Administrador

Barbeiro

Cliente

---

## Não entregaremos

- Convites por e-mail
- Múltiplos perfis por usuário
- Organização por equipes

---

# 👤 Clientes

## Entregaremos

- Cadastro
- Pesquisa
- Histórico
- Observações
- Desativação

---

## Não entregaremos

- Programa de fidelidade
- Cashback
- Avaliações
- Fotos

---

# ✂️ Barbeiros

## Entregaremos

- Cadastro
- Agenda
- Especialidades
- Horário de trabalho

---

## Não entregaremos

- Comissão automática
- Metas individuais
- Ranking

---

# 💈 Serviços

## Entregaremos

- Cadastro
- Categoria
- Duração
- Preço

---

## Não entregaremos

- Pacotes promocionais
- Combos
- Assinaturas

---

# 📅 Agenda

Este será nosso módulo principal.

## Entregaremos

- Criar agendamento
- Cancelar
- Reagendar
- Agenda diária
- Agenda semanal
- Horários disponíveis
- Validação de conflitos

---

## Não entregaremos

- Agenda mensal
- Arrastar e soltar
- Sincronização com Google Calendar

---

# 💳 Pagamentos

## Entregaremos

- Registrar pagamento
- PIX
- Dinheiro
- Débito
- Crédito
- Desconto

---

## Não entregaremos

- Pagamento parcial
- Parcelamento
- Gateway de pagamento
- PIX automático

---

# 💰 Financeiro

## Entregaremos

- Entradas
- Saídas
- Fluxo de caixa
- Lucro

---

## Não entregaremos

- DRE
- Balanço patrimonial
- Conciliação bancária

---

# 📊 Dashboard

## Entregaremos

Indicadores:

- faturamento;
- atendimentos;
- novos clientes;
- serviços mais vendidos;
- barbeiro com maior faturamento.

---

## Não entregaremos

- gráficos avançados;
- BI;
- comparativos anuais;
- previsões.

---

# O que deliberadamente ficará fora da V1?

Esta é uma lista importante.

Não porque sejam funcionalidades ruins.

Mas porque **não são necessárias para validar o produto**.

## V1 NÃO TERÁ

❌ Chat.

❌ IA.

❌ Mobile.

❌ WhatsApp.

❌ Multiempresa.

❌ Marketplace.

❌ Cupons.

❌ Fidelidade.

❌ WebSocket.

❌ Pagamentos online.

❌ Assinaturas.

❌ Integrações externas.

E isso é uma decisão consciente.

---

# Definition of Done (DoD)

Agora vem uma prática muito utilizada por equipes ágeis.

Uma funcionalidade **não está pronta** apenas porque "funciona".

Ela só será considerada concluída quando cumprir todos estes critérios.

## Para Backend

- Código implementado.
- Testes passando.
- Documentação atualizada.
- Swagger atualizado.
- Code Review realizado.

---

## Para Frontend

- Responsivo.
- Validado.
- Integrado à API.
- Tratamento de erros.
- Componentizado.

---

## Para Banco

- Migration criada.
- Constraints definidas.
- Índices criados.
- Relacionamentos validados.

---

## Para Projeto

- README atualizado.
- Changelog atualizado.
- Decisões arquiteturais registradas.

---

# Critérios de Aceitação da V1

A versão 1.0 estará pronta quando conseguirmos executar este fluxo sem falhas:

```
Administrador

↓

Login

↓

Cadastrar Barbeiro

↓

Cadastrar Serviço

↓

Cadastrar Cliente

↓

Criar Agendamento

↓

Registrar Atendimento

↓

Registrar Pagamento

↓

Consultar Dashboard

↓

Consultar Financeiro

↓

Logout
```

Se esse fluxo funcionar de ponta a ponta...

Temos um MVP.

---

# Indicadores da V1

Quero definir metas objetivas.

| Indicador | Meta |
| --- | --- |
| Casos de Uso do MVP | 100% implementados |
| Requisitos Funcionais do MVP | 100% |
| Regras de Negócio críticas | 100% |
| Testes das regras críticas | ≥ 80% |
| Deploy em produção | Sim |
| Docker | Sim |
| Documentação | Completa |

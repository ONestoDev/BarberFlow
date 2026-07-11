## Problema de Negócio

> **"Um software excelente não nasce de uma ideia brilhante. Ele nasce da compreensão profunda de um problema."**
>

Essa frase vai nos acompanhar durante todo o projeto.

---

# Antes de construir...

Quero que você imagine a seguinte cena.

---

Carlos é dono de uma barbearia.

Ele possui:

- 3 barbeiros;
- cerca de 800 clientes cadastrados (na cabeça dele);
- agenda pelo WhatsApp;
- pagamentos em PIX, dinheiro e cartão;
- vende pomadas, shampoos e óleos para barba.

Todos os dias acontecem coisas como:

> "João pediu para remarcar."
>

> "Pedro esqueceu do horário."
>

> "O barbeiro Lucas está de férias."
>

> "A pomada acabou."
>

> "Quanto faturamos este mês?"
>

> "Qual barbeiro atendeu mais clientes?"
>

> "Quem não vem há mais de 90 dias?"
>

Carlos consegue responder algumas dessas perguntas...

Mas demora.

Às vezes precisa abrir conversas antigas.

Às vezes procura num caderno.

Às vezes simplesmente não sabe.

---

# Esse é o verdadeiro problema

Muitas pessoas acreditam que o problema é:

> "A barbearia precisa de um sistema."
>

Na verdade, não.

O problema é outro.

## O dono não possui informação para tomar decisões.

E isso muda completamente a forma como construiremos o software.

O nosso sistema não servirá apenas para:

- cadastrar clientes;
- marcar horários.

Ele servirá para responder perguntas importantes do negócio.

---

# O nosso produto é um sistema de gestão

Essa é uma decisão importante.

Nós não estamos construindo um "agendador".

Estamos construindo um **ERP especializado para barbearias**.

Isso muda tudo.

---

# Os quatro pilares do sistema

Depois de analisar o problema, identifiquei quatro áreas principais.

## 📅 Agenda

Controla:

- horários;
- barbeiros;
- disponibilidade;
- reagendamentos;
- cancelamentos.

Objetivo:

Nunca perder um atendimento.

---

## 👥 Clientes

Controla:

- cadastro;
- histórico;
- preferências;
- frequência;
- fidelização.

Objetivo:

Conhecer o cliente.

---

## 💰 Financeiro

Controla:

- recebimentos;
- despesas;
- caixa;
- faturamento.

Objetivo:

Saber se a empresa realmente está dando lucro.

---

## 📊 Gestão

Controla:

- indicadores;
- relatórios;
- desempenho.

Objetivo:

Auxiliar o dono na tomada de decisões.

---

# O que realmente venderemos?

Aqui está uma mudança de mentalidade.

Nós não vendemos software.

Vendemos:

## Organização.

Vendemos:

## Tempo.

Vendemos:

## Informação.

Vendemos:

## Tranquilidade.

Essa é a proposta de valor do BarberFlow.

---

# Proposta de Valor

Vamos escrever a primeira versão.

---

## BarberFlow

> Centralize clientes, agenda, financeiro e gestão da sua barbearia numa única plataforma simples, rápida e confiável, permitindo que você dedique menos tempo à administração e mais tempo ao crescimento do seu negócio.
>

Essa frase será a base da nossa landing page, do README e até da apresentação do produto.

---

# Diferenciais do nosso sistema

Aqui quero tomar uma decisão de produto.

Não quero copiar simplesmente sistemas existentes.

Quero que o nosso sistema tenha uma identidade própria.

Os diferenciais da V1 serão:

### Simplicidade

Um barbeiro deve aprender a usar o sistema em poucos minutos.

---

### Velocidade

As principais tarefas devem exigir poucos cliques.

---

### Interface limpa

Nada de telas poluídas.

---

### Dashboard realmente útil

Não queremos dezenas de gráficos sem propósito.

Queremos indicadores que respondam perguntas reais.

---

# Quais perguntas o nosso sistema deve responder?

Essa é uma técnica utilizada em Product Management.

Se o sistema não consegue responder essas perguntas, provavelmente ainda falta alguma funcionalidade.

No primeiro dia de uso, o dono da barbearia deve conseguir descobrir:

- Quanto faturou hoje?
- Quantos clientes foram atendidos?
- Quantos horários ainda estão livres?
- Quem cancelou?
- Quem faltou?
- Qual serviço é o mais vendido?
- Qual barbeiro atende mais clientes?
- Quanto entrou em dinheiro, PIX e cartão?
- Quanto foi gasto?
- Qual o lucro do dia?

Perceba que isso já nos dá pistas sobre quais dados precisaremos armazenar.

---

# O princípio que guiará todas as funcionalidades

Quero estabelecer uma regra de engenharia para este projeto.

> **Todas as funcionalidades precisam responder a uma necessidade real do negócio.**
>

Se, em algum momento, pensarmos em adicionar algo, faremos duas perguntas:

1. Qual problema essa funcionalidade resolve?
2. Ela traz valor para o usuário nesta versão?

Se a resposta for "não", ela vai para o roadmap futuro.

Essa disciplina evita que o produto cresça de forma desordenada.
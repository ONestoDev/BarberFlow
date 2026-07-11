# Requisitos Não Funcionais

> **"Os requisitos funcionais dizem o que o sistema faz. Os requisitos não funcionais dizem como ele deve se comportar."**
>

Eles serão o guia das nossas decisões técnicas durante todo o projeto.

---

# Antes de começar...

Imagine dois sistemas.

Sistema A

- Faz tudo.

Sistema B

- Faz tudo.
- Responde rapidamente.
- Nunca perde dados.
- Funciona em celular.
- É seguro.
- É fácil de manter.

Os dois possuem exatamente as mesmas funcionalidades.

Qual deles é melhor?

Obviamente o segundo.

A diferença entre eles está justamente nos requisitos não funcionais.

---

# Como organizaremos?

Dividiremos em categorias.

```
Performance

↓

Segurança

↓

Usabilidade

↓

Disponibilidade

↓

Escalabilidade

↓

Manutenibilidade

↓

Observabilidade
```

---

# 📂 Categoria 1 — Performance

Nosso sistema será utilizado durante o expediente inteiro.

Ele precisa ser rápido.

---

## RNF-001

As páginas deverão carregar em menos de **2 segundos** em condições normais de uso.

---

## RNF-002

As consultas comuns deverão responder em até **500 ms**.

Exemplos:

- clientes;
- agenda;
- serviços.

---

## RNF-003

Operações críticas deverão responder em até **2 segundos**.

Exemplo:

```
Criar agendamento

↓

Registrar pagamento

↓

Cadastrar cliente
```

---

## RNF-004

O Dashboard poderá levar um pouco mais de tempo, mas nunca ultrapassar **5 segundos**.

Por quê?

Porque envolve agregações e cálculos.

---

# 📂 Categoria 2 — Segurança

Aqui não aceitaremos atalhos.

---

## RNF-005

Toda comunicação será feita via **HTTPS** em produção.

---

## RNF-006

As senhas serão armazenadas utilizando algoritmo de hash seguro.

Nunca em texto puro.

---

## RNF-007

Todas as rotas privadas exigirão autenticação JWT.

---

## RNF-008

Cada usuário poderá acessar apenas os recursos permitidos pelo seu perfil (RBAC).

---

## RNF-009

O sistema deverá registrar tentativas de acesso inválidas.

---

# 📂 Categoria 3 — Usabilidade

Nosso maior diferencial será a simplicidade.

---

## RNF-010

Um barbeiro deverá conseguir aprender o sistema em menos de **30 minutos**.

---

## RNF-011

As tarefas principais deverão exigir o menor número possível de cliques.

Nossa meta:

```
Agendar cliente

≤ 5 cliques
```

---

## RNF-012

A interface deverá ser totalmente responsiva.

Desktop.

Tablet.

Celular.

---

## RNF-013

Mensagens de erro devem orientar o usuário sobre como resolver o problema.

Exemplo:

❌

```
Erro 500
```

✔️

```
O horário selecionado já foi reservado.

Escolha outro horário disponível.
```

---

# 📂 Categoria 4 — Disponibilidade

Mesmo sendo um MVP, vamos pensar como produto.

---

## RNF-014

O sistema deverá estar disponível **99% do tempo**.

---

## RNF-015

Backups do banco deverão ser realizados periodicamente (estratégia definida na fase de infraestrutura).

---

## RNF-016

Atualizações não devem causar perda de dados.

---

# 📂 Categoria 5 — Escalabilidade

Hoje teremos uma barbearia.

Amanhã podemos ter cem.

---

## RNF-017

A arquitetura deverá permitir adicionar novos módulos sem grandes alterações nos existentes.

---

## RNF-018

O sistema deverá suportar evolução para múltiplas empresas (multiempresa) sem reescrita completa.

---

## RNF-019

A API deverá ser stateless.

Isso facilitará futuras escalas horizontais.

---

# 📂 Categoria 6 — Manutenibilidade

Como Tech Lead...

Essa talvez seja minha categoria favorita.

---

## RNF-020

O código seguirá princípios SOLID.

---

## RNF-021

A arquitetura seguirá Clean Architecture simplificada.

---

## RNF-022

Cada módulo possuirá responsabilidade única.

---

## RNF-023

Nenhuma regra de negócio ficará dentro dos Controllers.

---

## RNF-024

Todo acesso ao banco passará pelo Repository.

---

## RNF-025

O projeto deverá possuir cobertura de testes para regras críticas.

Não vamos perseguir 100% de cobertura. Vamos focar no que realmente reduz riscos.

---

# 📂 Categoria 7 — Observabilidade

Quero adicionar uma categoria que muitos cursos ignoram.

Em produção, não basta o sistema funcionar. Precisamos entender o que está acontecendo.

---

## RNF-026

Todas as exceções deverão ser registradas em log.

---

## RNF-027

Operações críticas deverão gerar eventos de auditoria.

Exemplos:

- login;
- alteração de senha;
- cancelamento de agendamento;
- registro de pagamento.

---

## RNF-028

Cada requisição deverá possuir um identificador único (*Request ID*).

Isso facilitará a análise de problemas em produção.

> **Observação:** Não implementaremos isso logo na V1 do código. Apenas registraremos como requisito arquitetural para orientar a evolução do sistema.
>

---

# 📂 Categoria 8 — Qualidade do Código

Este projeto também será uma vitrine do seu trabalho.

---

## RNF-029

Todo código novo deverá seguir o padrão definido pelo projeto.

---

## RNF-030

Nenhuma funcionalidade será considerada concluída sem:

- implementação;
- testes;
- documentação atualizada.

---

## RNF-031

Toda alteração relevante deverá ser registrada no changelog.

Isso reforça o controle de evolução do produto.

---

# 📊 Indicadores de qualidade

Quero que tenhamos metas claras.

| Indicador | Meta |
| --- | --- |
| Tempo médio de resposta (consultas comuns) | ≤ 500 ms |
| Operações críticas | ≤ 2 s |
| Cobertura de testes (regras críticas) | ≥ 80% |
| Disponibilidade | ≥ 99% |
| Responsividade | Desktop, Tablet e Mobile |
| Autenticação | JWT |
| Armazenamento de senha | Hash seguro |
| Exclusão lógica | Sim |
| Arquitetura | Monólito Modular |
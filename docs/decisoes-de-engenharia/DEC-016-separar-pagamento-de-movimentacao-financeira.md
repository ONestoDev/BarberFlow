## DEC-016 — Separar pagamento de movimentação financeira

Poderíamos registrar tudo apenas em `payments`.

Mas vamos separar:

```
payments
```

para o pagamento do atendimento.

E:

```
financial_transactions
```

para o fluxo financeiro geral.

### Por quê?

Porque futuramente o financeiro precisará registrar também:

- aluguel;
- energia;
- compra de produtos;
- manutenção;
- comissões;
- entradas avulsas.

Assim, o pagamento gera uma entrada financeira, mas o financeiro não depende apenas de pagamentos.

Boa arquitetura é isso: simples agora, mas sem bloquear crescimento futuro.
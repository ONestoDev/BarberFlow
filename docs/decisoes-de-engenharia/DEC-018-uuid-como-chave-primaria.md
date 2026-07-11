## DEC-018 — Uso de UUID como chave primária

Usaremos `UUID` em vez de `SERIAL`.

### Motivos

- Evita exposição de sequência incremental.
- Facilita futuras integrações.
- Ajuda quando o sistema evoluir para multiempresa.
- É comum em APIs modernas.

Para um sistema simples, `SERIAL` também funcionaria. Mas como o BarberFlow tem roadmap de SaaS, `UUID` é uma escolha mais preparada.

---

# Observação importante

Neste modelo ainda não criamos a regra de conflito de agendamento diretamente no banco.

Por quê?

Porque essa regra envolve:

```
barbeiro
data
intervalo de horário
status do atendimento
```

Essa validação será feita principalmente no **Service** do backend.

Mais tarde, poderemos reforçar com constraints avançadas do PostgreSQL, mas para a V1 manteremos a regra no domínio da aplicação.
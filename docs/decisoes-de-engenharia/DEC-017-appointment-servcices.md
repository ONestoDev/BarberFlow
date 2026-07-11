## DEC-017 — `appointment_services` com preço histórico

A tabela `appointment_services` guardará:

```
price_at_time
duration_at_time
```

Mesmo que o serviço mude depois.

### Motivo

Histórico financeiro precisa ser confiável.

Se hoje o corte custa R$ 40 e daqui a seis meses passar para R$ 50, atendimentos antigos não podem mudar de valor.
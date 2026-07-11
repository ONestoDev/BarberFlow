## DEC-004 — Exclusão lógica (Soft Delete)

Nenhum cadastro importante será removido fisicamente na V1.

Em vez disso, utilizaremos um campo como:

```
ativo = true
```

ou

```
deleted_at = null
```

Quando um cliente ou serviço for "excluído", ele apenas deixará de aparecer nas consultas padrão.

### Motivos

- Preserva histórico.
- Evita perda de dados.
- Mantém integridade referencial.
- Facilita recuperação de registros excluídos por engano.

Essa decisão também simplificará relatórios e auditorias.
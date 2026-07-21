# DEC-020 — Cliente e usuário são entidades relacionadas

## Decisão

O cadastro operacional de cliente será independente da conta de acesso.

`customers.user_id` será opcional e poderá vincular um cliente a um registro de
`users` quando o portal do cliente for habilitado.

## Motivos

- Na V1, nome e telefone são obrigatórios para o cliente, mas e-mail é opcional.
- Uma conta de usuário exige e-mail e senha.
- Administradores e barbeiros precisam cadastrar clientes rapidamente no balcão.
- O vínculo opcional permite ativar o acesso do cliente posteriormente sem duplicar
  seu histórico de atendimentos.

## Consequências

- Um cliente não recebe credenciais automaticamente ao ser cadastrado.
- Quando existir portal do cliente, a criação da conta deverá vincular o usuário ao
  cliente existente.
- O telefone continua sendo a identidade operacional única do cliente na V1.

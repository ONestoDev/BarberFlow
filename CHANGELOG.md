# Changelog

Todas as mudanças relevantes do BarberFlow serão registradas neste arquivo.

## [Não publicado]

### Adicionado

- Endpoint `POST /api/v1/auth/login` com autenticação por e-mail e senha.
- Geração e validação de tokens JWT.
- Hash e verificação de senhas com bcrypt.
- Migration inicial da tabela `users`.
- Testes unitários de autenticação e teste do endpoint de login.
- Validação de tokens nas rotas protegidas.
- Controle de acesso por perfil para operações administrativas.
- Endpoints de cadastro, listagem e consulta do usuário autenticado.
- Comando interativo para criação do administrador inicial.
- Módulo de clientes com cadastro, pesquisa, consulta, edição e desativação lógica.
- Normalização e unicidade do telefone do cliente.
- Migration da tabela `customers` com vínculo opcional à conta de usuário.
- Decisão de engenharia DEC-020 sobre a separação entre cliente e credenciais.
- Módulo de barbeiros vinculado a usuários com perfil `BARBER`.
- Cadastro de especialidades e jornadas semanais com intervalos.
- Registro de férias, folgas e outras indisponibilidades temporárias.
- Migration das tabelas `barbers`, `barber_specialties`, `barber_schedules` e
  `barber_unavailabilities`.
- Catálogo de serviços com categorias, duração, preço e descrição.
- Pesquisa de serviços por nome ou descrição e filtro por categoria.
- Desativação lógica de serviços que preserva o histórico futuro.
- Migration das tabelas `service_categories` e `services`.
- Início da Sprint 2 com o módulo de agendamentos.
- Agendamentos com múltiplos serviços e snapshots históricos de preço e duração.
- Cálculo automático do término do atendimento.
- Validação de jornada, intervalo, indisponibilidade e conflitos de horário.
- Cancelamento e reagendamento com proteção por estado.
- Configuração `APP_TIMEZONE` para interpretar a jornada local e armazenar datas em UTC.
- Migration das tabelas `appointments` e `appointment_services`.
- Máquina de estados completa do atendimento: agendado, confirmado, em atendimento
  e concluído.
- Consulta de horários disponíveis por data, barbeiro e conjunto de serviços.
- Intervalo dos slots configurável por `APPOINTMENT_SLOT_INTERVAL_MINUTES`.
- Encerramento da Sprint 2; Sprint 3 deixada explicitamente em pausa.
- Retomada e início da Sprint 3 com o módulo de pagamentos.
- Pagamento integral por atendimento via dinheiro, PIX, débito ou crédito.
- Registro separado de valor original, desconto e valor efetivamente pago.
- Criação atômica da entrada em `financial_transactions` a partir do pagamento.
- Migration das tabelas `payments` e `financial_transactions`.
- Lançamentos financeiros manuais de entrada e saída.
- Categoria obrigatória para despesas.
- Correções financeiras imutáveis por contralançamento vinculado.
- Fluxo de caixa com totais de entradas, despesas e lucro por período.
- Migration para categorias e vínculos de correção financeira.
- Encerramento da Sprint 3.
- Dashboard administrativo filtrado por período.
- Indicadores de faturamento, atendimentos concluídos e novos clientes.
- Rankings de serviços vendidos e faturamento por barbeiro.
- Encerramento da Sprint 4 e pausa antes do frontend administrativo da Sprint 5.

### Alterado

- Dependências atualizadas para versões compatíveis com Python 3.14.
- Datas de auditoria configuradas com suporte explícito a fuso horário.
- Pytest configurado na raiz para resolver `src` tanto no terminal quanto no PyCharm.

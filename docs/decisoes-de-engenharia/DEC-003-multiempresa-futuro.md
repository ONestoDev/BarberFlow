## DEC-003

### O sistema será pensado para múltiplas barbearias (multiempresa), mas a implementação dessa funcionalidade ficará para uma versão futura.

Na V1, cada instalação atenderá apenas uma empresa.

### Por quê?

Porque adicionar multiempresa desde o início aumentaria significativamente a complexidade:

- isolamento de dados;
- autenticação;
- permissões;
- cobrança por assinatura.

Não precisamos disso para validar o produto.
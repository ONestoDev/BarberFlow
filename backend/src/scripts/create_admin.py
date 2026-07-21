import argparse
import getpass

from pydantic import ValidationError

from src.modules.users.repository import UserRepository
from src.modules.users.schemas import UserCreate
from src.modules.users.service import EmailAlreadyInUseError, UserService
from src.shared.database.connection import SessionLocal
from src.shared.database.enums import UserRole


def main() -> None:
    parser = argparse.ArgumentParser(description="Cria o administrador inicial.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    password = getpass.getpass("Senha: ")
    confirmation = getpass.getpass("Confirme a senha: ")
    if password != confirmation:
        raise SystemExit("As senhas não coincidem.")

    with SessionLocal() as db:
        repository = UserRepository(db)
        if repository.has_admin():
            raise SystemExit("Já existe um administrador cadastrado.")
        try:
            data = UserCreate(
                name=args.name,
                email=args.email,
                password=password,
                role=UserRole.ADMIN,
            )
            user = UserService(repository).create(data)
        except ValidationError as exc:
            raise SystemExit(str(exc)) from exc
        except EmailAlreadyInUseError as exc:
            raise SystemExit("Já existe um usuário com este e-mail.") from exc

    print(f"Administrador criado: {user.email}")


if __name__ == "__main__":
    main()

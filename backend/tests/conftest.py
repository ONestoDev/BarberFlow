import os


os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/barberflow_test",
)
os.environ.setdefault("JWT_SECRET", "test-secret-do-not-use-in-production")

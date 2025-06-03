DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_NAME = "MyProject"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
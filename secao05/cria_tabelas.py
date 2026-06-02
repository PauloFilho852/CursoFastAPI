from core.database import engine
import models  # noqa: F401
from models.base_class import Base


async def create_tables():
    print("Criando as tabelas no banco de dados...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
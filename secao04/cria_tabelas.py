#from core.settings import settings
from core.database import engine
from models.curso_model import CursoModel

async def create_tables():
    print('Criando as tabelas no banco de dados...')
    async with engine.begin() as conn:
        await conn.run_sync(CursoModel.metadata.drop_all)
        await conn.run_sync(CursoModel.metadata.create_all)
    print('Tabelas criadas com sucesso!')

if __name__ == '__main__':    
    import asyncio
    asyncio.run(create_tables())
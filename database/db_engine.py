from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .db_config import DBConfig

engine = create_async_engine(
    url=DBConfig().db_url,
    echo=False,
)

async_session = async_sessionmaker(engine)

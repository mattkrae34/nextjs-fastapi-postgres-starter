from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


from db.models.models import Base

_main_uri = "postgres:postgres@database:5432/postgres"
_sync_uri = f"postgresql://{_main_uri}"
_async_uri = f"postgresql+asyncpg://{_main_uri}"

sync_engine = create_engine(_sync_uri)

Base.metadata.create_all(sync_engine)

engine = create_async_engine(_async_uri)

from sqlalchemy import MetaData, UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(
    settings.database_url,
    echo = settings.db_echo,
    connect_args = {"ssl" : True, "statement_cache_size": 0},
    pool_pre_ping = True,
    pool_recycle = 300
    )

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

def all_column_names(constraint,table):
    return "__".join(col.name for col in constraint.columns)

NAMING_CONVENTION = {
    "all_column_names": all_column_names,
    "ix": "ix__%(table_name)s__%(all_column_names)s",             # index
    "uq": "uq__%(table_name)s__%(all_column_names)s",             # unique constraint
    "ck": "ck__%(table_name)s__%(constraint_name)s",           # check constraint
    "fk": "fk__%(table_name)s__%(column_0_name)s__%(referred_table_name)s",  # foreign key
    "pk": "pk__%(table_name)s",                               # primary key
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention= NAMING_CONVENTION)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

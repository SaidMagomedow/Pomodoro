from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


from settings import Settings

settings = Settings()

engine = create_async_engine(settings.db_url, future=True, echo=True, pool_pre_ping=True)


AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import Config


class Base(DeclarativeBase):
    pass


engine = create_engine(Config.DATABASE_URL)

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def init_db():
    from app.db.models import currency, exchange_rate

    Base.metadata.create_all(engine)

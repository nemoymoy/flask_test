import atexit
import os
import datetime
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedColumn, mapped_column

POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'netology')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    login: MappedColumn[str] = mapped_column(String(50), unique=True)
    password: MappedColumn[str] = mapped_column(String(60))
    registration_time: MappedColumn[datetime.datetime] = mapped_column(DateTime, default=func.now())

    @property
    def id_json(self):
        return {'id': self.id}

    @property
    def json(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password,
            'registration_time': self.registration_time.isoformat()
        }
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

atexit.register(engine.dispose)
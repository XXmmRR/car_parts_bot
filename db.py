"""Тут будет вся логика связанная с бд"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from databases.basecars_orm import BaseCars

DATABASE_NAME = 'bot.sqlite'

engine = create_engine(f"sqlite:///{DATABASE_NAME}")
Session = sessionmaker(bind=engine)

Base = declarative_base()


class CreateBaseCars(Base, BaseCars):
    pass


def create_db():
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()


if __name__ == '__main__':
    create_db()
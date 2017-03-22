import os


from sqlalchemy import (Boolean, Column, create_engine, Integer, String,
                        ForeignKey, Table, MetaData)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('room_id', Integer, ForeignKey('room.id')),
                          Column('people_id', Integer, ForeignKey('people.id'))
                          )


class Room(Base):
    '''create table room'''
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), nullable=False)
    type = Column(String(10), nullable=False)
    max_space = Column(Integer, nullable=False)
    occupants = relationship('Person',
                             secondary=association_table,
                             backref='room',
                             order_by=id)


class Person(Base):
    '''create table people'''
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    role = Column(String(10), nullable=False)
    wants_livingspace = Column(Boolean, nullable=False)


class CreateDb:
    ''' create database for the project'''

    def __init__(self, database=None):
        if database:
            if '.sqlite' not in database:
                self.database += '.sqlite'
        else:
            self.database = 'amity.sqlite'
        self.engine = create_engine('sqlite:///' + self.database)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def clear(self):
        os.remove(self.database)

'''This is the database module that holds all the database logic for amity'''

from sqlalchemy import (Boolean, Column, create_engine, Integer, String,
                        ForeignKey, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

BASE = declarative_base()

association = Table('association', BASE.metadata,
                    Column('room_id', Integer, ForeignKey('room.id')),
                    Column('people_id', Integer, ForeignKey('people.id')))


class Room(BASE):
    '''create table room'''
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), nullable=False)
    type = Column(String(10), nullable=False)
    max_space = Column(Integer, nullable=False)
    occupants = relationship('Person',
                             secondary=association,
                             backref='room',
                             order_by=id)


class Person(BASE):
    '''create table people'''
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    role = Column(String(10), nullable=False)
    wants_livingspace = Column(Boolean, nullable=False)


class Database:
    ''' create database for the project'''

    def __init__(self, database=None):
        if database:
            self.database = ''
            if '.sqlite' not in database:
                self.database += '.sqlite'
        else:
            self.database = 'amity.sqlite'
        self.engine = create_engine('sqlite:///' + self.database)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        BASE.metadata.create_all(self.engine)

    def initialize(self, database=None):
        '''Reinitialize the database with a session'''
        self.__init__(database)

    def clear(self):
        '''Clear database tables so as to save amity's state afresh'''
        connection = self.engine.connect()
        transaction = connection.begin()
        for table in reversed(BASE.metadata.sorted_tables):
            connection.execute(table.delete())
        transaction.commit()

    def save(self):
        '''Save amity's state to database'''
        self.session.commit()
        self.session.close()

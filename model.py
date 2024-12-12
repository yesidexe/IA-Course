from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class TodoList(Base):
    __tablename__ = 'todolist'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    task = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
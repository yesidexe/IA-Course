from sqlalchemy import Boolean, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TodoList(Base):    
    __tablename__ = 'todolist'
    
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    task = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
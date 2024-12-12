import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_url='sqlite:///tareas.db'):
        try:
            self.engine = create_engine(db_url, echo=False)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            logger.error(f"Error al inicializar base de datos: {e}")
            raise

    def get_session(self):
        return self.Session()
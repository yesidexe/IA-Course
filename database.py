import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from model import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_url='postgresql://postgres:postgres@localhost:5432/todolist'):
        try:            
            self.engine = create_engine(db_url, echo=False)
            
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
                logger.info("Base de datos creada exitosamente")  
                        
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            logger.error(f"Error al inicializar base de datos: {e}")
            raise

    def get_session(self):
        return self.Session()
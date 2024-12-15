import logging

from model import TodoList
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class TodoListCrud:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_task(self, title, task):
        session = self.db_manager.get_session()
        try:
            new_task = TodoList(title=title, task=task, completed=False)
            session.add(new_task)
            session.commit()
            logger.info(f"Tarea creada con ID: {new_task.id}")
            return new_task.id
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error al crear tarea: {e}")
            return None
        finally:
            session.close()

    def get_tasks(self):
        session = self.db_manager.get_session()        
        try:
            tasks = session.query(TodoList).all()
            return tasks
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener tareas: {e}")
            return []
        finally:
            session.close()

    def update_task(self, task_id, title=None, task=None, completed=None):
        session = self.db_manager.get_session()
        try:
            update_task = session.query(TodoList).filter_by(id=task_id).first()
            if update_task:
                if title is not None:
                    update_task.title = title
                if task is not None:
                    update_task.task = task
                if completed is not None:
                    update_task.completed = completed
                session.commit()
                logger.info(f"Tarea {task_id} actualizada")
                return True
            logger.warning(f"Tarea {task_id} no encontrada para actualizar")
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error al actualizar tarea: {e}")
            return False
        finally:
            session.close()
            
    def drop_task(self, task_id):
        session = self.db_manager.get_session()
        try:
            drop_task = session.query(TodoList).filter_by(id=task_id).first()
            if drop_task:
                session.delete(drop_task)
                session.commit()
                logger.info(f"Tarea {task_id} eliminada")
                return True
            logger.warning(f"Tarea {task_id} no encontrada para eliminar")
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error al eliminar tarea: {e}")
            return False
        finally:
            session.close()
    
    def import_tasks(self, json_data):
        session = self.db_manager.get_session()
        try:
            if not all(isinstance(data, dict) and 'title' in data and 'task' in data for data in json_data):
                raise ValueError("Datos de entrada inválidos para importar tareas")
            
            for data in json_data:
                new_task = TodoList(
                    title=data['title'],
                    task=data['task'],
                    completed=data.get('completed', False)
                )
                session.add(new_task)
            session.commit()
            logger.info("Tareas importadas exitosamente")
            return True
        except (SQLAlchemyError, ValueError) as e:
            session.rollback()
            logger.error(f"Error al importar tareas: {e}")
            return False
        finally:
            session.close()

    # En crud.py
    def export_tasks(self):
        session = self.db_manager.get_session()
        try:
            tasks = session.query(TodoList).all()
            tasks_data = [
                {"title": task.title, "task": task.task, "completed": task.completed}
                for task in tasks
            ]
            return tasks_data
        except SQLAlchemyError as e:
            logger.error(f"Error al exportar tareas: {e}")
            return []
        finally:
            session.close()
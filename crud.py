from sqlalchemy.orm.exc import NoResultFound
from model import TodoList

class TodoListCrud:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_task(self, title, task):
        session = self.db_manager.get_session()
        try:
            new_task = TodoList(title=title, task=task, completed=False)
            session.add(new_task)
            session.commit()
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
                return True
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
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error al eliminar tarea: {e}")
            return False
        finally:
            session.close()
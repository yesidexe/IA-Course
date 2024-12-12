import streamlit as st
from database import DatabaseManager
from crud import TodoListCrud

def main():
    st.title("📝 Lista de Tareas")

    try:
        db_manager = DatabaseManager()
        crud = TodoListCrud(db_manager)
    except Exception as e:
        st.error(f"No se pudo inicializar la base de datos: {e}")
        return

    st.header("Agregar Nueva Tarea")
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Título de la tarea")
    with col2:
        task_description = st.text_input("Descripción de la tarea")
    if st.button("Crear Tarea"):
        if task_title and task_description:
            crud.add_task(task_title, task_description)
            st.success("Tarea creada exitosamente")
        else:
            st.warning("No pueden haber campos vacios")

    st.header("Mis Tareas")
    tasks = crud.get_tasks()

    if not tasks:
        st.info("No hay tareas pendientes")
    else:
        df_tasks = st.data_editor(
            data=[
                {
                    "id": task.id, 
                    "title": task.title,
                    "task": task.task,
                    "completed": task.completed
                } for task in tasks
            ],
            column_config={
                "id": st.column_config.NumberColumn(disabled=True),
                "completada": st.column_config.CheckboxColumn("Completada")
            },
            hide_index=True
        )

        for or_task, new_task in zip(tasks, df_tasks):
            if new_task['title'] != or_task.title or new_task['task'] != or_task.task or new_task['completed'] != or_task.completed:
                crud.update_task(
                    or_task.id, 
                    title=new_task['title'], 
                    task=new_task['task'],
                    completed=new_task['completed']
                )

    st.header("Eliminar Tarea")
    drop_id_task = st.number_input("ID de tarea a eliminar", min_value=1)
    if st.button("Eliminar Tarea"):
        if crud.drop_task(drop_id_task):
            st.success(f"tarea {drop_id_task} eliminada")
        else:
            st.warning("No se encontró la tarea")

if __name__ == "__main__":
    main()


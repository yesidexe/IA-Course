import json
import streamlit as st
from database import DatabaseManager
from crud import TodoListCrud

def main():
    st.set_page_config(layout="wide")
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
            st.experimental_rerun()
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
                    "completed": task.completed,
                    "actions": task.id
                } for task in tasks
            ],
            column_config={
                "id": st.column_config.NumberColumn(disabled=True),
                "completed": st.column_config.CheckboxColumn("completed"),
                "actions": st.column_config.ButtonColumn(
                    "Eliminar", 
                    help="Eliminar esta tarea",
                    width="small")
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
                
            if new_task['actions'] == or_task.id and st.button(f"Eliminar {or_task.id}", key=f"delete_{or_task.id}"):
                crud.drop_task(or_task.id)
                st.experimental_rerun()

    st.header("Importar/Exportar Tareas")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Exportar Tareas a JSON"):
            tasks = crud.get_tasks()
            data_to_export = [
                {
                    "id": task.id, 
                    "title": task.title, 
                    "task": task.task,
                    "completed": task.completed
                } for task in tasks
            ]
            
            with open("todolist.json", "w") as f:
                json.dump(data_to_export, f, indent=4)
            
            st.success("Tareas exportadas a todolist.json")

    with col2:
        # Importar tareas
        json_file = st.file_uploader("Importar Tareas desde JSON", type=['json'])
        
        if json_file is not None:
            try:
                # Leer archivo JSON
                data_to_import = json.load(json_file)
                
                # Importar tareas
                if crud.import_tasks(data_to_import):
                    st.success("Tareas importadas exitosamente")
                    st.experimental_rerun()
                else:
                    st.error("Error al importar tareas")
            except Exception as e:
                st.error(f"Error al procesar el archivo JSON: {e}")

if __name__ == "__main__":
    main()


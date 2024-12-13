import json
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

    # AGREGAR TAREA
    st.header("Agregar Nueva Tarea")
    col1, col2 = st.columns([1, 3,])
    with col1:
        task_title = st.text_input("Título de la tarea")
    with col2:
        task_description = st.text_input("Descripción de la tarea")
        
    st.write("")
    if st.button("Agregar tareas"):
        if task_title and task_description:
            crud.add_task(task_title, task_description)
            st.rerun()
        else:
            st.warning("No pueden haber campos vacios")

    # MIS TAREAS
    col1, col2 = st.columns([2, 1])
    with col1:    
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
                    } for task in tasks
                ],
                column_config={
                    "id": st.column_config.NumberColumn(disabled=True),
                    "completed": st.column_config.CheckboxColumn("completed"),
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

    with col2:
        col1, col2 = st.columns(2)

        
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
            
            json_data = json.dumps(data_to_export, indent=4)
            
            st.download_button(
                label="Descargar Tareas en JSON",
                data=json_data,
                file_name="todolist.json",
                mime="application/json"
            )
            
            st.success("Tareas exportadas a todolist.json")

        json_file = st.file_uploader("Importar Tareas desde JSON", type=['json'])
        
        if json_file is not None:
            try:
                # Leer archivo JSON
                data_to_import = json.load(json_file)
                
                # Importar tareas
                if crud.import_tasks(data_to_import):
                    st.success("Tareas importadas exitosamente")
                    st.rerun()
                else:
                    st.error("Error al importar tareas")
            except Exception as e:
                st.error(f"Error al procesar el archivo JSON: {e}")

if __name__ == "__main__":
    main()


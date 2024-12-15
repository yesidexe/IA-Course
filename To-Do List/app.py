import json
import streamlit as st
from database import DatabaseManager
from crud import TodoListCrud

def main():
    if 'imported_files' not in st.session_state:
        st.session_state.imported_files = set()
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
        
    if st.button("Agregar tareas"):
        if task_title and task_description:
            task_id = crud.add_task(task_title, task_description)
            if task_id:
                st.rerun()
            else:
                st.error("Error al agregar la tarea")
        else:
            st.warning("No pueden haber campos vacios")

    # MIS TAREAS
        
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
                "eliminar": False
            } for task in tasks
        ],
            column_config={
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "completed": st.column_config.CheckboxColumn("Completado"),
                "eliminar": st.column_config.CheckboxColumn("Eliminar")
            },
            hide_index=True
        )

        for original, updated in zip(tasks, df_tasks):
            if updated.get('eliminar', False):
                success = crud.drop_task(original.id)
                if success:
                    st.rerun()
                else:
                    st.error(f"Error al eliminar la tarea {original.id}")
                    
            elif (
                updated['title'] != original.title or 
                updated['task'] != original.task or 
                updated['completed'] != original.completed):
                success = crud.update_task(
                    original.id, 
                    title=updated['title'], 
                    task=updated['task'],
                    completed=updated['completed']
                )
                if success:
                    st.toast(f"Tarea {original.id} actualizada", icon="✅")
                else:
                    st.error(f"Error al actualizar la tarea {original.id}")
    
    # Exportar tareas
    if st.button("Exportar Tareas en JSON"):
        data_to_export = crud.export_tasks()
        if data_to_export:
            json_data = json.dumps(data_to_export, indent=4, ensure_ascii=False)
            st.download_button(
                label="Descargar Tareas en JSON",
                data=json_data,
                file_name="todolist.json",
                mime="application/json"
            )
        else:
            st.error("No se pudieron exportar las tareas")
                
    # Importar tareas
    json_file = st.file_uploader("Importar Tareas desde JSON", type=['json'])
    
    if json_file is not None:
        # Verificar si ya se importó este archivo
        if json_file.name not in st.session_state.imported_files:
            try:
                # Leer archivo JSON
                data_to_import = json.load(json_file)
                
                # Importar tareas
                if crud.import_tasks(data_to_import):
                    st.toast("Tareas importadas exitosamente", icon="✅")
                    # Registrar el archivo como importado
                    st.session_state.imported_files.add(json_file.name)
                    st.rerun()
                else:
                    st.error("Error al importar tareas")
            except Exception as e:
                st.error(f"Error al procesar el archivo JSON: {e}")
if __name__ == "__main__":
    main()


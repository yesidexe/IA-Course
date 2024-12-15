# To-Do List
Es una "aplicación" que permite gestionar tareas. Consiste en Agregar tareas, poder editarlas como marcalas como completadas, también permite eliminarlas. Al finalizar tienes la opción de poner importar otras tareas que tengas en formato JSON, al igual como exportar las tareas actuales en formato JSON tmaibén

## **Contenido**
- `app.py` interfaz desarrollada con Streamlit para gestionar tareas, permitiendo agregar, ver, editar, eliminar, exportar e importar tareas en formato JSON..
- `crud.py` gestiona tareas con operaciones CRUD (crear, leer, actualizar, eliminar) utilizando SQLAlchemy. Permite importar y exportar tareas en formato JSON.
- `database.py` gestiona la conexión y creación de la base de datos usando SQLAlchemy. Se asegura de que la base de datos exista y maneja sesiones para interactuar con ella.
- `model.py` define el modelo de datos para la tabla todolist en la base de datos, con campos para ID, título, tarea y estado de completado. Utiliza SQLAlchemy para la definición y mapeo de la base de datos.

## **Ambiente de desarrollo**
- [Python](https://www.python.org/)
- [VisualStudioCode](https://code.visualstudio.com/)
- [Streamlit](https://streamlit.io/)
- [Sqlite](https://www.sqlite.org/)

## **Librerias usadas**
> 📢 Principalmente pondré estas tres librerias, en el archivo `requirements.txt` aparecen más debido a estas librerias descargan otras para funcionar.
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Streamlit](https://streamlit.io/)
- [SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/en/latest/)

## **Funcionamiento**
1. Luego de haber descargado todo das click derecho en la carpeta y abres desde ahí el terminal, si no aparece esta función simplemente copias la ruta y la pegas en el powershell con `cd '<ruta>'`.
2. Tomando en cuenta de que ya tienes python creas un entorno virtual `python -m venv <nombre del entorno>`, al finalizar lo activas `<nombre del entorno>\Scripts\activate`.
3. Instalas por separado las librerias usadas, o ejecutas el requirements de la siguiente manera `pip install -r requirements.txt`.
4. Corres el streamlit con el comando `streamlit run app.py`, cuando abra es bastante intuitiva la interfaz, agregas la tarea con el título y descripción, puedes marcar el checkbox para completar la tarea, también puedes marcar el checkbox para eliminarla, abajo puedes exportar e importar las tareas como quieras.




  

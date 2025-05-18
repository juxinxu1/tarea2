# Tarea 2 - CC5002: Actividades Recreativas

Este proyecto implementa una aplicación web en Flask para registrar y visualizar actividades recreativas, con validaciones, carga de archivos e integración con una base de datos MySQL de la extensión de VS code.

## 📝 Consideraciones importantes para la corrección

- **Basado en el Auxiliar 4:** El diseño general de la aplicación está basado en el Auxiliar 4 del curso. Usé este auxiliar como referencia para estructurar las rutas, conexión a base de datos y validaciones.

- **Ambiente virtual requerido:** Para que la aplicación funcione correctamente, debe activarse el ambiente virtual llamado `tarea2` (creado con `python -m venv tarea2`) y luego ejecutarse el servidor con el comando:
  
  ```bash
  flask run
Inserción múltiple consistente: En la función create_activity de db.py, me aseguré de que todas las inserciones a las tablas actividad, contactar_por, actividad_tema y foto se realicen dentro de una misma conexión y en el orden correcto, para mantener la consistencia referencial. Si alguna falla, no se insertan las demás.

Carga dinámica de comunas: Para mejorar la experiencia de usuario, implementé un sistema de carga dinámica de comunas al seleccionar la región usando JavaScript y una ruta API en Flask. Esto evita cargar todas las comunas desde el inicio, lo que mejora el rendimiento.

Validación doble (frontend y backend): Aunque el formulario tiene validaciones en JavaScript, también se valida todo en el backend (utils/validations.py) para garantizar la integridad, incluso si alguien manipula el formulario desde el navegador.

Subida y verificación de imágenes: Solo se permite subir entre 1 y 5 archivos de tipo JPG o PNG. El backend usa filetype y hashlib para validar que los archivos realmente sean imágenes válidas y no solo tengan una extensión permitida.

Paginación manual en el listado: La lista de actividades implementa paginación de 5 en 5 actividades manualmente, pasando el parámetro pagina por la URL y calculando los límites en el backend. Esto permite escalar fácilmente en el futuro.

Diseño modular del código: Separé las funciones de validación, acceso a base de datos y lógica de Flask para facilitar el mantenimiento y posibles mejoras posteriores.

Cambio de entorno y repositorio: Para esta tarea tuve que crear un nuevo repositorio, ya que en la Tarea 1 trabajé usando IntelliJ IDEA, pero ahora no me permite acceder correctamente al repositorio anterior. Por ello, realicé la Tarea 2 desde cero utilizando Visual Studio Code como entorno de desarrollo.
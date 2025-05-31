# PySQL Console

---

## 📄 Descripción del Proyecto

**PySQL Console** es una herramienta de gestión de bases de datos SQLite diseñada para ser utilizada directamente desde la línea de comandos. Desarrollada en Python y aprovechando la librería `rich` para una experiencia de usuario mejorada, esta aplicación te permite interactuar con tus bases de datos SQLite de una manera visualmente atractiva y funcional.

Con PySQL Console, puedes realizar operaciones esenciales como **crear nuevas tablas, visualizar el contenido de tus tablas existentes, insertar nuevos registros, buscar información específica, actualizar datos y eliminar filas o tablas completas**. Es una solución ideal para quienes buscan una forma sencilla y eficiente de administrar sus bases de datos SQLite sin la complejidad de una interfaz gráfica de usuario.

---

## ✨ Características Principales

* **Gestión Completa de Tablas:**
    * **Creación:** Define y genera nuevas tablas con columnas personalizadas, tipos de datos (`TEXT`, `INTEGER`, `REAL`, `BLOB`, `TEXT UNIQUE`) y la opción de establecer restricciones `NOT NULL`.
    * **Visualización:** Lista todas las tablas presentes en la base de datos y muestra el contenido detallado de cualquier tabla seleccionada en un formato tabular claro.
    * **Eliminación:** Borra tablas completas de forma segura con una confirmación previa.
* **Operaciones CRUD sobre Registros:**
    * **Crear (C - Insertar):** Añade nuevos datos a tus tablas de forma interactiva.
    * **Leer (R - Mostrar/Buscar):** Visualiza todos los registros de una tabla o realiza búsquedas basadas en el contenido de cualquier columna.
    * **Actualizar (U - Modificar):** Edita registros existentes especificando su `ID` y proporcionando los nuevos valores para las columnas.
    * **Eliminar (D - Borrar):** Suprime filas individuales de una tabla basándose en el valor de una columna.
* **Interfaz de Usuario Mejorada:** Gracias a la librería `rich`, la consola presenta menús interactivos, tablas formateadas y mensajes de estado claros y coloridos, mejorando significativamente la experiencia del usuario.
* **Manejo de Errores:** Incluye un manejo básico de excepciones para operaciones de base de datos, informando al usuario sobre posibles problemas.
* **Conexión Segura a la DB:** Utiliza un administrador de contexto (`@contextmanager`) para garantizar que las conexiones a la base de datos se abran y cierren de manera adecuada, previniendo fugas de recursos.

---

## 🚀 Cómo Empezar

Sigue estos pasos para poner en marcha PySQL Console en tu sistema.

### Prerrequisitos

* **Python 3.x:** Asegúrate de tener una versión compatible de Python instalada. Puedes verificarlo con:
    ```bash
    python --version
    ```

### Instalación

1.  **Clona el repositorio** (o descarga los archivos del proyecto):

    ```bash
    git clone [https://github.com/tu-usuario/PySQL-Console.git](https://github.com/tu-usuario/PySQL-Console.git)
    cd PySQL-Console
    ```

2.  **Instala las dependencias de Python** utilizando `pip`:

    ```bash
    pip install rich
    ```

### Uso

Para iniciar la aplicación, navega al directorio del proyecto en tu terminal y ejecuta el script principal:

```bash
python python main.py
```

## ⚠️ Consideraciones de Seguridad (Importante)
Es fundamental destacar que, en su implementación actual, las funciones como get_columnas y eliminar_tabla construyen dinámicamente las consultas SQL insertando directamente el nombre de la tabla. Esta práctica, si bien funcional para nombres de tablas controlados, puede ser vulnerable a ataques de inyección SQL si el nombre de la tabla proviene de una entrada no validada por el usuario en un entorno de producción.

Recomendación: Para garantizar la máxima seguridad, especialmente en aplicaciones que manejen datos sensibles o provengan de fuentes externas, se recomienda encarecidamente implementar una validación estricta (por ejemplo, una lista blanca de nombres de tablas permitidos) antes de ejecutar cualquier consulta SQL que incluya identificadores de tabla construidos dinámicamente.

## 🤝 Contribuciones
¡Tu ayuda es bienvenida! Si deseas contribuir a PySQL Console, ya sea mejorando el código, añadiendo nuevas funcionalidades o reportando errores, por favor:

Haz un fork de este repositorio.
Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
Realiza tus cambios y haz commit (git commit -m 'Añadir nueva funcionalidad X').
Sube tus cambios a tu fork (git push origin feature/nueva-funcionalidad).
Abre un Pull Request a este repositorio.
## 📄 Licencia
Este proyecto está distribuido bajo la Licencia MIT. Consulta el archivo LICENSE (si lo tienes) para más detalles.

## 📧 Contacto
Para cualquier pregunta, sugerencia o comentario, no dudes en contactarme a través de dcazorla.0190@gmail.com.

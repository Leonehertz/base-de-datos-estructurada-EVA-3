# 🍔 Aplicación CRUD de Gestión de Alimentos con MongoDB y Python

Este repositorio contiene una aplicación de consola desarrollada en Python que interactúa con una base de datos no estructurada de MongoDB para gestionar información sobre alimentos y sus propiedades nutricionales. El proyecto demuestra la implementación de operaciones CRUD (Crear, Leer, Actualizar, Eliminar) utilizando PyMongo, el controlador oficial de MongoDB para Python.

---

## 📋 Características Principales

* **Modelo de Datos Flexible:** Diseño de documentos de alimentos que incorpora subdocumentos y arrays para representar información compleja como porciones, macronutrientes, micronutrientes y alérgenos.
* **Operaciones CRUD Completas:**
    * **Creación (Create):** Inserción de nuevos registros de alimentos.
    * **Lectura (Read):** Consultas variadas con filtros por nombre, rango de calorías, categoría, micronutrientes y alérgenos, incluyendo proyecciones de campos y uso de operadores lógicos y de comparación.
    * **Actualización (Update):** Modificación de campos directos, campos anidados en subdocumentos y elementos específicos dentro de arrays.
    * **Eliminación (Delete):** Borrado de registros individuales o múltiples por criterios, y eliminación de elementos específicos de arrays.
* **Conexión Flexible:** Configurable para conectar tanto a instancias de MongoDB local como a clusters en la nube (MongoDB Atlas).
* **Menú Interactivo:** Permite al usuario realizar operaciones CRUD de forma manual y experimentar con la base de datos.
* **Demostración Automática:** Incluye un bloque de código que ejecuta una secuencia predefinida de operaciones CRUD para facilitar la evaluación del proyecto.

---

## 🛠️ Tecnologías Utilizadas

* **MongoDB:** Base de datos NoSQL orientada a documentos.
* **Python 3.x:** Lenguaje de programación.
* **PyMongo:** Controlador oficial de MongoDB para Python.
* **Visual Studio Code (VS Code):** Editor de código.
* **MongoDB Compass / Studio 3T:** Herramientas GUI para gestión y visualización de la base de datos.

---

## 🚀 Configuración y Ejecución del Proyecto

Sigue estos pasos para poner en marcha la aplicación:

### 1. Requisitos Previos

Asegúrate de tener instalados los siguientes componentes en tu sistema:

* **Python 3.x:**
    * Descárgalo de [python.org](https://www.python.org/downloads/).
    * **Importante:** Durante la instalación, marca la casilla "Add Python X.X to PATH".
* **MongoDB Community Server:**
    * Descárgalo de [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community).
    * Asegúrate de que el servicio de MongoDB esté en ejecución (puedes verificarlo en los servicios de tu sistema operativo).
* **Visual Studio Code (VS Code):**
    * Descárgalo de [code.visualstudio.com](https://code.visualstudio.com/).
    * Instala la **extensión de Python de Microsoft** desde el Marketplace de VS Code.
* **MongoDB Compass o Studio 3T:**
    * Descárgalos de [mongodb.com/products/compass](https://www.mongodb.com/products/compass) o [studio3t.com/download](https://studio3t.com/download/).

### 2. Clonar el Repositorio

Abre tu terminal o Git Bash y clona este repositorio:

```bash
git clone [https://github.com/TuUsuario/NombreDeTuRepositorio.git](https://github.com/TuUsuario/NombreDeTuRepositorio.git)
cd NombreDeTuRepositorio # Navega a la carpeta del proyecto

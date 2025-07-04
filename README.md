# Cuentas Claras - Aplicación de Seguimiento de Gastos

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2+-green?style=for-the-badge&logo=django&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-blueviolet?style=for-the-badge&logo=tailwind-css&logoColor=white)

**Cuentas Claras** es una aplicación web desarrollada con Python y Django, diseñada para ofrecer a los usuarios una herramienta intuitiva y potente para el seguimiento de sus finanzas personales. Permite registrar ingresos y gastos, categorizarlos y visualizar resúmenes mensuales a través de un dashboard interactivo.

Este proyecto fue construido como una pieza central de mi portafolio para demostrar mis habilidades en desarrollo backend y frontend, siguiendo las mejores prácticas de la industria.

---

### Tabla de Contenidos
1. [Capturas de Pantalla](#capturas-de-pantalla)
2. [Características Principales](#características-principales)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Instalación y Uso Local](#instalación-y-uso-local)
5. [Licencia](#licencia)

---

### Capturas de Pantalla

A continuación, se muestran algunas de las vistas principales de la aplicación.

**1. Dashboard Principal:**

![Dashboard Principal](screenshots/dashboard_main.png)

**2. Gestión de Categorías:**

![Gestión de Categorías](screenshots/categories_management.png)

---

### Características Principales

* **Autenticación de Usuarios:** Sistema completo de registro e inicio de sesión para que cada usuario gestione sus finanzas de forma privada y segura.
* **CRUD Completo para Transacciones:** Los usuarios pueden **C**rear, **L**eer, **A**ctualizar y **E**liminar (CRUD) sus transacciones de ingresos y gastos.
* **CRUD Completo para Categorías:** Cada usuario puede gestionar sus propias categorías personalizadas para organizar sus movimientos.
* **Dashboard Interactivo:**
    * Tarjetas de resumen con totales de ingresos, gastos y balance del período seleccionado.
    * Filtro por mes y año para analizar el historial financiero.
    * Gráfico de dona (doughnut chart) que muestra la distribución de gastos por categoría.
* **Interfaz Responsiva:** Diseño moderno y limpio desarrollado con Tailwind CSS, adaptable a dispositivos móviles y de escritorio.
* **Feedback al Usuario:** Mensajes de notificación para confirmar acciones exitosas (crear, editar, eliminar) o informar de errores.

---

### Tecnologías Utilizadas

* **Backend:**
    * Python 3.11
    * Django 5.2
    * SQLite3 (para desarrollo)
* **Frontend:**
    * HTML5
    * Tailwind CSS
    * Chart.js (para los gráficos)
* **Herramientas de Desarrollo:**
    * Git y GitHub
    * Entornos virtuales (`venv`)

---

### Instalación y Uso Local

Para ejecutar este proyecto en tu máquina local, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/SamEP11/seguimiento-gastos.git](https://github.com/SamEP11/seguimiento-gastos.git)
    cd seguimiento-gastos
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\activate

    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    *Asegúrate de tener un archivo `requirements.txt`. Puedes crearlo con `pip freeze > requirements.txt`.*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplica las migraciones:**
    ```bash
    python manage.py migrate
    ```

5.  **Crea un superusuario (opcional, para el panel de admin):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Ejecuta el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

¡Abre tu navegador y ve a `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento!

---

### Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

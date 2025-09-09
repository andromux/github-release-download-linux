# GitHub Release Download Linux


> [!NOTE]
> **⭐ ¿Te gusta este proyecto?**  
> Si encuentras útil esta herramienta, puedes apoyar para que más gente la descubra dejando tu estrella ⭐ o contribuyendo para añadir mejoras, novedades o resolver bugs. ¡Toda ayuda es bienvenida!
> 

___________________________

- [Leer Manual para contribuir](./CONTRIBUTING.md)
- [Descargar Programa (Linux)](https://github.com/andromux/releases_download_eden/releases/tag/1.0.0)
____________________________

## Para que Usuario esta enfocado el proyecto

El **GitHub Releases Downloader** es una aplicación de escritorio moderna que simplifica la descarga de archivos desde los releases de repositorios de GitHub [1](#0-0) . La aplicación proporciona una interfaz gráfica intuitiva construida con Flet que elimina la necesidad de navegar manualmente por GitHub o usar comandos de terminal complejos [2](#0-1) .

## Beneficios Principales

### **Interfaz Gráfica Amigable**
La aplicación presenta una interfaz limpia y organizada que permite configurar fácilmente el repositorio, token de autenticación y carpeta de descarga [3](#0-2) . Los usuarios pueden alternar entre temas claro y oscuro según sus preferencias [4](#0-3) .

### **Gestión Eficiente de Releases**
El programa carga automáticamente todos los releases disponibles del repositorio configurado, mostrando información detallada como fecha de publicación, número de archivos y tamaño total [5](#0-4) . Esta vista organizada permite identificar rápidamente el release deseado.

### **Opciones de Descarga Flexibles**
Los usuarios pueden descargar archivos de tres maneras diferentes:
- **Descarga individual**: Un archivo específico con seguimiento de progreso en tiempo real [6](#0-5) 
- **Descarga selectiva**: Múltiples archivos seleccionados mediante checkboxes <cite />
- **Descarga completa**: Todos los archivos del release seleccionado <cite />


### **Autenticación Segura**
El programa maneja tokens de GitHub de forma segura, guardándolos localmente para uso futuro y permitiendo acceso a repositorios privados cuando sea necesario [7](#0-7) .

## Casos de Uso Ideales

- **Desarrolladores** que necesitan descargar releases específicos de proyectos
- **Usuarios finales** que buscan versiones estables de software alojado en GitHub
- **Administradores de sistemas** que requieren automatizar descargas de herramientas
- **Equipos de QA** que necesitan acceder a diferentes versiones para pruebas

## Arquitectura Robusta

La aplicación está diseñada con una arquitectura modular que separa claramente la interfaz de usuario de la lógica de negocio [8](#0-8) . Esto garantiza estabilidad, facilita el mantenimiento y permite futuras expansiones de funcionalidad.
___________________________

### Funcionamiento del Programa: El Flujo de la Aplicación

<p align="center">
  <img src="https://github.com/user-attachments/assets/e2e55e2c-9c64-4c32-ae4c-fac33e0035f8" width="250">
  <img src="https://github.com/user-attachments/assets/7d010dbb-abb4-455c-b87e-a4f8d7b03471" width="250">
  <img src="https://github.com/user-attachments/assets/673a0fa5-569c-4c7a-98b0-0ddf6eb99224" width="250">
</p>



https://github.com/user-attachments/assets/49bfd52e-1f98-45f4-9d4d-2ca81d26192c


El programa sigue un flujo lógico y bien definido:

1.  **Inicio (`main.py`):**
    * El archivo `main.py` actúa como el **punto de entrada** de la aplicación.
    * Configura la ventana principal de Flet (título, tamaño, tema).
    * Inicializa la clase `GitHubAPI`, que maneja toda la lógica de la comunicación con GitHub. Esto es clave, ya que **separa la lógica de negocio de la interfaz de usuario**.
    * Carga la configuración inicial (el token de GitHub si existe).
    * Crea la primera y única vista, `HomeView`, y la agrega a la pila de vistas de la página (`page.views.append`).
    * Establece la navegación (`page.go(page.views[0].route)`) para que Flet muestre la vista inicial.

2.  **La Vista Principal (`HomeView`):**
    * El archivo `home_view.py` define la clase `HomeView`, que es un contenedor de todos los componentes de la interfaz de usuario.
    * En su constructor (`__init__`), se crean y organizan todos los elementos visuales: campos de texto, botones, listas, etc.
    * Cada sección de la UI se construye en su propio método (`build_header`, `build_config_section`, etc.), lo que hace el código muy legible.
    * Los **manejadores de eventos** (`on_click`, `on_submit`) se vinculan a los métodos de la clase, como `load_releases` o `download_single_file`.

3.  **Gestión de la Lógica (`GitHubAPI`):**
    * La clase `GitHubAPI` está completamente separada de la UI. Su única responsabilidad es interactuar con la API de GitHub.
    * Tiene métodos para obtener *releases*, descargar archivos y manejar la autenticación.
    * Esto es fundamental para el **principio de responsabilidad única**: si algo falla en la descarga, sabes que el error está en `GitHubAPI`, no en la forma en que se muestra la interfaz.

4.  **Componentes Reutilizables (`ReleaseCard`):**
    * La clase `ReleaseCard` encapsula el diseño de un elemento de la lista.
    * En lugar de crear un `ft.ListTile` con todos sus atributos cada vez, `HomeView` simplemente instancia un `ReleaseCard` y le pasa los datos necesarios.
    * Esto hace que el código sea más limpio, fácil de leer y de mantener.

---

### Funcionamiento a Detalle de las Rutas en Flet

En Flet, el concepto de "rutas" es más simple que en frameworks web como React o Vue, ya que se basa en una **pila de vistas** (una "stack"). .

* **`page.views`:** Es una lista (`List`) de objetos de vista. Flet siempre muestra la última vista en esta lista.
* **`page.go(route)`:** Cuando se llama a este método, Flet busca una vista en `page.views` con la ruta especificada. Si la encuentra, la muestra. Si no, navega a la ruta. En tu caso, dado que solo tienes una vista, la ruta `/` siempre estará en el índice 0.
* **`page.on_view_pop`:** Es un evento que se activa cuando el usuario presiona el botón "atrás" del sistema operativo o el del propio Flet. Tu código maneja este evento sacando la vista superior de la pila (`page.views.pop()`) y yendo a la ruta de la nueva vista superior.

Aunque tu aplicación actual solo tiene una vista, el uso de rutas y la pila de vistas es la base para aplicaciones de una o varias pantallas.

---

### Cómo Añadir Más Funcionalidades a Futuro

La estructura actual está diseñada para ser fácilmente ampliable:

1.  **Añadir una nueva pantalla:**
    * Crea un nuevo archivo en el directorio `views/`, por ejemplo, `settings_view.py`.
    * Define una nueva clase, `SettingsView(ft.View)`, con su propia UI y lógica.
    * Asigna una ruta única en su constructor, como `route="/settings"`.
    * En `main.py` o en `HomeView`, añade un botón o un `ListTile` que, al hacer clic, use `page.go("/settings")` para navegar a la nueva pantalla. Flet manejará la navegación automáticamente.
    * Asegúrate de que la nueva vista incluya un botón de regreso o un `AppBar` que permita al usuario volver a la vista principal.

2.  **Añadir una nueva funcionalidad de GitHub:**
    * Si quieres, por ejemplo, listar los colaboradores de un repositorio, crea un nuevo método en la clase `GitHubAPI`.
    * Este método se encargaría de hacer la solicitud HTTP a la API de GitHub, sin interactuar con la UI.
    * Luego, desde `HomeView` (o desde cualquier otra vista), simplemente llama a ese nuevo método de `self.github_api` y usa los datos que te devuelve para actualizar la interfaz.

3.  **Añadir un componente de UI más complejo:**
    * Si necesitas un componente que se repita con frecuencia (como una barra de progreso personalizada o una tarjeta de usuario), créalo como una clase separada en el directorio `components/`.
    * De forma similar a `ReleaseCard`, define la clase, hazla heredar de un componente de Flet (`ft.Container`, `ft.Column`, etc.) e impórtala donde la necesites.

En resumen, la clave es mantener la **separación de preocupaciones**: la UI va en `views/` y `components/`, la lógica de la aplicación va en `GitHubAPI`, y el manejo de la aplicación y la navegación se centraliza en `main.py`. Esta arquitectura te permitirá crecer sin que tu código se vuelva difícil de manejar.
Ahora te muestro un ejemplo práctico de cómo agregar una nueva sección de "Acerca de" a tu aplicación, siguiendo la estructura modular que ya tienes. Verás lo fácil que es expandir tu proyecto manteniendo el código limpio y organizado.

-----

### Paso 1: Crear la nueva vista

Primero, crea un nuevo archivo en la carpeta `views/` llamado `about_view.py`. Este archivo contendrá la clase para la nueva pantalla.

**views/about_view.py**

```python
import flet as ft

class AboutView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/about",
            padding=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        self.page = page

        # Contenido de la vista
        self.controls = [
            ft.Text(
                "Acerca de Eden Releases Downloader",
                size=24,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text("Versión: 1.0.0"),
            ft.Text("Desarrollado por: Andromux ORG"),
            ft.Text("Esta es una herramienta para simplificar la descarga de assets de GitHub."),
            ft.ElevatedButton(
                "Volver al inicio",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: self.page.go("/"),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_800
                )
            )
        ]
```

En este código:

  * La clase `AboutView` hereda de `ft.View`.
  * Le asignamos una **ruta** única, `/about`, para poder navegar a ella.
  * El botón de "Volver al inicio" usa `self.page.go("/")` para navegar de regreso a la ruta principal, mostrando la `HomeView`.

-----

### Paso 2: Actualizar `main.py` para manejar la nueva vista

Ahora, necesitas modificar `main.py` para que la aplicación sepa cómo manejar la nueva ruta.

**main.py**

```python
import flet as ft
from github_api import GitHubAPI
from views.home_view import HomeView
from views.about_view import AboutView  # <-- Importamos la nueva vista

def main(page: ft.Page):
    page.title = "GitHub Releases Downloader"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_width = 1200
    page.window_height = 800
    page.padding = 0
    
    github_api = GitHubAPI()
    token = github_api.load_token_from_file()
    if token:
        github_api.set_token(token)
    
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(HomeView(page, github_api))
        elif page.route == "/about":
            page.views.append(AboutView(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)
    
if __name__ == "__main__":
    ft.app(target=main)
```

En este código:

  * **Importamos** la clase `AboutView` desde su archivo.
  * Reemplazamos la lógica de `view_pop` por un **manejador de eventos de cambio de ruta**, `route_change`.
  * El nuevo manejador de rutas es más robusto: cada vez que la ruta cambia (por ejemplo, al hacer clic en un enlace), borra la pila de vistas y la reconstruye con la vista correcta para la ruta actual.

-----

### Paso 3: Agregar el botón de navegación en `HomeView`

Finalmente, en `home_view.py`, agrega un botón o un enlace que permita al usuario ir a la nueva vista. El lugar más lógico es en el `AppBar` o en una sección de información.

**views/home\_view.py**

```python
...
from components.release_card import ReleaseCard

class HomeView(ft.View):
    def __init__(self, page: ft.Page, github_api: GitHubAPI):
        super().__init__(
            route="/",
            scroll=ft.ScrollMode.AUTO,
            padding=0,
        )
        self.page = page
        self.github_api = github_api
        self.releases_data = []
        self.selected_release = None
        
        # UI Components (sin cambios)
        self.repo_field = ft.TextField(...)
        self.token_field = ft.TextField(...)
        self.download_path_field = ft.TextField(...)
        self.releases_list = ft.ListView(...)
        self.assets_list = ft.ListView(...)
        self.progress_bar = ft.ProgressBar(...)
        self.status_text = ft.Text(...)
        
        # Construir la estructura de la vista
        self.controls = [
            self.build_header(),
            ft.Column(
                [
                    self.build_config_section(),
                    self.build_load_button(),
                    self.build_releases_section(),
                    self.build_assets_section(),
                ],
                expand=True,
                spacing=0
            ),
            self.build_status_section()
        ]

    # ... otros métodos ...

    def build_header(self):
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.CLOUD_DOWNLOAD, size=35, color=ft.Colors.BLUE),
                    ft.Text("Eden Gestor de Descargas", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                ], spacing=10),
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.DARK_MODE,
                        tooltip="Cambiar a tema oscuro",
                        on_click=self.toggle_theme
                    ),
                    ft.IconButton( # <-- Nuevo botón de "Acerca de"
                        icon=ft.Icons.INFO_OUTLINE,
                        tooltip="Acerca de",
                        on_click=lambda _: self.page.go("/about") # <-- Navega a la nueva ruta
                    ),
                ], spacing=5),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=ft.Colors.SURFACE,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)),
        )

    # ... el resto de la clase ...
```

En este código:

  * Modificamos el método `build_header` para agregar un `IconButton` para la nueva pantalla de "Acerca de".
  * El manejador `on_click` del botón ahora usa `self.page.go("/about")`.

Con estos cambios, tienes una nueva sección completamente funcional, demostrando la escalabilidad de tu estructura de proyecto.

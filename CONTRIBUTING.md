# Contribuir a Eden Releases Downloader

¡Gracias por tu interés en contribuir a **Eden Releases Downloader**! Este documento te guiará a través del proceso de contribución a nuestra herramienta GUI para descargar releases de GitHub. <cite/>

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Primeros Pasos](#primeros-pasos)
- [Configuración del Entorno](#configuración-del-entorno)
- [Proceso de Contribución](#proceso-de-contribución)
- [Estilo de Código](#estilo-de-código)
- [Pruebas](#pruebas)
- [Reportar Problemas](#reportar-problemas)
- [Sugerir Mejoras](#sugerir-mejoras)

## 🤝 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código. Por favor, reporta comportamientos inaceptables a los mantenedores del proyecto. <cite/>

## 🚀 Primeros Pasos

### Prerrequisitos

- **Python 3.8 o superior**
- **Git**
- **Conocimientos básicos de Flet y Python**
- **Familiaridad con la API de GitHub** (opcional pero útil)

### Configuración del Entorno

1. **Fork el repositorio**
   ```bash
   # Clona tu fork
   git clone https://github.com/tu-usuario/github-release-download-linux.git
   cd github-release-download-linux
   ```

2. **Configura el repositorio upstream**
   ```bash
   git remote add upstream https://github.com/andromux/github-release-download-linux.git
   ```

3. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

4. **Instala las dependencias**
   ```bash
   pip install flet requests pathlib
   # Si hay requirements.txt:
   pip install -r requirements.txt
   ```

5. **Verifica que todo funcione**
   ```bash
   python main.py
   ```

## 🔄 Proceso de Contribución

### 1. Crear una Rama

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
# o
git checkout -b ui/mejora-interfaz
```

### 2. Hacer Cambios

- Mantén los commits pequeños y enfocados
- Escribe mensajes de commit descriptivos
- Sigue las convenciones de estilo del proyecto
- Respeta la arquitectura modular existente

### 3. Probar tus Cambios

```bash
# Verificar que la app funcione correctamente
python main.py

# Probar diferentes escenarios:
# - Con y sin token de GitHub
# - Con repositorios públicos y privados
# - Descargas individuales y múltiples
```

### 4. Enviar Pull Request

1. Push a tu fork:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

2. Crear un Pull Request desde GitHub
3. Describe claramente los cambios realizados
4. Incluye capturas de pantalla si hay cambios en la UI
5. Espera la revisión

## 🎨 Estilo de Código

### Convenciones de Python

- **Sigue PEP 8**
- **Usa nombres descriptivos** para variables y funciones
- **Documenta funciones complejas** con docstrings
- **Mantén las líneas bajo 88 caracteres** (compatible con Black)

### Convenciones Específicas del Proyecto

Basándose en la estructura actual del proyecto: [1](#0-0) 

```python
import flet as ft
from github_api import GitHubAPI
from views.home_view import HomeView

def main(page: ft.Page):
    # Configura la página al inicio
    page.title = "Releases Downloader"
    page.theme_mode = ft.ThemeMode.SYSTEM
    
    # Inicializa la capa de API
    github_api = GitHubAPI()
    
    # Crea las vistas siguiendo el patrón existente
    home_view = HomeView(page, github_api)
    page.views.append(home_view)
```

### Estructura de Archivos del Proyecto

El proyecto sigue esta estructura modular: [2](#0-1) 

```
github-release-download-linux/
├── main.py                    # Punto de entrada de la aplicación
├── github_api.py             # Lógica de comunicación con GitHub API
├── views/                    # Vistas de la aplicación
│   └── home_view.py         # Vista principal
├── components/               # Componentes reutilizables
│   └── release_card.py      # Tarjeta de release
├── .secret_token.json       # Token de GitHub (no incluir en commits)
└── README.md
```

### Patrones de Arquitectura

El proyecto implementa **separación de responsabilidades**: [3](#0-2) 

- **`main.py`**: Punto de entrada y configuración
- **`GitHubAPI`**: Lógica de negocio y comunicación con API
- **`HomeView`**: Interfaz de usuario y manejo de eventos
- **`ReleaseCard`**: Componentes reutilizables

## 🧪 Pruebas

Actualmente el proyecto no tiene pruebas automatizadas, pero puedes contribuir añadiéndolas:

### Pruebas Manuales Recomendadas

```bash
# Verificar funcionalidad básica
python main.py

# Probar casos específicos:
# 1. Cargar releases sin token
# 2. Cargar releases con token válido
# 3. Descargar archivos individuales
# 4. Descargar múltiples archivos
# 5. Cambiar repositorio
# 6. Alternar tema claro/oscuro
```

### Añadir Pruebas Automatizadas

Si quieres contribuir con pruebas, crea un directorio `tests/` y sigue este patrón:

```python
import pytest
from github_api import GitHubAPI

def test_github_api_initialization():
    api = GitHubAPI()
    assert api.repo == "eden-emulator/Releases"
    assert api.base_url.endswith("/repos/eden-emulator/Releases")
```

## 🐛 Reportar Problemas

### Antes de Reportar

- Verifica que el problema no esté ya reportado
- Asegúrate de usar la última versión
- Intenta reproducir el problema

### Información a Incluir

- **Descripción clara** del problema
- **Pasos para reproducir** el error
- **Comportamiento esperado** vs **comportamiento actual**
- **Capturas de pantalla** de la interfaz
- **Información del sistema**:
  - Versión de Python
  - Versión de Flet
  - Sistema operativo
  - ¿Usas token de GitHub?

### Plantilla de Issue

```markdown
**Descripción del problema**
Una descripción clara del bug en Eden Releases Downloader.

**Pasos para reproducir**
1. Abre la aplicación con `python main.py`
2. Configura el repositorio como '...'
3. Haz click en 'Cargar Releases'
4. Ver error

**Comportamiento esperado**
Los releases deberían cargarse correctamente.

**Capturas de pantalla**
Si aplica, añade capturas de la interfaz.

**Información del sistema:**
 - OS: [ej. Windows 11, Ubuntu 22.04]
 - Python: [ej. 3.9.7]
 - Flet: [ej. 0.21.0]
 - Token GitHub: [Sí/No]
```

## 💡 Sugerir Mejoras

### Tipos de Contribuciones Bienvenidas

- 🐛 **Corrección de bugs** en la descarga o interfaz
- ✨ **Nuevas características** como filtros de releases
- 📚 **Mejoras en documentación** y comentarios
- 🎨 **Mejoras en UI/UX** siguiendo el diseño de Flet
- ⚡ **Optimizaciones** en descargas o API calls
- 🧪 **Añadir pruebas** automatizadas
- 🔧 **Nuevos componentes** reutilizables

### Ideas Específicas para el Proyecto

Basándose en la funcionalidad actual: [4](#0-3) 

- **Filtros avanzados** para releases (por fecha, tamaño, etc.)
- **Historial de descargas** 
- **Configuración de proxy** para la API
- **Soporte para múltiples repositorios**
- **Verificación de checksums** de archivos
- **Modo batch** para descargar de múltiples repos

### Para Nuevas Características

1. **Abre un issue primero** para discutir la idea
2. Espera feedback antes de comenzar a desarrollar
3. Mantén el alcance pequeño y enfocado
4. Respeta la arquitectura modular existente
5. Incluye documentación en el código

## 📝 Commit Messages

Usa el formato de Conventional Commits:

```
tipo(alcance): descripción

feat(ui): añadir filtro por fecha en releases
fix(api): corregir manejo de errores en descarga
docs(readme): actualizar instrucciones de instalación
style(components): mejorar espaciado en ReleaseCard
refactor(github_api): simplificar método get_releases
ui(theme): mejorar contraste en modo oscuro
```

## 🏷️ Versioning

Este proyecto usa [Semantic Versioning](https://semver.org/):

- **MAJOR**: cambios incompatibles en la API o estructura
- **MINOR**: nuevas funcionalidades compatibles
- **PATCH**: correcciones de bugs compatibles

## 📞 ¿Necesitas Ayuda?

- 💬 **Abre un issue** para preguntas sobre el código
- 📧 **Contacta a Andromux ORG** para consultas generales
- 📖 **Revisa la documentación** en el README.md
- 🔍 **Estudia el código** - está bien documentado y estructurado

## 🎉 Reconocimientos

Todos los contribuidores serán reconocidos en:
- README.md del proyecto
- Release notes de nuevas versiones
- Comentarios en el código para contribuciones significativas

## 🔧 Arquitectura del Proyecto

Para contribuir efectivamente, es importante entender la arquitectura: [5](#0-4) 

### Flujo de la Aplicación

1. **`main.py`** inicializa la aplicación y crea las dependencias
2. **`GitHubAPI`** maneja toda la comunicación con GitHub
3. **`HomeView`** coordina la interfaz de usuario
4. **`ReleaseCard`** muestra información de cada release

### Añadir Nuevas Vistas

Si quieres añadir una nueva pantalla:

```python
# views/settings_view.py
import flet as ft

class SettingsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/settings")
        # Tu implementación aquí
```

¡Gracias por contribuir a Eden Releases Downloader! 🙏

---

**Nota**: Este es un documento vivo que puede cambiar. Siempre revisa la última versión antes de contribuir.

## Notas

Este CONTRIBUTING.md está específicamente adaptado al proyecto Eden Releases Downloader, incorporando su arquitectura modular con `GitHubAPI`, `HomeView`, y `ReleaseCard`. <cite/> El documento refleja la estructura actual del proyecto que usa Flet para la interfaz gráfica y mantiene una clara separación entre la lógica de negocio (API de GitHub) y la presentación (vistas y componentes). <cite/>

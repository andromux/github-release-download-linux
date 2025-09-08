import flet as ft
from typing import List, Dict
from datetime import datetime
import threading
from pathlib import Path
from github_api import GitHubAPI
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
        
        # UI Components
        self.repo_field = ft.TextField(
            label="Repositorio (usuario/repo)",
            value=self.github_api.repo,
            prefix_icon=ft.Icons.FOLDER,
            on_submit=self.update_repo,
            expand=True,
            helper_text="Ejemplo: andromux/releases_download_eden"
        )
        self.token_field = ft.TextField(
            label="Token de GitHub (opcional)",
            value=self.github_api.token or "",
            prefix_icon=ft.Icons.KEY,
            password=True,
            can_reveal_password=True,
            expand=True,
            helper_text="Para evitar límites de rate limiting"
        )
        self.download_path_field = ft.TextField(
            label="Carpeta de descarga",
            value="./downloads",
            prefix_icon=ft.Icons.FOLDER_OPEN,
            expand=True,
            read_only=True
        )
        self.releases_list = ft.ListView(expand=True, spacing=2, padding=10)
        self.assets_list = ft.ListView(expand=True, spacing=2, padding=10)
        self.progress_bar = ft.ProgressBar(value=0, bgcolor=ft.Colors.SURFACE, color=ft.Colors.BLUE, height=8)
        self.status_text = ft.Text(
            "🚀 Listo para descargar releases de GitHub",
            size=14,
            color=ft.Colors.BLUE,
            text_align=ft.TextAlign.CENTER
        )
        
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
        
    # --- Métodos de Ayuda ---
    
    def _format_size(self, size_bytes: int) -> str:
        """Convierte bytes a un formato legible."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

    def update_status(self, message: str, color: str = "blue"):
        """Actualiza el texto de estado."""
        self.status_text.value = message
        self.status_text.color = color
        self.page.update()
    
    def toggle_theme(self, e):
        """Cambia entre tema claro y oscuro."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.Icons.LIGHT_MODE
            e.control.tooltip = "Cambiar a tema claro"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.Icons.DARK_MODE
            e.control.tooltip = "Cambiar a tema oscuro"
        self.page.update()

    def show_about_dialog(self, e):
        """Muestra el diálogo de información."""
        dialog = ft.AlertDialog(
            title=ft.Text("Acerca del Administrador Eden Releases"),
            content=ft.Column([
                ft.Text("Eden Releases Downloader GUI v1.0.0", weight=ft.FontWeight.BOLD),
                ft.Text("Una herramienta moderna para descargar releases de GitHub con interfaz gráfica."),
                ft.Text("Autor: Andromux ORG", style=ft.TextThemeStyle.BODY_SMALL),
            ], tight=True, scroll=ft.ScrollMode.AUTO, height=300),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: self.page.close(dialog))],
        )
        self.page.open(dialog)
        self.page.update()
        
    # --- Métodos para construir la UI ---
    
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
                    ft.IconButton(
                        icon=ft.Icons.INFO_OUTLINE,
                        tooltip="Acerca de",
                        on_click=self.show_about_dialog
                    ),
                ], spacing=5),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=ft.Colors.SURFACE,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)),
        )

    def build_config_section(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("⚙️ Configuración", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([self.repo_field, ft.ElevatedButton("Actualizar", icon=ft.Icons.REFRESH, on_click=self.update_repo, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE,))], spacing=10),
                    ft.Row([self.token_field, ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.save_token, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN,))], spacing=10),
                    ft.Row([self.download_path_field, ft.ElevatedButton("Seleccionar", icon=ft.Icons.FOLDER_OPEN, on_click=self.select_download_folder, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.ORANGE,))], spacing=10),
                ], spacing=15),
                padding=20
            ),
            elevation=2,
            margin=10
        )
        
    def build_load_button(self):
        return ft.Container(
            content=ft.ElevatedButton(
                "Cargar Releases",
                icon=ft.Icons.DOWNLOAD,
                on_click=self.load_releases,
                style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE, elevation={"": 2, "pressed": 8}, padding=ft.padding.symmetric(horizontal=30, vertical=15)),
                width=200,
                height=50
            ),
            alignment=ft.alignment.center,
            margin=10
        )

    def build_releases_section(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📦 Releases Disponibles", size=18, weight=ft.FontWeight.BOLD),
                    self.releases_list
                ], spacing=10),
                padding=20
            ),
            elevation=2,
            margin=10
        )
        
    def build_assets_section(self):
        download_buttons = ft.Row([
            ft.ElevatedButton("📥 Descargar Seleccionados", icon=ft.Icons.DOWNLOAD_FOR_OFFLINE, on_click=self.download_selected_files, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN,)),
            ft.ElevatedButton("📦 Descargar Todos", icon=ft.Icons.DOWNLOAD, on_click=self.download_all_assets, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.PURPLE,))
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("📁 Archivos de la Release", size=18, weight=ft.FontWeight.BOLD),
                    self.assets_list,
                    download_buttons
                ], spacing=10),
                padding=20
            ),
            elevation=2,
            margin=10
        )

    def build_status_section(self):
        return ft.Container(
            content=ft.Column([
                self.progress_bar,
                self.status_text
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.SURFACE,
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)),
        )

    # --- Métodos para la lógica de los eventos ---
    
    def update_repo(self, e):
        new_repo = self.repo_field.value.strip()
        if new_repo:
            self.github_api.set_repo(new_repo)
            self.releases_data = []
            self.releases_list.controls.clear()
            self.assets_list.controls.clear()
            self.update_status(f"📂 Repositorio actualizado: {self.github_api.repo}", "blue")
            self.page.update()

    def save_token(self, e):
        token = self.token_field.value.strip()
        if not token:
            self.update_status("❌ Token vacío", "red")
            return
        
        try:
            self.github_api.set_token(token)
            self.github_api.save_token_to_file(token)
            self.update_status("✅ Token configurado correctamente", "green")
        except Exception as ex:
            self.update_status(f"❌ Error: {str(ex)}", "red")

    def select_download_folder(self, e):
        def get_directory_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.download_path_field.value = e.path
                self.page.update()
                self.update_status(f"📁 Carpeta seleccionada: {e.path}", ft.Colors.GREEN)
        
        folder_picker = ft.FilePicker(on_result=get_directory_result)
        self.page.overlay.append(folder_picker)
        self.page.update()
        folder_picker.get_directory_path()

    def load_releases(self, e):
        def fetch_releases():
            try:
                self.update_status("📡 Obteniendo releases...", "blue")
                self.releases_data = self.github_api.get_releases()
                self.populate_releases_list()
                self.update_status(f"✅ {len(self.releases_data)} releases encontradas", "green")
            except Exception as ex:
                self.update_status(f"❌ Error: {str(ex)}", "red")
        
        threading.Thread(target=fetch_releases, daemon=True).start()

    def populate_releases_list(self):
        """Puebla la lista de releases usando el componente ReleaseCard."""
        self.releases_list.controls.clear()
        for i, release in enumerate(self.releases_data):
            release_card = ReleaseCard(
                release_data=release,
                on_click_handler=lambda e, idx=i: self.select_release(idx)
            )
            # Aplica el color de fondo alterno aquí, si es necesario
            if i % 2 != 0:
                 release_card.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
            self.releases_list.controls.append(release_card)
        self.page.update()

    def select_release(self, release_index: int):
        """Selecciona una release y muestra sus assets."""
        self.selected_release = self.releases_data[release_index]
        assets = self.selected_release['assets']
        self.assets_list.controls.clear()
        
        if not assets:
            self.assets_list.controls.append(ft.Text("⚠️ Esta release no tiene archivos para descargar", color=ft.Colors.ORANGE, size=16))
        else:
            for i, asset in enumerate(assets):
                asset_tile = ft.ListTile(
                    leading=ft.Icon(ft.Icons.FILE_DOWNLOAD, color=ft.Colors.GREEN),
                    title=ft.Text(asset['name'], weight=ft.FontWeight.W_500),
                    subtitle=ft.Text(f"Tamaño: {self._format_size(asset['size'])} | Descargas: {asset['download_count']}"),
                    trailing=ft.Row([
                        ft.IconButton(icon=ft.Icons.DOWNLOAD, tooltip="Descargar archivo", on_click=lambda e, a=asset: self.download_single_file(a)),
                        ft.Checkbox(value=False, data=asset, tooltip="Seleccionar para descarga múltiple")
                    ], tight=True),
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK) if i % 2 != 0 else None,
                )
                self.assets_list.controls.append(asset_tile)
        
        self.update_status(f"📦 Release seleccionada: {self.selected_release['name']}", ft.Colors.BLUE)
        self.page.update()

    def download_single_file(self, asset: Dict):
        """Descarga un solo archivo con barra de progreso."""
        def download_callback(downloaded, total_size):
            progress = (downloaded / total_size) * 100
            self.progress_bar.value = progress / 100
            self.page.update()
            
        def download():
            try:
                download_path = self.download_path_field.value or "./downloads"
                self.update_status(f"📥 Descargando {asset['name']}...", ft.Colors.BLUE)
                self.github_api.download_asset(asset, download_path, download_callback)
                self.progress_bar.value = 0
                self.update_status(f"✅ Descargado: {asset['name']}", ft.Colors.GREEN)
            except Exception as ex:
                self.update_status(f"❌ Error descargando {asset['name']}: {str(ex)}", ft.Colors.RED)
        
        threading.Thread(target=download, daemon=True).start()

    def download_selected_files(self, e):
        """Descarga los archivos seleccionados de la release."""
        selected_assets = []
        for control in self.assets_list.controls:
            if isinstance(control, ft.ListTile) and control.trailing:
                checkbox = next((item for item in control.trailing.controls if isinstance(item, ft.Checkbox) and item.value), None)
                if checkbox and checkbox.data:
                    selected_assets.append(checkbox.data)
        
        if not selected_assets:
            self.update_status("⚠️ No hay archivos seleccionados", ft.Colors.ORANGE)
            return

        def download_multiple():
            try:
                download_path = self.download_path_field.value or "./downloads"
                successful = 0
                total = len(selected_assets)
                for i, asset in enumerate(selected_assets):
                    try:
                        self.update_status(f"📥 Descargando {i+1}/{total}: {asset['name']}", ft.Colors.BLUE)
                        self.github_api.download_asset(asset, download_path)
                        successful += 1
                        self.progress_bar.value = (i + 1) / total
                        self.page.update()
                    except Exception as ex:
                        print(f"Error descargando {asset['name']}: {ex}")
                self.progress_bar.value = 0
                self.update_status(f"✅ Descarga completada: {successful}/{total} archivos", ft.Colors.GREEN)
            except Exception as ex:
                self.update_status(f"❌ Error en descarga múltiple: {str(ex)}", ft.Colors.RED)

        threading.Thread(target=download_multiple, daemon=True).start()

    def download_all_assets(self, e):
        """Marca todos los archivos y luego llama a la función de descarga."""
        if not self.selected_release:
            self.update_status("⚠️ Selecciona una release primero", ft.Colors.ORANGE)
            return
            
        for control in self.assets_list.controls:
            if isinstance(control, ft.ListTile) and control.trailing:
                for item in control.trailing.controls:
                    if isinstance(item, ft.Checkbox):
                        item.value = True
        self.page.update()
        self.download_selected_files(e)

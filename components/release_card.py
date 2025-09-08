import flet as ft
from typing import Dict
from datetime import datetime

class ReleaseCard(ft.ListTile):
    def __init__(self, release_data: Dict, on_click_handler):
        super().__init__()
        
        # Almacena los datos del lanzamiento y el handler para el click
        self.release_data = release_data
        self.on_click = on_click_handler
        
        # Construye la UI del componente
        self.leading = ft.Icon(ft.Icons.ARCHIVE, color=ft.Colors.BLUE)
        self.title = ft.Text(
            self.release_data['name'] or f"Release {self.release_data['tag_name']}",
            weight=ft.FontWeight.BOLD
        )
        self.subtitle = ft.Text(self._build_subtitle())
        self.trailing = ft.Icon(ft.Icons.CHEVRON_RIGHT)
        
    def _format_size(self, size_bytes: int) -> str:
        """Convierte bytes a formato legible."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
        
    def _build_subtitle(self) -> str:
        """Crea el texto del subtítulo con la información del lanzamiento."""
        published_date = datetime.strptime(
            self.release_data['published_at'], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%Y-%m-%d")
        
        total_size = sum(asset['size'] for asset in self.release_data['assets'])
        size_str = self._format_size(total_size) if total_size > 0 else "N/A"
        
        return (f"Tag: {self.release_data['tag_name']} | "
                f"Fecha: {published_date} | "
                f"Archivos: {len(self.release_data['assets'])} | "
                f"Tamaño: {size_str}")

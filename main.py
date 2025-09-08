#!/usr/bin/env python3
"""
GitHub Releases Downloader GUI
"""

import flet as ft
from github_api import GitHubAPI
from views.home_view import HomeView

def main(page: ft.Page):
    page.title = "Releases Downloader"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_width = 1200
    page.window_height = 800
    page.padding = 0
    
    # Inicializar la capa de API y cargar el token
    github_api = GitHubAPI()
    token = github_api.load_token_from_file()
    if token:
        github_api.set_token(token)
    
    # Crear y agregar la vista principal
    page.views.append(HomeView(page, github_api))
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_view_pop = view_pop
    page.go(page.views[0].route)
    
if __name__ == "__main__":
    ft.app(target=main)

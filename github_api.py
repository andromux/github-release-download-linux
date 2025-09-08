import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
import threading

class GitHubAPI:
    def __init__(self, token: Optional[str] = None):
        self.repo = "eden-emulator/Releases"
        self.base_url = f"https://api.github.com/repos/{self.repo}"
        self.session = requests.Session()
        self.token = token
        self._setup_session()
        
    def _setup_session(self):
        """Configura los headers de la sesión HTTP."""
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Releases-Downloader-GUI/2.0'
        }
        if self.token:
            headers['Authorization'] = f'token {self.token}'
        self.session.headers.update(headers)
    
    def set_repo(self, new_repo: str):
        """Cambia el repositorio y actualiza la URL base."""
        self.repo = new_repo
        self.base_url = f"https://api.github.com/repos/{self.repo}"
        
    def set_token(self, new_token: str):
        """Configura un nuevo token y actualiza la sesión."""
        self.token = new_token
        self._setup_session()
        
    def save_token_to_file(self, token: str):
        """Guarda el token en un archivo local."""
        token_data = {'github_token': token}
        with open('.secret_token.json', 'w') as f:
            json.dump(token_data, f, indent=2)

    def load_token_from_file(self) -> Optional[str]:
        """Carga el token desde un archivo local."""
        token_file = Path(".secret_token.json")
        if token_file.exists():
            try:
                with open(token_file, 'r') as f:
                    data = json.load(f)
                    return data.get('github_token')
            except:
                return None
        return None
        
    def get_releases(self) -> List[Dict]:
        """Obtiene una lista de releases del repositorio."""
        url = f"{self.base_url}/releases"
        response = self.session.get(url, params={'per_page': 20})
        response.raise_for_status()
        return response.json()
        
    def download_asset(self, asset: Dict, download_path: str, progress_callback=None):
        """Descarga un solo archivo con un callback para el progreso."""
        Path(download_path).mkdir(parents=True, exist_ok=True)
        file_path = Path(download_path) / asset['name']
        url = asset['browser_download_url']
        
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total_size > 0:
                        progress_callback(downloaded, total_size)

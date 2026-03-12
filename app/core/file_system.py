from pathlib import Path
from typing import List
try:
    import git
except ImportError:
    git = None

class GitManager:
    """Clase para gestionar la clonación y actualización de repositorios de skills."""

    @staticmethod
    def _prepare_auth_url(repo_url: str, token: str) -> str:
        """Inserta el token en la URL de GitLab para autenticación HTTPS."""
        if not token or "gitlab.com" not in repo_url:
            return repo_url
        
        # Formato: https://oauth2:TOKEN@gitlab.com/usuario/repo.git
        prefix = "https://"
        if repo_url.startswith(prefix):
            return f"https://oauth2:{token}@{repo_url[len(prefix):]}"
        return repo_url

    @staticmethod
    def sync_repository(repo_url: str, local_path: Path, token: str = None) -> bool:
        """Clona el repositorio si no existe o hace pull si ya existe."""
        if git is None:
            print("Error: GitPython no está instalado. Ejecute 'pip install gitpython'")
            return False
            
        auth_url = GitManager._prepare_auth_url(repo_url, token)
        
        try:
            if not local_path.exists():
                print(f"Clonando repositorio (con auth)...")
                git.Repo.clone_from(auth_url, local_path)
                return True
            else:
                print(f"Sincronizando repositorio en {local_path}...")
                repo = git.Repo(local_path)
                # Actualizar la URL del remoto por si el token cambió
                repo.remotes.origin.set_url(auth_url)
                repo.remotes.origin.pull()
                return True
        except Exception as e:
            print(f"Error al sincronizar con Git: {e}")
            return False

class FileSystemManager:
    """Clase para gestionar la lectura de archivos del sistema."""



    @staticmethod
    def read_file_content(file_path: Path) -> str:
        """Lee el contenido de un archivo de forma segura."""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            return f"# Error al leer el archivo\n\n{str(e)}"

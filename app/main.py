import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, 
    QHBoxLayout, QWidget, QFileDialog, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Qt

from app.core.file_system import FileSystemManager, GitManager
from app.core.md_engine import MarkdownEngine
from app.ui.components import FileSidebar, FileViewerContainer

# Configuración desde variables de entorno
GITLAB_REPO_URL = os.getenv("GITLAB_REPO_URL", "https://gitlab.com/tu-usuario/tu-repo-de-skills.git")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
DEFAULT_SKILLS_PATH = Path.home() / ".skills-platform/repository"

class MainWindow(QMainWindow):
    """Ventana principal de la plataforma de Markdown."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MD Platform - Visualizador de Markdown")
        self.resize(1000, 700)

        # Sincronizar repositorio al iniciar
        self._sync_skills()
        
        # Usar la ruta predeterminada de skills
        self.current_dir = DEFAULT_SKILLS_PATH
        if not self.current_dir.exists():
            self.current_dir.mkdir(parents=True, exist_ok=True)
            
        self.md_engine = MarkdownEngine(Path("assets/css/markdown.css"))

    def _sync_skills(self):
        """Sincroniza los skills desde el repositorio remoto con autenticación."""
        print(f"Sincronizando con {GITLAB_REPO_URL}...")
        GitManager.sync_repository(GITLAB_REPO_URL, DEFAULT_SKILLS_PATH, token=GITLAB_TOKEN)
        
        # Componentes UI
        self._init_ui()
        self._refresh_files()

    def _init_ui(self):
        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Botón para abrir directorio
        self.open_dir_btn = QPushButton("Abrir Carpeta")
        self.open_dir_btn.clicked.connect(self._select_directory)
        main_layout.addWidget(self.open_dir_btn)

        # Splitter (Sidebar | Viewer)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.sidebar = FileSidebar()
        self.sidebar.file_selected.connect(self._load_markdown_file)
        
        # Usamos el contenedor que tiene el header + viewer
        self.viewer_container = FileViewerContainer()
        
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.viewer_container)
        
        # Proporciones iniciales (Sidebar: 200px, Viewer: Resto)
        self.splitter.setStretchFactor(1, 4)
        
        main_layout.addWidget(self.splitter)

    def _select_directory(self):
        """Abre un diálogo para seleccionar el directorio de archivos MD."""
        dir_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", str(self.current_dir))
        if dir_path:
            self.current_dir = Path(dir_path)
            self._refresh_files()

    def _refresh_files(self):
        """Actualiza el directorio raíz del sidebar."""
        self.sidebar.set_root_path(str(self.current_dir))

    def _load_markdown_file(self, file_path: Path):
        """Carga y renderiza el contenido del archivo MD seleccionado."""
        md_text = FileSystemManager.read_file_content(file_path)
        html_content = self.md_engine.render(md_text)
        self.viewer_container.update_view(file_path.name, html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    
    # Estilo básico QSS
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QSplitter::handle {
            background-color: #ccc;
        }
        QPushButton {
            padding: 8px;
            background-color: #0078d4;
            color: white;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #106ebe;
        }
        QTreeView {
            border: none;
            background-color: white;
            outline: none;
        }
        QTreeView::item {
            padding: 4px;
        }
        QTreeView::item:selected {
            background-color: #e5f3ff;
            color: #000;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

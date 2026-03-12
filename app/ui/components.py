from PySide6.QtWidgets import (
    QTreeView, QTextBrowser, 
    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFrame, QFileSystemModel
)
from PySide6.QtCore import Qt, Signal, QItemSelection, QModelIndex
from pathlib import Path
from typing import List

class FileSidebar(QWidget):
    """Componente para mostrar el árbol de carpetas y archivos MD."""
    file_selected = Signal(Path)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        # Título
        self.title_label = QLabel("Archivos")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; padding: 10px; background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        self.layout.addWidget(self.title_label)

        # Modelo de sistema de archivos
        self.file_model = QFileSystemModel()
        self.file_model.setNameFilters(["*.md"])
        self.file_model.setNameFilterDisables(False) # Oculta los archivos que no coinciden en lugar de deshabilitarlos
        
        # Árbol de archivos
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setHeaderHidden(True)
        # Ocultar columnas de tamaño, tipo y fecha
        for i in range(1, 4):
            self.tree_view.hideColumn(i)
            
        self.tree_view.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.layout.addWidget(self.tree_view)

    def set_root_path(self, path: str):
        """Actualiza el directorio raíz del árbol."""
        root_index = self.file_model.setRootPath(path)
        self.tree_view.setRootIndex(root_index)

    def _on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        """Emite la señal cuando se selecciona un archivo .md."""
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            # Solo emitir si es un archivo (no una carpeta)
            if not self.file_model.isDir(index):
                file_path = Path(self.file_model.filePath(index))
                self.file_selected.emit(file_path)
                

class FileHeader(QWidget):
    """Componente para mostrar el nombre del archivo actual."""

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 10, 15, 10)
        self.layout.setSpacing(10)
        
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
        """)

        self.file_icon = QLabel("📄") # Icono simple
        self.file_name_label = QLabel("Ningún archivo seleccionado")
        
        self.layout.addWidget(self.file_icon)
        self.layout.addWidget(self.file_name_label)
        self.layout.addStretch()

    def set_file_name(self, name: str):
        """Actualiza el nombre del archivo mostrado."""
        self.file_name_label.setText(name)


class MDViewer(QTextBrowser):
    """Componente para visualizar el contenido Markdown convertido a HTML."""

    def __init__(self):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setPlaceholderText("Selecciona un archivo para visualizarlo...")
        
    def display_content(self, html_content: str):
        """Renderiza el contenido HTML en el visor."""
        self.setHtml(html_content)


class FileViewerContainer(QWidget):
    """Contenedor que agrupa el Header y el Visor."""

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header = FileHeader()
        self.viewer = MDViewer()

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.viewer)

    def update_view(self, file_name: str, html_content: str):
        """Actualiza tanto el encabezado como el contenido del visor."""
        self.header.set_file_name(file_name)
        self.viewer.display_content(html_content)

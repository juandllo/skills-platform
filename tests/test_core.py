import pytest
from pathlib import Path
from app.core.file_system import FileSystemManager
from app.core.md_engine import MarkdownEngine

def test_get_markdown_files(tmp_path):
    # Crear archivos de prueba
    (tmp_path / "file1.md").write_text("content")
    (tmp_path / "file2.txt").write_text("content")
    (tmp_path / "file3.MD").write_text("content")
    
    files = FileSystemManager.get_markdown_files(str(tmp_path))
    
    assert len(files) == 2
    assert files[0].name == "file1.md"
    assert files[1].name == "file3.MD"

def test_markdown_rendering():
    css_path = Path("assets/css/markdown.css")
    engine = MarkdownEngine(css_path)
    
    md_text = "# Title\n\n**Bold**"
    html = engine.render(md_text)
    
    assert "Title</h1>" in html
    assert "<strong>Bold</strong>" in html
    assert "<html>" in html
    assert "markdown-body" in html

def test_read_file_content(tmp_path):
    p = tmp_path / "hello.md"
    p.write_text("Hello World", encoding='utf-8')
    
    content = FileSystemManager.read_file_content(p)
    assert content == "Hello World"

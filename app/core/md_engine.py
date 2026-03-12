import markdown
from pathlib import Path

class MarkdownEngine:
    """Clase para convertir Markdown a HTML estilizado."""

    def __init__(self, css_path: Path):
        self.css_path = css_path
        self.extensions = [
            'fenced_code',
            'codehilite',
            'tables',
            'toc',
            'extra'
        ]

    def render(self, md_text: str) -> str:
        """Convierte texto MD a HTML completo con CSS embebido."""
        # Convertir MD a HTML
        content_html = markdown.markdown(md_text, extensions=self.extensions)
        
        # Leer CSS
        css_content = ""
        if self.css_path.exists():
            css_content = self.css_path.read_text(encoding='utf-8')
        
        # Plantilla HTML final para QTextBrowser
        html_template = f"""
        <html>
        <head>
            <style>
            {css_content}
            </style>
        </head>
        <body>
            <div class="markdown-body">
                {content_html}
            </div>
        </body>
        </html>
        """
        return html_template

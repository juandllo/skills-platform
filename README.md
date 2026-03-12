# Skills Platform 🚀

**Skills Platform** es una herramienta de escritorio potente y ligera construida con **Python** y **PySide6**. Su objetivo principal es centralizar la gestión de tus "skills" (fragmentos de conocimiento, prompts, scripts o lógica reutilizable) almacenados en un repositorio remoto de GitLab y permitirte visualizarlos e inyectarlos en tus proyectos locales de forma eficiente.

## 🌟 Características Principales

-   **Sincronización Automática con GitLab**: Al iniciar, la aplicación clona o actualiza automáticamente tu repositorio de skills mediante un Token de Acceso Personal.
-   **Visualizador Markdown Enriquecido**: Renderizado elegante con resaltado de sintaxis (Pygments) y soporte completo para tablas y bloques de código.
-   **Navegación Intuitiva**: Sidebar dinámico para explorar tus carpetas de skills con facilidad.
-   **Arquitectura Modular**: Diseñada para separar la lógica del sistema de archivos, el motor de renderizado y la interfaz de usuario.

## 🛠️ Requisitos Previos

-   **Python 3.10+**
-   **Git** instalado en tu sistema.
-   Un **Token de Acceso Personal (PAT)** de GitLab con permisos de `read_repository`.

## ⚙️ Configuración y Uso

### 1. Clonar e Instalar Dependencias

```bash
git clone <url-de-este-proyecto>
cd skills-platform
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Para que la aplicación se conecte a tu repositorio de GitLab, crea un archivo `.env` en la raíz del proyecto:

```env
# URL de tu repositorio de skills (HTTPS)
GITLAB_REPO_URL=https://gitlab.com/tu-usuario/tu-repositorio-de-skills.git

# Tu Token de Acceso Personal de GitLab
GITLAB_TOKEN=glpat-TU_TOKEN_AQUI_12345
```

> 💡 **Nota de Seguridad**: El archivo `.env` está incluido en el `.gitignore` para proteger tus credenciales. Nunca lo subas a un repositorio público.

### 3. Ejecutar la Aplicación

```bash
python -m app.main
```

## 🏗️ Estructura del Proyecto

-   `app/core/`: Lógica de sincronización Git, manejo de archivos y motor Markdown.
-   `app/ui/`: Componentes de la interfaz de usuario (Sidebar, Visor, Contenedores).
-   `assets/`: Estilos CSS para el visor y recursos visuales.
-   `.skills-platform/`: Directorio local donde se clona el repositorio de skills (ignorado por Git).

---
*Desarrollado con ❤️ para mejorar la productividad en la gestión de conocimiento.*

@echo off
REM Activar el entorno virtual de IA-MangaJaNai-CLI y dejar la terminal lista para ejecutar comandos
cd /d "%~dp0IA-MangaJaNai-CLI"

if not exist "venv_mangajanai" (
    echo El entorno virtual no existe. Ejecuta install_win.bat primero.
    pause
    exit /b 1
)

call venv_mangajanai\Scripts\activate.bat

REM Deja la terminal abierta para que el usuario pueda ejecutar comandos en el venv
cmd /K

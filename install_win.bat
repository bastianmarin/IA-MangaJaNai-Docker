@echo off
REM 0. Instala dependencias necesarias (git, curl, tar) si no existen
where git >nul 2>nul || (
    echo Git no encontrado. Por favor instala Git manualmente.
    exit /b 1
)
where curl >nul 2>nul || (
    echo curl no encontrado. Por favor instala curl manualmente.
    exit /b 1
)
where tar >nul 2>nul || (
    echo tar no encontrado. Por favor instala tar manualmente.
    exit /b 1
)

REM 1. Clona el repositorio IA-MangaJaNai-CLI si no existe
if not exist "IA-MangaJaNai-CLI" (
    git clone https://github.com/bastianmarin/IA-MangaJaNai-CLI.git
)
cd IA-MangaJaNai-CLI

REM 2. Descarga los modelos si no existen
if not exist "models" (
    mkdir models
    curl -L -o models/IllustrationJaNai_V1_ModelsOnly.zip https://github.com/the-database/MangaJaNai/releases/download/1.0.0/IllustrationJaNai_V1_ModelsOnly.zip
    curl -L -o models/MangaJaNai_V1_ModelsOnly.zip https://github.com/the-database/MangaJaNai/releases/download/1.0.0/MangaJaNai_V1_ModelsOnly.zip
    tar -xf models/IllustrationJaNai_V1_ModelsOnly.zip -C models
    tar -xf models/MangaJaNai_V1_ModelsOnly.zip -C models
)

REM 3. Crea y activa un entorno virtual con Python (usa python instalado en el sistema)
if not exist "venv_mangajanai" (
    python -m venv venv_mangajanai
)
call venv_mangajanai\Scripts\activate.bat

REM 4. Actualiza pip
python -m pip install --upgrade pip

REM 5. Instala los requirements
python -m pip install -r ..\requirements.txt
python -m pip install -r requirements.txt

REM 6. Instala torch y torchvision para CUDA 12.1
python -m pip install torch==2.2.1+cu121 torchvision==0.17.1+cu121 --index-url https://download.pytorch.org/whl/cu121

cd ..
echo Instalacion completada. Puedes ejecutar convert.py ahora.

# IA-MangaJaNai-Docker

This repository is designed to facilitate the extraction, enhancement (upscale), and compression of images from PDF files, using GPU acceleration. It is ideal for use on rental machines with powerful GPUs, allowing you to process large volumes of images quickly and efficiently. It has been tested and mainly used on GPU rental services like Vast.ai.

## What does it do?

- Extracts images from PDF files.
- Upscales images using AI (MangaJaNai) leveraging the GPU.
- Compresses the enhanced images into CBZ files ready for manga or comic reading.

## Recommended requirements

- **Operating system:** Ubuntu 20.04 (a clean image works perfectly)
- **RAM:** 16 GB or more
- **GPU:** NVIDIA with at least 12 GB VRAM (e.g., RTX 3060 or higher)
- **Python:** The script will automatically install Python 3.12 if not present

> **Note:** Currently, **there is no support for NVIDIA 5000 series GPUs**

## Installation

### Linux (Recommended: Ubuntu)

1. **Clone the repository and enter the folder:**

```bash
# Clone this repository and enter the folder
cd IA-MangaJaNai-Docker
```

2. **Run the installation script:**

```bash
# Give execution permissions and run the installer
chmod +x install.sh
./install.sh
```

This will install all necessary dependencies, Python, the AI models, and set up the environment.

### Windows

> **Important:** You must have Python 3.12 already installed and available in your PATH on Windows. The scripts will not work with other Python versions or if Python 3.12 is not in your PATH.

1. **Clone this repository and enter the folder:**

Open PowerShell or CMD and run:

```powershell
git clone https://github.com/bastianmarin/IA-MangaJaNai-Docker.git
cd IA-MangaJaNai-Docker
```

2. **Run the Windows installer:**

```powershell
install_win.bat
```

This will install all required dependencies, download the models, and create the virtual environment.

## Usage

### Linux

1. **Place your PDF files in the `input/` folder**

2. **Run the main script:**

```bash
python3.12 convert.py
```

3. **Results:**
   - Extracted and upscaled images are saved in the `output/` folder.
   - Final CBZ files are found in the `zip/` folder.

### Windows

1. **Place your PDF files in the `input/` folder**

2. **Activate the virtual environment:**

```bat
venv_shell.bat
```

This will open a terminal with the virtual environment activated.

3. **Run the main script:**

```bat
python convert.py
```

4. **Results:**
   - Extracted and upscaled images are saved in the `output/` folder.
   - Final CBZ files are found in the `zip/` folder.

## Additional notes

- The process leverages the GPU to accelerate image upscaling.
- If you use a rental machine (e.g., Vast.ai, LambdaLabs, RunPod, Paperspace, etc.), you can use a base Ubuntu 20.04 image and follow these steps without issues.
- If you encounter dependency problems, make sure your GPU is compatible with CUDA 12.1 and you have enough VRAM.
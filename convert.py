import os
import shutil
import subprocess
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) no está instalado. Instala con: pip install PyMuPDF")
    sys.exit(1)

def create_directories(base_path):
    input_dir = os.path.join(base_path, "input")
    output_dir = os.path.join(base_path, "output")
    zip_dir = os.path.join(base_path, "zip")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(zip_dir, exist_ok=True)
    return input_dir, output_dir, zip_dir

def extract_images_from_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            pdf_name_no_ext = os.path.splitext(filename)[0]
            current_pdf_output_folder = os.path.join(output_dir, pdf_name_no_ext)
            os.makedirs(current_pdf_output_folder, exist_ok=True)
            try:
                doc = fitz.open(pdf_path)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    image_list = page.get_images(full=True)
                    for img_index, img_info in enumerate(image_list):
                        xref = img_info[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"].lower()
                        if not image_bytes:
                            continue
                        if image_ext not in ['png', 'jpeg', 'jpg', 'gif', 'bmp', 'tiff', 'jp2']:
                            image_ext = 'png'
                        image_filename = f"page_{page_num + 1:03d}_img_{img_index + 1:03d}.{image_ext}"
                        image_save_path = os.path.join(current_pdf_output_folder, image_filename)
                        with open(image_save_path, "wb") as img_file:
                            img_file.write(image_bytes)
                doc.close()
            except Exception as e:
                print(f"Error extrayendo imágenes de {filename}: {e}")

def get_python_executable(venv_path):
    if os.name == "nt":
        # Windows
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        # Linux/Mac: usa el mismo Python que ejecuta este script
        return sys.executable

def upscale_image_with_mangajanai(image_path, output_folder, venv_path, mangajanai_src_path):
    python_exe = get_python_executable(venv_path)
    run_upscale = os.path.join(mangajanai_src_path, "run_upscale.py")
    os.makedirs(output_folder, exist_ok=True)
    cmd = [
        python_exe,
        run_upscale,
        "-f", image_path,
        "-o", output_folder,
        "-u", "2"
    ]
    def quote(path):
        return f'"{path}"' if ' ' in path else path
    cmd_str = ' '.join([quote(arg) if i in [0,1,3,5] else arg for i, arg in enumerate(cmd)])
    print(f"Comando a ejecutar: {cmd_str}")
    print(f"Upscaling {image_path} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error en upscale de {image_path}:\n{result.stderr}")
    else:
        print(f"Upscale terminado para {image_path}")

def upscale_folder_with_mangajanai(input_folder, output_folder, venv_path, mangajanai_src_path):
    python_exe = get_python_executable(venv_path)
    run_upscale = os.path.join(mangajanai_src_path, "run_upscale.py")
    os.makedirs(output_folder, exist_ok=True)
    cmd = [
        python_exe,
        run_upscale,
        "-d", input_folder,
        "-o", output_folder,
        "-u", "2"
    ]
    def quote(path):
        return f'"{path}"' if ' ' in path else path
    cmd_str = ' '.join([quote(arg) if i in [0,1,3,5] else arg for i, arg in enumerate(cmd)])
    print(f"Comando a ejecutar: {cmd_str}")
    print(f"Upscaling carpeta {input_folder} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error en upscale de {input_folder}:\n{result.stderr}")
    else:
        print(f"Upscale terminado para {input_folder}")

def compress_to_cbz(folder_path, zip_dir):
    base_name = os.path.join(zip_dir, os.path.basename(folder_path))
    shutil.make_archive(base_name, 'zip', root_dir=folder_path)
    zip_file = base_name + ".zip"
    cbz_file = base_name + ".cbz"
    if os.path.exists(cbz_file):
        os.remove(cbz_file)
    os.rename(zip_file, cbz_file)
    print(f"CBZ creado: {cbz_file}")

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_dir, output_dir, zip_dir = create_directories(base_path)
    venv_path = os.path.join(base_path, "IA-MangaJaNai-CLI", "venv_mangajanai")
    mangajanai_src_path = os.path.join(base_path, "IA-MangaJaNai-CLI", "src")

    print("Extrayendo imágenes de PDFs...")
    extract_images_from_pdfs(input_dir, output_dir)

    print("\nUpscale de imágenes con MangaJaNai...")
    for folder in os.listdir(output_dir):
        folder_path = os.path.join(output_dir, folder)
        if os.path.isdir(folder_path):
            upscaled_folder = folder_path + "_upscaled"
            os.makedirs(upscaled_folder, exist_ok=True)
            # Upscale todo el directorio de una vez
            upscale_folder_with_mangajanai(folder_path, upscaled_folder, venv_path, mangajanai_src_path)
            print(f"\nComprimiendo {upscaled_folder} a CBZ...")
            compress_to_cbz(upscaled_folder, zip_dir)

    print("\nProceso completo.")

if __name__ == "__main__":
    main()

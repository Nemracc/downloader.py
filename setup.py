import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import tarfile
import shutil

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(PROJECT_DIR, "downloads")
VENV_DIR = os.path.join(PROJECT_DIR, "venv")

# URLs de Geckodriver (última versión 0.34.0, modificar si hay nueva)
GECKODRIVER_WIN = "https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.34.0-win64.zip"
GECKODRIVER_LINUX = "https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.34.0-linux64.tar.gz"

def create_download_folder():
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)
        print("[✔] Carpeta downloads/ creada")

def create_virtualenv():
    if not os.path.exists(VENV_DIR):
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    print("[✔] Entorno virtual listo")

def install_requirements():
    pip_path = os.path.join(VENV_DIR, "Scripts" if os.name=="nt" else "bin", "pip")
    subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    print("[✔] Dependencias instaladas")

def download_geckodriver():
    system = platform.system()
    if system == "Windows":
        url = GECKODRIVER_WIN
        zip_path = os.path.join(PROJECT_DIR, "geckodriver.zip")
        print("[...] Descargando Geckodriver para Windows")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(PROJECT_DIR)
        os.remove(zip_path)

    elif system == "Linux":
        url = GECKODRIVER_LINUX
        tar_path = os.path.join(PROJECT_DIR, "geckodriver.tar.gz")
        print("[...] Descargando Geckodriver para Linux")
        urllib.request.urlretrieve(url, tar_path)
        with tarfile.open(tar_path, "r:gz") as tar_ref:
            tar_ref.extractall(PROJECT_DIR)
        os.remove(tar_path)
        os.chmod(os.path.join(PROJECT_DIR, "geckodriver"), 0o755)
    else:
        print("[✖] Sistema no soportado")
        sys.exit(1)

    print("[✔] Geckodriver listo")

def run_main():
    python_path = os.path.join(VENV_DIR, "Scripts" if os.name=="nt" else "bin", "python")
    subprocess.check_call([python_path, "main.py"])

if __name__ == "__main__":
    create_download_folder()
    create_virtualenv()
    install_requirements()
    download_geckodriver()
    run_main()

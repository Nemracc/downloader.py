import os
from tqdm import tqdm

def ensure_download_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_filename_from_url(url):
    return url.split("/")[-1].split("?")[0] or "download.bin"

def create_progress_bar(total, desc):
    return tqdm(
        total=total,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=desc,
        dynamic_ncols=True
    )

def log_bandwidth(current_speed, active_downloads):
    print(f"💡 Velocidad actual: {current_speed:.2f} MB/s | Descargas simultáneas: {active_downloads}")

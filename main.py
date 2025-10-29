import asyncio
from downloader.manager import adaptive_download

def load_urls(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    urls = load_urls("urls.txt")
    if not urls:
        print("No se encontraron URLs en urls.txt")
    else:
        asyncio.run(adaptive_download(urls))

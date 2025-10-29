import aiohttp
import aiofiles
import os
import time
from .config import CHUNK_SIZE, RETRY_LIMIT
from .utils import get_filename_from_url

async def download_file(url, download_path, monitor, ui):
    filename = get_filename_from_url(url)
    filepath = os.path.join(download_path, filename)

    file_mode = "wb"
    downloaded = 0
    total = 0

    for attempt in range(RETRY_LIMIT):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=None) as resp:
                    total = int(resp.headers.get("Content-Length", 0))
                    await ui.update(filename, downloaded, total, 0, "Descargando")

                    async with aiofiles.open(filepath, file_mode) as f:
                        start_time = time.time()
                        last_time = start_time
                        last_bytes = downloaded

                        async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
                            await f.write(chunk)
                            downloaded += len(chunk)
                            await monitor.add_bytes(len(chunk))

                            now = time.time()
                            if now - last_time >= 1:
                                speed = (downloaded - last_bytes) / (1024 * 1024) / (now - last_time)
                                await ui.update(filename, downloaded, total, speed, "Descargando")
                                last_time = now
                                last_bytes = downloaded

            await ui.update(filename, total, total, 0, "✅ Completado")
            return
        except Exception as e:
            await ui.update(filename, downloaded, total, 0, f"❌ Error: {e}")

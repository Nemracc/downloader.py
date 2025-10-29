import asyncio
from .worker import download_file
from .bandwidth import BandwidthMonitor
from .utils import ensure_download_folder, log_bandwidth
from .config import (
    DOWNLOAD_FOLDER,
    INITIAL_CONCURRENT_DOWNLOADS,
    MIN_CONCURRENT_DOWNLOADS,
    MAX_CONCURRENT_DOWNLOADS,
    ADJUST_INTERVAL,
    SPEED_THRESHOLD,
)
from .ui import DownloadUI
from .selenium_driver import get_direct_link

async def adaptive_download(urls):
    ensure_download_folder(DOWNLOAD_FOLDER)
    monitor = BandwidthMonitor()
    ui = DownloadUI()

    asyncio.create_task(monitor.measure_speed())
    asyncio.create_task(ui.run_ui())

    active_limit = INITIAL_CONCURRENT_DOWNLOADS
    pending_urls = list(urls)
    running_tasks = []

    while pending_urls or running_tasks:
        running_tasks = [t for t in running_tasks if not t.done()]

        speed = monitor.get_speed()
        running = len(running_tasks)
        log_bandwidth(speed, running)

        if speed < SPEED_THRESHOLD and active_limit > MIN_CONCURRENT_DOWNLOADS:
            active_limit -= 1
        elif speed > SPEED_THRESHOLD * 2 and active_limit < MAX_CONCURRENT_DOWNLOADS:
            active_limit += 1

        while len(running_tasks) < active_limit and pending_urls:
            original_url = pending_urls.pop(0)
            # Obtener URL directa con Selenium
            direct_url = await asyncio.to_thread(get_direct_link, original_url)
            task = asyncio.create_task(download_file(direct_url, DOWNLOAD_FOLDER, monitor, ui))
            running_tasks.append(task)

        await asyncio.sleep(1)

    await asyncio.gather(*running_tasks)

import asyncio
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.progress import Progress

class DownloadUI:
    def __init__(self):
        self.console = Console()
        self.status_data = {}
        self.lock = asyncio.Lock()

    async def update(self, filename, downloaded, total, speed, status):
        async with self.lock:
            self.status_data[filename] = {
                "downloaded": downloaded,
                "total": total,
                "speed": speed,
                "status": status
            }

    def make_table(self):
        table = Table(title="📥 Gestor de Descargas", expand=True)
        table.add_column("Archivo", style="cyan", no_wrap=True)
        table.add_column("Progreso", justify="right")
        table.add_column("Tamaño Total", justify="right")
        table.add_column("Velocidad (MB/s)", justify="right")
        table.add_column("Estado", justify="center")

        for file, info in self.status_data.items():
            progress = (info["downloaded"] / info["total"] * 100) if info["total"] > 0 else 0
            table.add_row(
                file,
                f"{progress:.1f}%",
                f"{info['total'] / (1024 * 1024):.2f} MB",
                f"{info['speed']:.2f}",
                info["status"]
            )
        return table

    async def run_ui(self):
        with Live(self.make_table(), refresh_per_second=2) as live:
            while True:
                async with self.lock:
                    live.update(self.make_table())
                await asyncio.sleep(1)

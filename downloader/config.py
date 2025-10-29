MAX_CONCURRENT_DOWNLOADS = 6     # límite máximo posible
MIN_CONCURRENT_DOWNLOADS = 1     # límite mínimo
INITIAL_CONCURRENT_DOWNLOADS = 3 # inicio adaptativo
CHUNK_SIZE = 1024 * 512
DOWNLOAD_FOLDER = "downloads"
RETRY_LIMIT = 5
ADJUST_INTERVAL = 10             # segundos entre reajustes
SPEED_THRESHOLD = 1.0            # MB/s bajo el cual reducimos descargas

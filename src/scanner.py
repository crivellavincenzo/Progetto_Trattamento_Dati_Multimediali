from pathlib import Path


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def get_image_files(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"La cartella non esiste: {folder_path}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Il percorso non è una cartella: {folder_path}")

    image_files = []

    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            image_files.append(file_path)

    return image_files
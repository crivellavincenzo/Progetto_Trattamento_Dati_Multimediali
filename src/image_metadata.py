from pathlib import Path
from PIL import Image

# partendo da un'immagine, ne restiuisce delle informazioni
def get_image_metadata(file_path):
    file_path = Path(file_path)

    with Image.open(file_path) as image:
        width, height = image.size
        image_format = image.format

        exif_data = image.getexif()
        has_exif = len(exif_data) > 0

    file_size = file_path.stat().st_size

    return {
        "file_path": file_path,
        "file_name": file_path.name,
        "width": width,
        "height": height,
        "pixels": width * height,
        "format": image_format,
        "file_size": file_size,
        "has_exif": has_exif
    }

# Seleziona l'immagine da consigliare privilegiando:
# 1. il maggior numero di pixel;
# 2. a parità di pixel, la presenza di EXIF;
# 3. a parità, il formato JPEG;
# 4. infine, la maggiore dimensione del file.
def choose_best_image(group):
    metadata_list = [
        get_image_metadata(file_path)
        for file_path in group
    ]

    max_pixels = max(
        metadata["pixels"]
        for metadata in metadata_list
    )

    candidates = [
        metadata
        for metadata in metadata_list
        if metadata["pixels"] == max_pixels
    ]

    exif_candidates = [
        metadata
        for metadata in candidates
        if metadata["has_exif"]
    ]

    if exif_candidates:
        candidates = exif_candidates

    jpeg_candidates = [
        metadata
        for metadata in candidates
        if metadata["format"] == "JPEG"
    ]

    if jpeg_candidates:
        candidates = jpeg_candidates

    return max(
        candidates,
        key=lambda metadata: metadata["file_size"]
    )
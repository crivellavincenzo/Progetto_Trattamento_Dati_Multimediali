# PIL => permette di aprire e leggere un immagine
from PIL import Image
import imagehash

# per ogni immagine, utilizzeremo un hash percettivo 'perceptual hash' (pHash)
# pHash restituirà per immagini simili, degli hash simili tra loro.
def calculate_phash(file_path):
    with Image.open(file_path) as image:
        return imagehash.phash(image)


# threshold => tolleranza, la distanza che devono avere due immagini per potersi definire simili.
# tutto l'algoritmo si basa semplicemente su questo valore, 5 significa che i due hash differiscono di 5 bit
def find_near_duplicates(image_files, threshold=5):
    near_duplicates = []

    hashes = {}

    for file_path in image_files:
        try:
            hashes[file_path] = calculate_phash(file_path)
        except Exception as e:
            print(f"Errore durante l'analisi di {file_path.name}: {e}")

    files = list(hashes.keys())

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            file1 = files[i]
            file2 = files[j]

            hash1 = hashes[file1]
            hash2 = hashes[file2]

            # calcoliamo 'Hamming distance', cioè quanti bit sono diversi.
            distance = hash1 - hash2

            if distance <= threshold:
                near_duplicates.append(
                    {
                        "file1": file1,
                        "file2": file2,
                        "distance": distance
                    }
                )

    return near_duplicates
# hashlib => libreria standard di Python che fornisce diversi algoritmi crittografici di hashing.
# nel codice utilizzeremo 'SHA-256'
import hashlib
from collections import defaultdict

# quello che faremo e prendere per ogni byte un impronta di 256 bit e poi confrontare i risultati
# cercheremo le immagini esattamente duplicate

def calculate_sha256(file_path):
    # creando un object da lavorare
    sha256 = hashlib.sha256()

    # rb significa:
    #   r => read
    #   b => binary
    # il with gestisce la chiusura del file in maniera automatica.


    with open(file_path, "rb") as file:
        while True:
            # leggiamo a blocchi di 8kb, il valore è stato scelto principalmente perchè non risulta essere ne troppo piccolo, ne troppo grande.
            data = file.read(8192)

            if not data:
                break

            # aggiungiamo questo blocco corrente al calcolo degli hash sha-256
            sha256.update(data)

    #generiamo hash ottenuto in forma di stringa esadecimale
    return sha256.hexdigest()


def find_exact_duplicates(image_files):
    # creiamo una mappa di liste:
    #   la chiave sarà il codice hash, il pile_path sarà invece inserito nella
    #   lista per distinguere le varie immagini duplicate
    hashes = defaultdict(list)

    # calcoliamo l'hash di tutte le immagini e inseriamo i risultati nella lista
    for file_path in image_files:
        file_hash = calculate_sha256(file_path)
        #se due immagini hanno uno stesso file_hash, e quindi risulteranno duplicate
        hashes[file_hash].append(file_path)

    duplicates = []

    #prendiamo tutte le duplicate (almeno 2 per ogni lista della mappa)
    for files in hashes.values():
        if len(files) > 1:
            duplicates.append(files)

    return duplicates
# Deduplicazione di immagini

Progetto realizzato per il corso di **Trattamento dei Dati Multimediali**.

L'obiettivo del progetto è sviluppare un'applicazione Python in grado di individuare automaticamente immagini duplicate o quasi duplicate presenti all'interno di una cartella.

Il sistema distingue i **duplicati esatti** dalle immagini che presentano piccole differenze, come variazioni di dimensione, compressione o formato.

Al termine dell'analisi viene generato un report HTML contenente i gruppi di immagini individuati, alcune informazioni tecniche e un suggerimento sull'immagine da conservare.

---

## Funzionalità

Il programma permette di:

- scansionare automaticamente una cartella contenente immagini;
- individuare duplicati esatti tramite hash **SHA-256**;
- individuare immagini visivamente simili tramite **Perceptual Hash (pHash)**;
- raggruppare le immagini simili;
- estrarre informazioni tecniche dalle immagini;
- verificare la presenza di metadati EXIF;
- suggerire un'immagine da conservare per ogni gruppo;
- generare un report finale in formato HTML.

---

## Tecnologie utilizzate

Il progetto è sviluppato in **Python**.

Le principali librerie utilizzate sono:

- `pathlib` per la gestione dei percorsi e dei file;
- `hashlib` per il calcolo dell'hash SHA-256;
- `Pillow` per l'apertura e l'analisi delle immagini;
- `ImageHash` per il calcolo del perceptual hash (pHash).

---

## Struttura del progetto

```text
Progetto_Trattamento_Dati_Multimediali/
│
├── images/
│   └── immagini da analizzare
│
├── output/
│   └── report.html
│
├── src/
│   ├── main.py
│   ├── scanner.py
│   ├── exact_duplicates.py
│   ├── perceptual_duplicates.py
│   ├── duplicate_groups.py
│   ├── image_metadata.py
│   └── report.py
│
└── README.md
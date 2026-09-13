from pathlib import Path

from scanner import get_image_files
from exact_duplicates import find_exact_duplicates
from perceptual_duplicates import find_near_duplicates
from duplicate_groups import create_duplicate_groups
from image_metadata import get_image_metadata, choose_best_image
from report import generate_html_report

def main():
    #prendiamo il percorso del progetto, e sapendo che le immagini saranno in 'images'. le preleveremo.
    project_root = Path(__file__).resolve().parent.parent
    folder_path = project_root / "images"

    image_files = get_image_files(folder_path)

    print(f"Immagini trovate: {len(image_files)}")

    #FASE 1 - cerchiamo dei gruppi di duplicati, qui cerchiamo i duplicati esatti
    duplicates = find_exact_duplicates(image_files)

    if not duplicates:
        print("Nessun duplicato esatto trovato.")
        return

    print(f"\nGruppi di duplicati trovati: {len(duplicates)}")
    for index, group in enumerate(duplicates, start=1):
        print(f"\nGruppo {index}:")

        for file_path in group:
            print(f" - {file_path.name}")

    #FASE 2 - cerchiamo anche le immagini che possiamo descrivere come 'quasi duplicati'
    print("\n--- QUASI DUPLICATI ---")

    near_duplicates = find_near_duplicates(image_files)

    if not near_duplicates:
        print("Nessun quasi-duplicato trovato.")
    else:
        for result in near_duplicates:
            print(
                f"{result['file1'].name} <-> "
                f"{result['file2'].name} "
                f"(distanza pHash: {result['distance']})"
            )

    #FASE 3 - andiamo ad analizzare nel dettaglio il gruppo

    #creando un grafo, prende le coppie di immagini simili tra loro
    groups = create_duplicate_groups(near_duplicates)

    print("\n--- ANALISI DEI GRUPPI ---")

    for index, group in enumerate(groups, start=1):

        print(f"\nGruppo {index}:")

        for file_path in group:
            metadata = get_image_metadata(file_path)

            print(f"\n{metadata['file_name']}")
            print(f" Risoluzione: {metadata['width']} x {metadata['height']}")
            print(f" Pixel totali: {metadata['pixels']}")
            print(f" Formato: {metadata['format']}")
            print(f" Dimensione file: {metadata['file_size'] / 1024:.2f} KB")
            print(f" EXIF presenti: {'Sì' if metadata['has_exif'] else 'No'}")

        best_image = choose_best_image(group)

        print("\nImmagine consigliata:")
        print(f" {best_image['file_name']}")

    output_folder = project_root / "output"
    output_folder.mkdir(exist_ok=True)

    report_path = output_folder / "report.html"

    generate_html_report(
        groups,
        duplicates,
        near_duplicates,
        report_path
    )

    print("\nReport generato:")
    print(report_path)



if __name__ == "__main__":
    main()
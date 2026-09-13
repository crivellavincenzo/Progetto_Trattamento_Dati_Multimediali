from pathlib import Path

from image_metadata import get_image_metadata, choose_best_image


def are_exact_duplicates(file1, file2, exact_duplicates):
    for group in exact_duplicates:
        if file1 in group and file2 in group:
            return True

    return False


def get_phash_distance(file1, file2, near_duplicates):
    for duplicate in near_duplicates:
        same_order = (
                duplicate["file1"] == file1
                and duplicate["file2"] == file2
        )

        reverse_order = (
                duplicate["file1"] == file2
                and duplicate["file2"] == file1
        )

        if same_order or reverse_order:
            return duplicate["distance"]

    return None


def generate_html_report(
        groups,
        exact_duplicates,
        near_duplicates,
        output_path
):
    output_path = Path(output_path)

    html = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Report Deduplicazione Immagini</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f4f4f4;
                color: #222;
            }

            h1 {
                color: #333;
                margin-bottom: 30px;
            }

            h2 {
                margin-top: 0;
            }

            h3 {
                margin-top: 25px;
            }

            .group {
                background-color: white;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 8px;
            }

            table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 15px;
            }

            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
            }

            th {
                background-color: #eeeeee;
            }

            .relations {
                margin-top: 20px;
                padding: 15px;
                background-color: #f8f8f8;
                border-left: 5px solid #607d8b;
            }

            .recommended {
                margin-top: 20px;
                padding: 15px;
                background-color: #e8f5e9;
                border-left: 5px solid #2e7d32;
            }

            .exact {
                color: #1565c0;
                font-weight: bold;
            }

            .near {
                color: #ef6c00;
                font-weight: bold;
            }

            ul {
                margin-top: 10px;
            }

            li {
                margin-bottom: 8px;
            }
        </style>
    </head>

    <body>

    <h1>Report Deduplicazione Immagini</h1>
    """

    if not groups:
        html += "<p>Nessun gruppo di immagini simili trovato.</p>"

    for index, group in enumerate(groups, start=1):
        html += f"""
        <div class="group">

        <h2>Gruppo {index}</h2>

        <table>

        <tr>
            <th>File</th>
            <th>Risoluzione</th>
            <th>Pixel</th>
            <th>Formato</th>
            <th>Dimensione</th>
            <th>EXIF</th>
        </tr>
        """

        for file_path in sorted(group, key=lambda x: x.name.lower()):
            metadata = get_image_metadata(file_path)

            html += f"""
            <tr>
                <td>{metadata['file_name']}</td>

                <td>
                    {metadata['width']} x {metadata['height']}
                </td>

                <td>
                    {metadata['pixels']}
                </td>

                <td>
                    {metadata['format']}
                </td>

                <td>
                    {metadata['file_size'] / 1024:.2f} KB
                </td>

                <td>
                    {'Sì' if metadata['has_exif'] else 'No'}
                </td>
            </tr>
            """

        html += """
        </table>

        <div class="relations">
        <h3>Relazioni rilevate</h3>
        <ul>
        """

        group_files = sorted(
            list(group),
            key=lambda x: x.name.lower()
        )

        for i in range(len(group_files)):
            for j in range(i + 1, len(group_files)):
                file1 = group_files[i]
                file2 = group_files[j]

                if are_exact_duplicates(
                        file1,
                        file2,
                        exact_duplicates
                ):
                    html += f"""
                    <li>
                        <strong>{file1.name}</strong>
                        ↔
                        <strong>{file2.name}</strong>

                        <span class="exact">
                            — Duplicato esatto
                        </span>
                    </li>
                    """

                else:
                    distance = get_phash_distance(
                        file1,
                        file2,
                        near_duplicates
                    )

                    if distance is not None:
                        html += f"""
                        <li>
                            <strong>{file1.name}</strong>
                            ↔
                            <strong>{file2.name}</strong>

                            <span class="near">
                                — Quasi-duplicato
                                (distanza pHash: {distance})
                            </span>
                        </li>
                        """

        html += """
        </ul>
        </div>
        """

        best_image = choose_best_image(group)

        html += f"""
        <div class="recommended">

            <strong>Immagine consigliata:</strong>
            {best_image['file_name']}

            <br><br>

            <strong>Motivazione:</strong>

            <ul>
                <li>
                    Risoluzione:
                    {best_image['width']} x {best_image['height']}
                </li>

                <li>
                    Pixel totali:
                    {best_image['pixels']}
                </li>

                <li>
                    Formato:
                    {best_image['format']}
                </li>

                <li>
                    Dimensione file:
                    {best_image['file_size'] / 1024:.2f} KB
                </li>

                <li>
                    Metadati EXIF:
                    {'presenti' if best_image['has_exif'] else 'assenti'}
                </li>
            </ul>

        </div>

        </div>
        """

    html += """
    </body>
    </html>
    """

    output_path.write_text(
        html,
        encoding="utf-8"
    )

    return output_path
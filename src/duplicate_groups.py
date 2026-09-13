def create_duplicate_groups(near_duplicates):
    graph = {}
    # grafo con queste caratteristiche:
    #   chiave = immagine
    #   valore = insieme delle immagini simili collegate


    for duplicate in near_duplicates:
        file1 = duplicate["file1"]
        file2 = duplicate["file2"]

        #lo facciamo sia da F1 a F2, che fa F2 a F1, cosi sappiamo quale lista di File è associata a F1, e viceversa
        graph.setdefault(file1, set()).add(file2)
        graph.setdefault(file2, set()).add(file1)

    visited = set()
    groups = []

    # visita ricorsiva del grafo
    def visit(file, group):
        if file in visited:
            return

        visited.add(file)
        group.add(file)

        for neighbour in graph.get(file, []):
            visit(neighbour, group)

    # cerchiamo tutte le componenti connesse del grafo.
    for file in graph:
        if file not in visited:
            group = set()

            visit(file, group)

            if len(group) > 1:
                groups.append(group)

    return groups
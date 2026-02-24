from main import Generation_personnes

test = Generation_personnes(10)

def afficher_population(population):
    # En-tête
    headers = [
        "ID",
        "Alive",
        "Altruisme",
        "Role",
        "Coord",
        "Danger",
        "InGroup"
    ]

    # Largeur fixe des colonnes
    widths = [36, 6, 10, 15, 10, 8, 8]

    # Impression de l'en-tête
    for header, width in zip(headers, widths):
        print(f"{header:<{width}}", end=" ")
    print()
    print("-" * sum(widths))

    # Impression des lignes
    for person in population:
        row = [
            str(person[0]),                 # UUID
            str(person[1]),                 # Alive
            f"{person[2]:.3f}",             # Altruisme
            person[3],                      # Role
            str(person[4]),                 # Coord
            f"{person[5]:.3f}",             # Danger
            f"{person[6]:.3f}"              # InGroup
        ]

        for value, width in zip(row, widths):
            print(f"{value:<{width}}", end=" ")
        print()

afficher_population(test)
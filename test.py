from main import *

test = Generation_personnes(30)

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
            f"{person[2]:.2f}",             # Altruisme
            person[3],                      # Role
            str(person[4]),                 # Coord
            f"{person[5]:.2f}",             # Danger
            f"{person[6]:}"                 # InGroup
        ]

        for value, width in zip(row, widths):
            print(f"{value:<{width}}", end=" ")
        print()

def trouver_isoles(civilisation):
    directions = [(-1,0),(1,0),(0,-1),(0,1),
                  (-1,-1),(-1,1),(1,-1),(1,1)]
    
    coord_map = {person[COORD]: person for person in civilisation}
    isoles = []

    for person in civilisation:
        x, y = person[COORD]
        a_un_voisin = False

        for dx, dy in directions:
            voisin = coord_map.get((x+dx, y+dy))
            if voisin:
                a_un_voisin = True
                break  # dès qu’on trouve un voisin, on sort

        if not a_un_voisin:
            isoles.append((person[COORD], person[IS_IN_GROUPE]))
    
    return isoles

def afficher_groupes(population):
    # Trier la population par groupe, les isolés (-1) à la fin
    population_triee = sorted(population, key=lambda p: (p[IS_IN_GROUPE] if p[IS_IN_GROUPE] >= 0 else float('inf')))

    # En-tête
    headers = ["ID", "Alive", "Altruisme", "Role", "Coord", "Danger", "InGroup"]
    widths = [36, 6, 10, 15, 10, 8, 8]

    for header, width in zip(headers, widths):
        print(f"{header:<{width}}", end=" ")
    print()
    print("-" * sum(widths))


    groupe_courant = None
    for person in population_triee:
        if person[IS_IN_GROUPE] != groupe_courant:
            if groupe_courant is not None:
                print()  # saut de ligne entre les groupes
            groupe_courant = person[IS_IN_GROUPE]

        row = [
            str(person[ID]),
            str(person[IS_ALIVE]),
            f"{person[ALTRUISME]:.2f}",
            person[ROLE],
            str(person[COORD]),
            f"{person[DANGER]:.2f}",
            f"{person[IS_IN_GROUPE]}"
        ]
        for value, width in zip(row, widths):
            print(f"{value:<{width}}", end=" ")
        print()

groupement(test)
afficher_groupes(test)

def dessiner_population(population):

    grille = [["." for _ in range(LONGUEUR)] for _ in range(LARGEUR)]

    for person in population:
        x, y = person[COORD]
        if person[IS_IN_GROUPE] == -1:
            grille[y][x] = "X"
        else:
            grille[y][x] = str(person[IS_IN_GROUPE])

    print()

    for y in range(LONGUEUR):
        ligne = " ".join(grille[y])
        print(ligne)

dessiner_population(test)
from main import *

test_assign_roles = [
    [0, True, 0.58, 'Soldat', (9, 2), 0.29, 1],
    [1, True, 0.58, 'Reste', (9, 2), 0.29, 1],
    [2, True, 0.58, 'Reste', (9, 2), 0.29, 1]
]


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

def trouver_isoles(civilisation, n=2):
    directions = [(x,y) for x in range(-n,n+1) for y in range (-n, n+1) if (x,y) != (0,0)]

    
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
    
    print()


def debug_groupes(civilisation):
    dict_groupes = get_dict_groupes(civilisation)

    print("\n===== ETAT DES GROUPES =====\n")

    for gid, membres in dict_groupes.items():
        taille = len(membres)
        capacite = group_capacity(membres, civilisation)

        print(f"Groupe {gid}")
        print(f"  Nombre de personnes : {taille}")
        print(f"  Capacités : {capacite}")
        print("-" * 30)

def moyenne_groupe(test):
    compte = comptage_groupe(test)
    somme = sum(compte.values())
    nb_groupes = len(compte)
    return somme / nb_groupes


def civilisation_to_grid_role(civilisation):
    grid = np.full((LONGUEUR, LARGEUR), -1)

    role_map = {
        "Soldat": 0,
        "Medecin": 1,
        "Agriculteur": 2,
        "Eau": 3,
        "Reste": 4
    }

    for person in civilisation:
        x, y = person[COORD]
        grid[y][x] = role_map.get(person[ROLE], -1)

    return grid


def plot_civilisation_role(civilisation):
    grid = civilisation_to_grid_role(civilisation)

    cmap = mcolors.ListedColormap([
        "#f5f5dc",
        "red",      # Soldat
        "blue",     # Medecin
        "green",    # Agriculteur
        "cyan",     # Eau
        "lightgrey" # Reste
    ])

    plt.figure()
    img = plt.imshow(grid, cmap=cmap, vmin=-1, vmax=4)

    cbar = plt.colorbar(img)
    cbar.set_ticks([-1,0,1,2,3,4])
    cbar.set_ticklabels(["Fond","Soldat", "Medecin", "Agriculteur", "Eau", "Reste"])

    plt.title("Etat de la civilisation")
    plt.show()

def civilisation_to_grid_groupe(civilisation):
    grid = np.full((LONGUEUR, LARGEUR), -1)

    groupe_map = {p[IS_IN_GROUPE] : p[IS_IN_GROUPE] for p in civilisation}

    for person in civilisation:
        x, y = person[COORD]
        grid[y][x] = groupe_map.get(person[IS_IN_GROUPE], -1)

    return grid

def plot_civilisation_groupe(civilisation):
    grid = civilisation_to_grid_groupe(civilisation)

    plt.figure()
    img = plt.imshow(grid)

    cbar = plt.colorbar(img)

    plt.title("Etat de la civilisation")
    plt.show()

def initialisation(civilisation):
    plot_civilisation_role(civilisation)
    plot_civilisation_groupe(civilisation)
    segregation(civilisation)
    deplacer_individus(civilisation)
    k_means(civilisation)
    assign_role_to_reste(civilisation)
    debug_groupes(civilisation)
    afficher_population(civilisation)
    plot_civilisation_role(civilisation)
    plot_civilisation_groupe(civilisation)

test = Generation_personnes(160)
initialisation(test)


import random
import uuid

# probas metiers

PROBA_SOLDAT = 0.15
PROBA_MEDECIN = 0.15
PROBA_AGRO = 0.3
PROBA_EAU = 0.3


# proprietes individu

ID = 0
IS_ALIVE = 1
ALRTRUISME = 2
ROLE = 3
COORD = 4
DANGER = 5
IS_IN_GROUPE = 6

# autres constantes

largeur = 10
longeur = 10


def get_role():
    p = random.random()
    if p < PROBA_SOLDAT:
        return "Soldat"
    elif p < PROBA_SOLDAT + PROBA_MEDECIN:
        return "Medecin"
    elif p < PROBA_SOLDAT + PROBA_MEDECIN + PROBA_AGRO:
        return "Agriculteur"
    elif p < PROBA_SOLDAT + PROBA_MEDECIN + PROBA_AGRO + PROBA_EAU:
        return "Eau"
    else:
        return "Reste"

# renvoie la taille de notre grille

def round_3(n):
    return round(n,3)

def get_grid_taille():
    return (longeur, largeur)

def get_coords(population):
    x_max, y_max = get_grid_taille()

    coords_existantes = {person[COORD] for person in population}

    while True:
        coord = (
            random.randint(0, x_max - 1),
            random.randint(0, y_max - 1)
        )
        if coord not in coords_existantes:
            return coord


def Generation_personnes(nb):
    # personne : identifiant, is_alive, altruisme, role, (x,y), danger, is_in_groupe

    civilisation = []

    for _ in range(nb):
        personne = [0] * 7

        personne[ID] = uuid.uuid1()
        personne[IS_ALIVE] = True
        personne[ALRTRUISME] = round_3(random.random())
        personne[ROLE] = get_role()
        personne[COORD] = get_coords(civilisation)
        personne[DANGER] = round_3(random.random())
        personne[IS_IN_GROUPE] = round_3(random.random())

        

        civilisation.append(personne)

    return civilisation




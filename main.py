import random
import uuid
import numpy as np

# probas metiers

PROBA_SOLDAT = 0.15
PROBA_MEDECIN = 0.15
PROBA_AGRO = 0.3
PROBA_EAU = 0.3


# proprietes individu

ID = 0
IS_ALIVE = 1
ALTRUISME = 2
ROLE = 3
COORD = 4
DANGER = 5
IS_IN_GROUPE = 6

# autres constantes

LARGEUR = 10
LONGUEUR = 10


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

def round_2(n):
    return round(n,2)

def get_grid_taille():
    return (LONGUEUR, LARGEUR)

def init_coords_libres():

    coords_libres = [(x,y) for x in range(LONGUEUR) for y in range(LARGEUR)]
    random.shuffle(coords_libres)
    return coords_libres

def get_next_coord(coord_libres):

    if not coord_libres:
        raise ValueError("Trop de personnes et pas assez de coordonnées")
    return coord_libres.pop()



def Generation_personnes(nb):
    # personne : identifiant, is_alive, altruisme, role, (x,y), danger, is_in_groupe

    coordonées = init_coords_libres()


    civilisation = []

    for _ in range(nb):
        personne = [0] * 7

        personne[ID] = uuid.uuid1()
        personne[IS_ALIVE] = True
        personne[ALTRUISME] = round_2(random.random())
        personne[ROLE] = get_role()
        personne[COORD] = get_next_coord(coordonées)
        personne[DANGER] = round_2(random.random())
        personne[IS_IN_GROUPE] = -1
        


        civilisation.append(personne)

    return civilisation



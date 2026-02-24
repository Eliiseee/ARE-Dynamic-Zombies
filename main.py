from random import random
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


def Generation_personnes(n):
    retour = []

    for i in range(n):
        p = random.random()
        if p < PROBA_SOLDAT:
            retour.append(gen_person("Soldat"))
        elif p < PROBA_SOLDAT + PROBA_MEDECIN:
            retour.append(gen_person("Medecin"))
        elif p < PROBA_SOLDAT + PROBA_MEDECIN + PROBA_AGRO:
            retour.append(gen_person("Agriculteur"))
        elif p < PROBA_SOLDAT + PROBA_MEDECIN + PROBA_AGRO + PROBA_EAU:
            retour.append(gen_person("Eau"))
        else:
            retour.append(gen_person("Reste"))

    return retour


# renvoie la taille de notre grille

def get_grid_taille():
    return (longeur, largeur)


def gen_person(role):
    # personne : identifiant, is_alive, altruisme, role, (x,y), danger, is_in_groupe

    x_max, y_max = get_grid_taille()
    personne = []
    personne[ID] = uuid.uuid1()
    personne[IS_ALIVE] = True
    personne[ALRTRUISME] = random.random()
    personne[ROLE] = role
    personne[COORD] = (random.randint(x_max),random.randint(y_max))
    personne[DANGER] = random.random()
    personne[IS_IN_GROUPE] = random.random()




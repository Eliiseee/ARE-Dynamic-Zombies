import random
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

#proprietes groupe

ID_GROUPE = 0
LISTE_IND = 1
CAPACITES = 2
DANGER_GROUPE = 3
ETAT = 4

# autres constantes

LARGEUR = 22
LONGUEUR = 22


def get_role():
    """
    Fonction qui ne prend rien en argument.
    Renvoie un string correspondant à un métier.

    Les métiers disponibles :
    "Soldat"
    "Medecin"
    "Agriculteur"
    "Eau"
    "Reste", ce qui correspond au reste de la population ayant un métier différent ignoré ici.
    """
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
    """
    Fonction qui prend en argument un entier n.
    Renvoie un ce nombre n arrondi à 2 chiffres après la virgule.
    """
    return round(n,2)

def get_grid_taille():
    """
    Fonction qui ne prend rien en argument.
    Renvoie la taille de la grille sous forme d'un tuple.

    Le tuple est de la forme suivante:
    (LONGUEUR, LARGEUR)
    """
    return (LONGUEUR, LARGEUR)

def init_coords_libres():
    """
    Fonction qui ne prend rien en argument.
    Fonction qui permet de générer une liste de tuple de toutes les coordonées possibles de la grille de manière aléatoires.

    Exemple :

    [(0,1), (1,1), (5,2), ...]
    """
    coords_libres = [(x,y) for x in range(LONGUEUR) for y in range(LARGEUR)]
    random.shuffle(coords_libres)
    return coords_libres

def get_next_coord(coord_libres):
    """
    Fonction qui prend en argument une pile de coordonées libres fournie de la fonction init_coords_libres().
    Renvoie une coordonées libre et supprime cette coordonée de la pile.
    """

    if not coord_libres:
        raise ValueError("Trop de personnes et pas assez de coordonnées")
    return coord_libres.pop()

def get_dict_groupes(civilisation):
    dict_groupes = {}

    for personne in civilisation:
        id = personne[IS_IN_GROUPE]
        if id not in dict_groupes:
            dict_groupes[id] = set()
        dict_groupes[id].add(personne[ID])
    
    return dict_groupes

def find_person(id, civilisaion):
    for p in civilisaion:
        if p[ID] == id:
            return p
    return -1

def group_capacity(group, civilisation):
    capacity = {"Soldat" : 0, "Agriculteur" : 0, "Medecin" : 0, "Eau" : 0}
    nb_people = len(group)

    for id in group:
        person = find_person(id, civilisation)
        role = person[ROLE]

        if role != "Reste":
            capacity[role] += 1
    
    return { key:(round_2(val/nb_people)) for key,val in capacity.items()}

    
def mean_group_danger(group, civilisation):
    nb_people = len(group)
    danger = 0

    for id in group:
        personne = find_person(id,civilisation)
        danger += personne[DANGER]
    return round_2(danger/nb_people)



def group_info(civilisation):
    dict_groupes = get_dict_groupes(civilisation)
    liste_groupes = []

    for key,val in dict_groupes.items():
        groupe = [0]*5

        groupe[ID_GROUPE] = key
        groupe[LISTE_IND] = val
        groupe[CAPACITES] = group_capacity(val, civilisation)
        groupe[DANGER_GROUPE] = mean_group_danger(val, civilisation)
        groupe[ETAT] = "Alive"
    
        liste_groupes.append(groupe)

    return liste_groupes



def Generation_personnes(nb):
    """
    Fonction qui prend en argument un nombre de personne à générer dans la grille.
    Renvoie une liste de nb personnes sous la forme d'une liste.

    Chaque personne est une liste de 7 argument différents.
    /!\ Par défaut IS_IN_GROUPE = -1 /!\ 

    [ID, IS_ALIVE, ALTRUISME, ROLE, COORD, DANGER, IS_IN_GROUPE]

    Exemple : 

    [[1, True, 0.26, Reste, (5, 0), 0.53, 1], [2, True, 0.81, Soldat, (3, 2), 0.56, 1]
    """
    # personne : identifiant, is_alive, altruisme, role, (x,y), danger, is_in_groupe

    coordonées = init_coords_libres()

    civilisation = []

    for _ in range(nb):
        personne = [0] * 7

        personne[ID] = _
        personne[IS_ALIVE] = True
        personne[ALTRUISME] = round_2(random.random())
        personne[ROLE] = get_role()
        personne[COORD] = get_next_coord(coordonées)
        personne[DANGER] = personne[ALTRUISME]/2
        personne[IS_IN_GROUPE] = -1

        civilisation.append(personne)

    return civilisation


def comptage_groupe(civilisation):
    """
    Fonction qui prend en argument une civilisation.
    Renvoie un dictionnaire avec le numéro de groupe et le nombre de personne dans ce dernier.

    Exemple :

    {1: 16, 2: 16, 3: 18, 4: 16, 9: 9, 8: 16, 11: 8, 5: 1}
    """
    compte = {}
    for person in civilisation:
        if person[IS_IN_GROUPE] in compte: 
            compte[person[IS_IN_GROUPE]] += 1
        else:
            compte[person[IS_IN_GROUPE]] = 1
    return compte
    

def fusionner_groupes_proches_n(civilisation, n = 2, limite = 15, seuil_petits_groupes = 3):
    """
    Fonction qui prend forcément en argument une civilisation
    Fonction qui permet de rassembler plusieurs petits groupes afin d'en créer un plus gros.
    Ne renvoie rien. 
    
    Prend 3 arguments facultatifs :

    n : Nombre entier qui représente le rayon de nos recherches pour directions.

    limite : Nombre entier qui représente le nombre max de personnes dans un même groupe (afin d'éviter d'en avoir un très gros monopolisant tout).
    
    seuil_petits groupes : Nombre entier qui représente notre tolérance face à des petits groupes même si la limite est dépasssée (afin d'éviter au maximum les personnes totalement isolées)
    
    /!\ On modifie directement les valeurs dans la variable civilisation.
    """

    compte = comptage_groupe(civilisation)
    directions = [(x,y) for x in range(-n,n+1) for y in range (-n, n+1)]
    coord_map = {person[COORD]: person for person in civilisation}
    changed = True

    while changed:
        changed = False

        for person in civilisation:
            if person[IS_IN_GROUPE] <= 0:
                continue 
            x, y = person[COORD]
            voisins = [coord_map.get((x+dx, y+dy)) for dx, dy in directions if coord_map.get((x+dx, y+dy))]
            groupes_voisins = [v[IS_IN_GROUPE] for v in voisins if v[IS_IN_GROUPE] > 0]

            if groupes_voisins:
                min_groupe = min(groupes_voisins + [person[IS_IN_GROUPE]])
                taille_source = compte.get(person[IS_IN_GROUPE],0)
                taille_cible = compte.get(min_groupe,0)

                if person[IS_IN_GROUPE] != min_groupe and (taille_cible < limite or taille_source < seuil_petits_groupes) and taille_cible < limite + seuil_petits_groupes :
                    ancien = person[IS_IN_GROUPE]
                    person[IS_IN_GROUPE] = min_groupe
                    compte[ancien] -= 1
                    compte[min_groupe] = compte.get(min_groupe,0) + 1
                    changed = True

                for v in voisins:
                    if v[IS_IN_GROUPE] > 0 and v[IS_IN_GROUPE] != min_groupe:
                        taille_source_voisin = compte.get(v[IS_IN_GROUPE],0)
                        taille_cible = compte.get(min_groupe,0)
                        if taille_cible < limite or taille_source_voisin < seuil_petits_groupes and taille_cible < limite + seuil_petits_groupes:
                            ancien = v[IS_IN_GROUPE]
                            v[IS_IN_GROUPE] = min_groupe
                            compte[ancien] -= 1
                            compte[min_groupe] = compte.get(min_groupe,0) + 1
                            changed = True


def groupement(civilisation, n = 2):
    """
    Fonction qui prend forcément en argument une civilisation
    Fonction qui permet de créer de petits groupes dans les alentours de n cases.

    Argument facultatif :
    
    n : Nombre entier qui représente le rayon de nos recherches pour directions.

    On utilise la fonction fusionner_groupes_proches_n afin de générer des groupes plus gros.

    /!\ On modifie directement les valeurs dans la variable civilisation.
    """
    directions = [(x,y) for x in range(-n,n+1) for y in range (-n, n+1)]
    
    coord_map = {person[COORD]: person for person in civilisation}
    groupe_id = 1

    for person in civilisation:
        x, y = person[COORD]

        voisins = [coord_map.get((x+dx, y+dy)) for dx, dy in directions if coord_map.get((x+dx, y+dy))]

        if not voisins:
            person[IS_IN_GROUPE] = -1
            continue

        groupes_voisins = [v[IS_IN_GROUPE] for v in voisins if v[IS_IN_GROUPE] > 0]

        if groupes_voisins:
            min_groupe = min(groupes_voisins)
            person[IS_IN_GROUPE] = min_groupe
        else:
            person[IS_IN_GROUPE] = groupe_id
            groupe_id += 1

    fusionner_groupes_proches_n(civilisation)
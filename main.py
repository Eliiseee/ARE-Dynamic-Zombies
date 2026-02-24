from random import random

def Generation_personnes(n):
    proba_soldat = 0.15
    proba_medecin = 0.15
    proba_agriculteur = 0.3
    proba_eau = 0.3
    # proba_reste = 0.1 #pas necessaire

    retour = []

    for i in range(n):
        p = random.random()
        if p < proba_soldat:
            retour.append(["Soldat"])
        elif p < proba_soldat + proba_medecin:
            retour.append(["Medecin"])
        elif p < proba_soldat + proba_medecin + proba_agriculteur:
            retour.append(["Agriculteur"])
        elif p < proba_soldat + proba_medecin + proba_agriculteur + proba_eau:
            retour.append(["Eau"])
        else:
            retour.append(["Reste"])

    return retour

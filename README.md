# Le meilleur projet d'ARE de toute la Terre

  Liste d'étapes à faire :

  Remarques, afin de faciliter la lecture de notre code on va utiliser des constantes en écrivant en majuscule afin d'accéder aux indices. Par exemple METIER = 2. 

# 0. Liste de chose à faire pour la prochaine fois:

  1) Création d'une fonction de déplacement d'un individus. (échanger 1/4 de la population d'un groupe avec un autre en choisissant aléatoirement une direction (Nord, Sud, Est, Ouest))
 
  2) Création d'une fonction qui permet de rassembler géographiquement tous les individus d'un groupe entre eux.

  3) Création d'un système d'attaque et de zombie.

  4) Création de fonctions d'affichage via numpy.

  5) Création d'une fonction qui permet d'assigner un role manquant a la survie à une personne n'ayant pas de métiers (reste). -> DONE

  6) Creation d'une fonction qui effectue une segregation des personnes en groupes par leur role. -> DONE

  7) Faire un k-means pour grouper les gens. -> DONE

  8) Faire un affichage via tkinter qui permet de vérifier nos travaux / faire la simulation de manière plus simple (Omar je m'en occupe).

# 1. Créer une fonction qui permet de générer des individus de plusieurs type différents.

La fonction prendra en argument un nombre d'individus et renvoie une liste avec tout ces individus. Je pense qu'il serait meilleur que chaque individu soit une liste. (exemple soldat, medecin etc...) -> DONE 

# 2. Création de groupes de manières logique. (Premier groupe avec voisins puis fusions de groupes)
 
 1) Faire en sorte que dans chaque case il n'y ai qu'une unique personne (grâce à son id par exemple ou en connaissant en permanance la position de chacun des habitants). -> DONE

 2) Faire en sorte que plusieurs personnes objectivement proches puissent former un groupe. -> DONE

 3) Création de groupe et d'un ID pour chaque groupe, à partir de maintenant on essaiera d'identifier le groupe entier à la place d'un individu. -> DONE

 4) Fonction d'affichage pour les groupes et les individus sous format ASCII afin de vérifier le bon fonctionnement de nos fonctions. -> DONE

# 3. Amélioration du système de groupe.

1) Ajout d'une limite du nombre d'individus par groupes (par défaut 15). -> DONE

2) On autorise quand même certains individus isolés à rejoindre un groupe à proximité (moins de 3 par défaut) afin de compléter le groupe, on peut donc avoir des groupes légèrement supérieurs à 15. -> DONE

3) Ajout de nouveaux éléments dans les fonctions fusions et groupement afin d'être en correspondance avec ce qu'on a choisi précédemment. -> DONE

4) Création de la nouvelle fonction comptage_groupe qui retourne un dictionnaire avec le numéro de groupe et le nombre de personnes dedans. -> DONE

5) Création de la nouvelle fonction moyenne_groupe qui retourne la moyenne du nombre d'individus dans tout les groupes. -> DONE

# 4. Création de groupes beaucoup plus réalistes. 

1) Instauration de l'algorithme de ségrégation de Schelling. -> DONE

2) Instauration de Kmeans afin de créer K groupes sociaux. -> DONE

3) Création d'un système de mort.

4) Création d'un système d'attaque de zombie (sans les créer).

5) Création d'une fonction de migration d'un individus. (échanger 1/4 de la population d'un groupe avec un autre en choisissant aléatoirement une direction (Nord, Sud, Est, Ouest))

# 5. Création d'un système d'affichage dynamique via Tkinter.

1) Création des fonctions d'affiches avec des boutons.

2) Donner le choix de pouvoir choisir entre la simulation avec schelling ou la simulation dans un cadre oprimal (ce qu'on avait fait de base).




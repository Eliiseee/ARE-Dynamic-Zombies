# Le meilleur projet d'ARE de toute la Terre

 > Liste d'étapes à faire :

 > Remarques, afin de faciliter la lecture de notre code on va utiliser des constantes en écrivant en majuscule afin d'accéder aux indices. Par exemple METIER = 2. 

# 1. Créer une fonction qui permet de générer des individus de plusieurs type différents.

La fonction prendra en argument un nombre d'individus et renvoie une liste avec tout ces individus. Je pense qu'il serait meilleur que chaque individu soit une liste. (exemple soldat, medecin etc...) -> DONE 

# 2. Créer une fonction qui permet de générer une grille 2D et de regrouper plusieurs personnes de manières logique.

La fonction prendra en argument une civilisation et nous renvera une grille 2D qui sera notre environnement. Pour l'instant on ne s'occupe pas de rajouter des ressources sur cette grille et on ne gère pas les déplacement de chacun. 

 1) Faire en sorte que dans chaque case il y ai une unique personne (grâce à son id par exemple ou en connaissant en permanance la position de chacun des habitants).

 2) Faire en sorte que plusieurs personnes objectivement proches puissent se rejoindre géographiquement et former un cercle autour d'un centre (ce qui serait le plus logique).

 3) Création de groupe et d'un ID pour chaque groupe, à partir de maintenant on essaiera d'identifier le groupe entier à la place d'un individu.

 4) Création de petit groupe de plein de petit groupes de zombie proportionnel à la taille de la population. 

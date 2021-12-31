# Description #

Le script bruteforce.py suggère une liste des ations les plus rentables à partir d'un fichier contenant une liste d'actions.\
Contraintes :
- 500 euros maximun par client.
- Actions indivisibles.
- Actions uniques.


Le script bruteforce.py génère trois fichiers csv :

- .\csv_file\
    1.  results_all.csv :\
        Toutes les combinaisons possibles selon le fichier d'actions lu.
    2.  combination_no_expensive.csv :\
        Exclu les combinaisons dont le coût total est trop chère (500 euros).
    3.  list_of_decision.csv :\
        La combinaison d'actions la plus rentable respectant les critères de sélections. Puis, excluant les combinaisons comprenant des actions de la plus rentable, détermine la seconde plus rentable. etc.\
        eiau

# Utilisation #

Deux listes d'actions sont présentes, actions.csv et actions-5.csv.\
La première est la liste des 20 actions du projet 07 d'OC, le seconde, la liste des 5 premières seulement.\
Dans bruteforce.py :
- La ligne 9 permet la lecture de "actions-5.csv"
- La ligne 10 permet la lecture de "actions.csv"

Mettre en commentaire, la ligne relatif au fichier à ne pas lire.

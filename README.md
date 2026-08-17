# Gestionnaire de lessive

Un petit programme Python créé pour aider les étudiants à mieux gérer leur linge.

L'idée est simple : quand on vit seul, on ne sait pas forcément quand lancer une machine. On peut attendre trop longtemps et se retrouver sans vêtements propres, ou au contraire lancer une machine presque vide.

Ce programme permet donc d'enregistrer les vêtements que l'on met de côté et d'estimer le poids total du linge. Il indique ensuite si la machine commence à être suffisamment remplie.

## Fonctionnement

Au lancement, on indique la capacité de sa machine à laver :

```text
Capacité de la machine : 6 kg
```

On peut ensuite ajouter les vêtements au fur et à mesure.

Chaque vêtement possède un poids estimé. Par exemple :

| Vêtement              | Poids estimé |
| --------------------- | -----------: |
| Chaussette            |         50 g |
| Sous-vêtement / boxer |         70 g |
| Débardeur             |        100 g |
| T-shirt               |        180 g |
| Chemise               |        250 g |
| Short                 |        200 g |
| Pantalon              |        500 g |
| Jean                  |        750 g |
| Pull léger            |        350 g |
| Pull épais / laine    |        600 g |
| Sweat                 |        400 g |
| Hoodie                |        600 g |
| Veste légère          |        500 g |
| Veste épaisse         |        800 g |
| Manteau               |      1 000 g |
| Pyjama                |        250 g |
| Serviette de bain     |        500 g |

Ces valeurs sont des estimations : le poids réel dépend notamment de la taille et de la matière du vêtement.

### Exemple

Si on ajoute :

* 5 chaussettes
* 3 T-shirts
* 1 jean

le programme estime :

```text
5 × 50 g   = 250 g
3 × 180 g  = 540 g
1 × 750 g  = 750 g

Total = 1540 g
```

Le panier contient donc environ **1,54 kg de linge**.

## Suivi du remplissage

Le programme calcule automatiquement le pourcentage de remplissage de la machine.

Les seuils sont proportionnels à la capacité choisie :

|   Remplissage | Statut                                |
| ------------: | ------------------------------------- |
| Moins de 75 % | OK                                    |
|     75 à 90 % | Le panier commence à être bien rempli |
|    90 à 100 % | Presque plein                         |
| 100 % ou plus | Lessive à faire                       |

Par exemple, pour une machine de 6 kg :

```text
75 % = 4,5 kg
90 % = 5,4 kg
100 % = 6 kg
```

Si la capacité est changée à 8 kg, les seuils sont automatiquement recalculés.

## Gestion des vêtements

Tous les vêtements actuellement enregistrés sont affichés dans une liste.

Chaque ligne possède ses propres boutons :

* `− 1` : retire un exemplaire du vêtement ;
* `Supprimer` : supprime complètement ce type de vêtement.

Par exemple :

```text
Vêtement              Quantité       Poids       Actions
--------------------------------------------------------------
Chaussette                8           400 g      [- 1] [Supprimer]
T-shirt                   3           540 g      [- 1] [Supprimer]
Jean                      1           750 g      [- 1] [Supprimer]
```

Un bouton `Lessive faite` permet de vider le panier une fois la machine terminée.

## Sauvegarde

Le programme sauvegarde automatiquement les données dans un fichier `lessive.json`.

Ce fichier est placé dans le même dossier que le programme Python :

```text
GestionnaireLessive/
├── lessive.py
├── lessive.json
└── README.md
```

Cela permet de fermer le programme, voire l'éditeur de code, puis de le relancer plus tard sans perdre le linge enregistré.

La capacité de la machine est également sauvegardée.

## Installation

Le programme nécessite simplement **Python 3**.

Aucune bibliothèque externe n'est nécessaire : l'interface utilise Tkinter, inclus avec Python.

Pour lancer le programme :

```bash
python lessive.py
```

Sur certains systèmes, il faudra utiliser :

```bash
python3 lessive.py
```

Le fichier `lessive.json` sera créé automatiquement au premier lancement.

## Technologies utilisées

* Python 3
* Tkinter
* JSON
* pathlib

## Objectif du projet

Le projet a été pensé comme un petit outil pratique pour les étudiants, notamment ceux qui commencent à vivre seuls et doivent apprendre à gérer les tâches du quotidien.

Il sert également de projet Python simple permettant de travailler sur :

* les interfaces graphiques ;
* la sauvegarde de données ;
* les dictionnaires ;
* les fonctions ;
* les calculs ;
* la gestion de fichiers ;
* la persistance des données.

Le principe reste volontairement simple :

**Ajouter son linge → suivre le poids → atteindre le seuil → faire sa lessive.**

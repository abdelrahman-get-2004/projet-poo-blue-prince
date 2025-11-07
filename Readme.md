# Projet POO  - Blue Prince

Ceci est notre implémentation du jeu "Blue Prince" pour le projet de Programmation Orientée Objet .

## Membres du Groupe

* Abdelrahman
* Tiantian
* Idris

## 🚀 Instructions d'Installation et de Lancement

**Prérequis :** Python 3.x

1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/abdelrahman-get-2004/projet-poo-blue-prince.git
    cd projet-poo-blue-prince
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Lancer le jeu :**
    ```bash
    python main.py
    ```

## 🏛️ Architecture du Projet

Le projet est divisé en trois modules principaux pour faciliter le travail en parallèle et respecter les exigences (Héritage, Abstraction).

### 1. Module Joueur & Objets (Abdelrahman)

* **Responsabilité :** Gérer l'état du joueur et la définition de tous les objets interactifs (Héritage/Abstraction).
* **Fichiers :**
    * `joueur.py`: Contient la `classe Joueur`. Gère l'inventaire (`consommables` comme les pas, clés, gemmes et `objets_permanents`).
    * `objets.py`:
        * `classe abstraite Objet`: Classe parente pour tous les objets.
        * `classe ObjetPermanent(Objet)`: Enfant pour la pelle, le marteau, etc..
        * `classe Nourriture(Objet)`: Enfant pour la pomme, le gâteau, etc., avec une méthode `utiliser()` qui redonne des pas.

### 2. Module Pièces & Catalogue (Tiantian)

* **Responsabilité :** Définir la structure et les variations des pièces (Héritage).
* **Fichiers :**
    * `piece.py`:
        * `classe Piece`: Classe parente avec les attributs de base (nom, rareté, coût, portes).
        * `classe PieceMagasin(Piece)`: Enfant pour les pièces jaunes.
        * `classe PieceJardin(Piece)`: Enfant pour les pièces vertes.
        * ...autres classes enfants pour les différents types de pièces.
    * `catalogue.py`: Fichier qui crée et stocke les instances de toutes les pièces possibles du jeu (`PIOCHE_INITIALE`).

### 3. Module Moteur de Jeu & Grille (Idris)

* **Responsabilité :** Gérer la logique de jeu, l'affichage `pygame` et l'état de la grille 5x9.
* **Fichiers :**
    * `grille.py`:
        * `classe Grille`: Contient la matrice 5x9, gère la position du joueur et les méthodes `placer_piece()`, `get_piece()`.
    * `main.py` (ou `jeu.py`):
        * `classe Jeu`: Le "Game Manager". Initialise `pygame`, `Grille`, et `Joueur`.
        * Contient la boucle de jeu principale (`run()`) qui gère les événements (ZQSD), met à jour la logique (`mettre_a_jour()`) et dessine à l'écran (`dessiner()`).
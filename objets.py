# fichier: objets.py
from abc import ABC, abstractmethod

class Objet(ABC):
    """
    Classe Abstraite (Mère) pour tous les objets du jeu.
     (Ceci est une classe abstraite comme demandé)
    """
    def __init__(self, nom: str):
        self.nom = nom

    @abstractmethod
    def utiliser(self, joueur):
        """
        Méthode abstraite. Chaque objet enfant DOIT
        implémenter cette méthode.
        """
        pass

# --- PREMIER ENFANT : NOURRITURE  (Héritage 1) ---

class Nourriture(Objet):
    """
    Représente la nourriture qui redonne des pas.
    Hérite de la classe Objet.
    """
    def __init__(self, nom: str, pas_bonus: int):
        # On appelle le constructeur de la classe Mère (Objet)
        super().__init__(nom)
        self.pas_bonus = pas_bonus

    def utiliser(self, joueur):
        """
        Implémentation de la méthode abstraite.
        Donne des pas au joueur.
        """
        # Note : On suppose que 'joueur' aura une méthode 'gagner_pas'
        # C'est le "CONTRAT" dont nous avons parlé.
        joueur.gagner_pas(self.pas_bonus)
        print(f"{joueur} utilise {self.nom} et gagne {self.pas_bonus} pas.")

# --- CRÉER DES OBJETS ---
# On crée des instances que le reste du jeu pourra utiliser
POMME = Nourriture("Pomme", 2)       # [cite: 72]
BANANE = Nourriture("Banane", 3)     # [cite: 73]
GATEAU = Nourriture("Gâteau", 10)    # [cite: 74]
SANDWICH = Nourriture("Sandwich", 15) # [cite: 75]
REPAS = Nourriture("Repas", 25)      # [cite: 76]


# --- DEUXIÈME ENFANT : OBJET PERMANENT (Héritage 2) ---

class ObjetPermanent(Objet):
    """
    Représente un objet permanent (Pelle, Marteau, etc.).
    Hérite de la classe Objet.
    """
    def __init__(self, nom: str):
        # On appelle le constructeur de la classe Mère (Objet)
        super().__init__(nom)

    def utiliser(self, joueur):
        """
        Implémentation de la méthode abstraite.
        Pour un objet permanent, "utiliser" ne fait rien
        par défaut.
        """
        print(f"L'objet {self.nom} est déjà dans l'inventaire permanent.")
        pass

# --- CRÉER DES OBJETS PERMANENTS ---
# On crée des instances que le reste du jeu pourra utiliser
PELLE = ObjetPermanent("Pelle")               # [cite: 53]
MARTEAU = ObjetPermanent("Marteau")             # [cite: 54]
KIT_CROCHETAGE = ObjetPermanent("Kit de crochetage") # [cite: 55]
DETECTEUR_METAUX = ObjetPermanent("Détecteur de métaux") # [cite: 56]
PATTE_LAPIN = ObjetPermanent("Patte de lapin")   # [cite: 57]
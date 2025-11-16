# fichier: joueur.py

# fichier: joueur.py

class Joueur:
    """
    Représente le joueur et son inventaire.
    """
    def __init__(self):
        # --- Inventaire Consommable (Section 2.1) ---
        self.pas = 70         # Initialement 70
        self.pieces_or = 0    # Initialement 0
        self.gemmes = 2       # Initialement 2
        self.cles = 0         # Initialement 0
        self.des = 0          # Initialement 0

        # --- NOUVEAU : Inventaire d'Objets ---
        # Cette liste remplacera les 'self.pelle = False', etc.
        # Elle contiendra des objets comme POMME, PELLE, MARTEAU...
        self.inventaire_objets = []

    def __str__(self):
        # AJOUT : Utile pour les messages de print
        return "Le Joueur"

    # --- Méthodes pour gérer l'inventaire ---

    def perdre_pas(self, quantite=1):
        """Fait perdre des pas au joueur."""
        self.pas -= quantite
        print(f"Pas restants : {self.pas}") # (Pour tester)

    def a_assez_pas(self):
        """Vérifie si le joueur peut encore se déplacer."""
        return self.pas > 0

    # --- AJOUTÉ : Méthodes pour le "Contrat" avec objets.py ---
    
    def gagner_pas(self, quantite):
        """
        Le "CONTRAT" pour la classe Nourriture.
        """
        self.pas += quantite
        print(f"Le Joueur gagne {quantite} pas. Total : {self.pas}")

    def ajouter_objet(self, objet):
        """Ajoute un objet (Nourriture, ObjetPermanent, etc.) à l'inventaire."""
        self.inventaire_objets.append(objet)
        print(f"{objet.nom} ajouté à l'inventaire.")

    def a_objet(self, nom_objet: str) -> bool:
        """
        Vérifie si le joueur possède un objet par son nom.
        Ex: a_objet("Pelle")
        """
        for objet in self.inventaire_objets:
            if objet.nom == nom_objet:
                return True
        return False
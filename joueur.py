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

        # --- Inventaire Permanent (Section 2.1) ---
        self.pelle = False         # 
        self.marteau = False       # 
        self.kit_crochetage = False # 
        self.detecteur_metaux = False # 
        self.patte_lapin = False    # 

    # --- Méthodes pour gérer l'inventaire ---

    def perdre_pas(self, quantite=1):
        """Fait perdre des pas au joueur."""
        self.pas -= quantite
        print(f"Pas restants : {self.pas}") # (Pour tester)

    def a_assez_pas(self):
        """Vérifie si le joueur peut encore se déplacer."""
        return self.pas > 0

# Vous ajouterez plus de méthodes ici plus tard (ex: depenser_gemmes, ajouter_cle, etc.)
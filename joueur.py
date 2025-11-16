# fichier: joueur.py

class Joueur:
    """
    Représente le joueur et son inventaire.
    Contient toutes les méthodes pour manipuler l'inventaire.
    """
    def __init__(self):
        # Inventaire Consommable (transformé en dictionnaire)
        self.consommables = {
            "pas": 70,         # [cite: 47]
            "pieces_or": 0,    # [cite: 48]
            "gemmes": 2,       # [cite: 49]
            "cles": 0,         # [cite: 50]
            "des": 0           # [cite: 51]
        }
        
        # Inventaire des objets (Nourriture, Objets Permanents)
        self.inventaire_objets = []

    def __str__(self):
        return "Le Joueur"

    # --- MÉTHODES POUR LES PAS ---
    def perdre_pas(self, quantite=1):
        self.consommables["pas"] -= quantite
        print(f"Pas restants : {self.consommables['pas']}")

    def gagner_pas(self, quantite):
        self.consommables["pas"] += quantite
        print(f"Le Joueur gagne {quantite} pas. Total : {self.consommables['pas']}")

    def a_assez_pas(self):
        return self.consommables["pas"] > 0

    # --- MÉTHODES POUR LES AUTRES CONSOMMABLES ---
    
    def _gagner_consommable(self, nom, quantite):
        """Méthode privée générique pour ajouter un consommable."""
        if nom in self.consommables:
            self.consommables[nom] += quantite
            print(f"Le Joueur gagne {quantite} {nom}. Total : {self.consommables[nom]}")
        else:
            print(f"Erreur: Consommable '{nom}' inconnu.")

    def _a_assez_consommable(self, nom, quantite_necessaire):
        """Méthode privée générique pour vérifier un consommable."""
        if nom in self.consommables:
            return self.consommables[nom] >= quantite_necessaire
        return False

    def _depenser_consommable(self, nom, quantite):
        """Méthode privée générique pour dépenser un consommable."""
        if self._a_assez_consommable(nom, quantite):
            self.consommables[nom] -= quantite
            print(f"Le Joueur dépense {quantite} {nom}. Restant : {self.consommables[nom]}")
            return True
        print(f"Pas assez de {nom} pour dépenser {quantite}.")
        return False

    # --- MÉTHODES "CONTRAT" (Publiques) POUR IDRIS ET TIANTIAN ---
    
    # Gemmes
    def gagner_gemmes(self, quantite): self._gagner_consommable("gemmes", quantite)
    def a_assez_gemmes(self, quantite): return self._a_assez_consommable("gemmes", quantite)
    def depenser_gemmes(self, quantite): return self._depenser_consommable("gemmes", quantite) # [cite: 133]

    # Clés
    def gagner_cles(self, quantite): self._gagner_consommable("cles", quantite)
    def a_assez_cles(self, quantite): return self._a_assez_consommable("cles", quantite)
    def depenser_cle(self, quantite=1): return self._depenser_consommable("cles", quantite) # [cite: 121]

    # Dés
    def gagner_des(self, quantite): self._gagner_consommable("des", quantite)
    def a_assez_des(self, quantite): return self._a_assez_consommable("des", quantite)
    def depenser_de(self, quantite=1): return self._depenser_consommable("des", quantite) # [cite: 131]

    # Or (pour Syscom)
    def gagner_or(self, quantite): self._gagner_consommable("pieces_or", quantite)
    def a_assez_or(self, quantite): return self._a_assez_consommable("pieces_or", quantite)
    def depenser_or(self, quantite): return self._depenser_consommable("pieces_or", quantite) # [cite: 173]

    # --- MÉTHODES POUR LES OBJETS (Inventaire) ---

    def ajouter_objet(self, objet):
        """Ajoute un objet (Nourriture, ObjetPermanent, etc.) à l'inventaire."""
        self.inventaire_objets.append(objet)
        print(f"{objet.nom} ajouté à l'inventaire.")

    def a_objet(self, nom_objet: str) -> bool:

        """
        Vérifie si le joueur possède un objet par son nom.
        Ex: a_objet("Pelle") [cite: 53] ou a_objet("Kit de crochetage") [cite: 55]
        """
        for objet in self.inventaire_objets:
            if objet.nom == nom_objet:
                return True
        return False
    
    # --- MÉTHODES POUR LES "EFFETS ASSOCIÉS" (Tableau 1) ---

    def get_modificateur_chance_objet(self) -> float:
        """
        Renvoie le multiplicateur de chance pour trouver des objets.
        (Pour la Patte de lapin)
        """
        if self.a_objet("Patte de lapin"):
            # L'effet de la patte de lapin (ex: +30% de chance)
            return 1.3  
        
        # Pas d'objet, pas de modification
        return 1.0

    def get_modificateur_chance_metal(self) -> float:
        """
        Renvoie le multiplicateur de chance pour trouver des clés/pièces.
        (Pour le Détecteur de métaux)
        """
        if self.a_objet("Détecteur de métaux"):
            # L'effet du détecteur (ex: +50% de chance)
            return 1.5
        
        # Pas d'objet, pas de modification
        return 1.0
    

    # --- MÉTHODES "CONTRAT" DE HAUT NIVEAU (Pour Idris) ---faciliter la lecture quant tu commende

    def peut_creuser(self) -> bool:
        """
        Vérifie si le joueur a l'objet nécessaire pour creuser.
        (Requis pour Tableau 2)
        """
        return self.a_objet("Pelle") # [cite: 53]

    def peut_ouvrir_coffre(self) -> bool:
        """
        Vérifie si le joueur a UN moyen d'ouvrir un coffre.
        (Requis pour Tableau 2)
        """
        # Peut ouvrir avec une clé [cite: 77] OU un marteau [cite: 54, 77]
        return self.a_assez_cles(1) or self.a_objet("Marteau")

    def peut_ouvrir_porte(self, niveau_porte: int) -> bool:
        """
        Vérifie si le joueur a UN moyen d'ouvrir une porte
        d'un certain niveau.
        (Requis pour Tableau 1)
        """
        if niveau_porte == 0:
            return True # Les portes de niveau 0 sont toujours ouvertes [cite: 122]
        
        if niveau_porte == 1:
            # Niveau 1 : Clé [cite: 124] OU Kit de crochetage 
            return self.a_assez_cles(1) or self.a_objet("Kit de crochetage")
        
        if niveau_porte == 2:
            # Niveau 2 : Clé uniquement [cite: 124, 126]
            return self.a_assez_cles(1)
        
        return False # Niveaux inconnus
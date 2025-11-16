# fichier: main.py
# (Implémentation du Moteur de Jeu, par Abdelrahman)

import pygame
import sys
import random 

# --- IMPORT DES MODULES DE L'ÉQUIPE ---
from joueur import Joueur
from room_defs import build_initial_deck, RoomTemplate
from grille import Grille
from room_defs import build_initial_deck, RoomTemplate, ANTECHAMBER_TEMPLATE 
# --- INITIALISATION PYGAME ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blue Prince - Moteur de Jeu")
clock = pygame.time.Clock()
BLACK, WHITE, GREY = (0, 0, 0), (255, 255, 255), (30, 30, 30)
font = pygame.font.SysFont(None, 24)

class Jeu:
    """
    Classe principale (Game Manager).
    Connecte le Joueur, la Grille et les Pièces.
    """
    def __init__(self):
        self.joueur = Joueur() # Module d'Abdelrahman
        self.grille = Grille(5, 9) # Module Grille
        
        self.pioche = build_initial_deck() # Module de Tiantian
        print(f"{len(self.pioche)} pièces chargées dans la pioche.")
         # Définir la taille des cases et charger les images ---
        self.taille_case = 60
        self.room_images = self.charger_images_pieces() 
        # -----------------------------------------------------------
        # Placer la pièce de départ
        piece_depart = self.pioche.pop(0) 
        self.grille.placer_piece(piece_depart, self.grille.joueur_x, self.grille.joueur_y)
        # 2. Pièce de VICTOIRE (en haut au milieu)
        self.win_x, self.win_y = 0, 4 # Ligne 0, Colonne 4
        self.grille.placer_piece(ANTECHAMBER_TEMPLATE, self.win_x, self.win_y)
        # Gérer l'état du jeu (crucial)
        self.etat = "deplacement" # Peut être "deplacement" ou "tirage"
        self.choix_tirage = [] # Va stocker les 3 pièces proposées
        self.selection_choix = 0 # Index du choix (0, 1, ou 2)
        self.destination_tirage = None # Coords (x, y) de la nouvelle pièce
        self.jeu_gagne = False

        # Collecter les objets de la pièce de départ
        self.collecter_objets_et_effets(piece_depart)

    def run(self):
        """Boucle de jeu principale."""
        running = True
        # La boucle s'arrête si on quitte, si on n'a plus de pas, OU si on a gagné
        while running and self.joueur.a_assez_pas() and not self.jeu_gagne:
            
            # 1. Gérer les événements (clavier)
            self.gerer_evenements()

            # 2. Dessiner le jeu
            self.dessiner()

            pygame.display.flip()
            clock.tick(60)
        
        # --- Boucle terminée, afficher l'écran de fin ---
        if self.jeu_gagne:
            self.afficher_ecran_fin("VOUS AVEZ GAGNÉ !")
        elif not self.joueur.a_assez_pas():
            self.afficher_ecran_fin("GAME OVER - Plus de pas")
        
        pygame.quit()
        sys.exit()

    def gerer_evenements(self):
        """Gère les inputs du joueur en fonction de l'état du jeu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # --- Si on est en mode DÉPLACEMENT ---
                if self.etat == "deplacement":
                    if event.key == pygame.K_z: # Haut
                        self.tenter_deplacement(dx=-1, dy=0)
                    if event.key == pygame.K_s: # Bas
                        self.tenter_deplacement(dx=1, dy=0)
                    if event.key == pygame.K_q: # Gauche
                        self.tenter_deplacement(dx=0, dy=-1)
                    if event.key == pygame.K_d: # Droite
                        self.tenter_deplacement(dx=0, dy=1)
                        # --- AJOUT POUR L'INTERACTION (Touche E) ---
                    if event.key == pygame.K_e:
                        self.interagir_avec_piece()
                
                # --- Si on est en mode TIRAGE DE PIÈCE ---
                elif self.etat == "tirage":
                    if event.key == pygame.K_q: # Choix Gauche
                        self.selection_choix = max(0, self.selection_choix - 1)
                    if event.key == pygame.K_d: # Choix Droite
                        self.selection_choix = min(len(self.choix_tirage) - 1, self.selection_choix + 1)
                    if event.key == pygame.K_RETURN: # Valider
                        self.valider_choix_piece()
                        # --- AJOUT POUR LES DÉS (Touche R) ---
                    if event.key == pygame.K_r: #
                        # On vérifie et dépense un dé (APPEL À VOTRE CODE)
                        if self.joueur.depenser_de(1): #
                            print("Relance du tirage !")
                            self.lancer_tirage() # On relance
                        else:
                            print("Pas assez de dés pour relancer.")



    def tenter_deplacement(self, dx, dy):
        """
        Logique de déplacement (Section 2.5).
        MISE À JOUR AVEC LA DIFFICULTÉ CROISSANTE (Section 2.8)
        """
        
        x_actuel, y_actuel = self.grille.joueur_x, self.grille.joueur_y
        new_x, new_y = x_actuel + dx, y_actuel + dy
        
        # 1. Vérifier si on est dans les limites
        if not (0 <= new_x < self.grille.rows and 0 <= new_y < self.grille.cols):
            print("Déplacement hors limites.")
            return

        # 2. Regarder la pièce de destination
        piece_destination = self.grille.get_piece(new_x, new_y)

        # 3. Si la pièce est DÉJÀ DÉCOUVERTE
        if piece_destination:
            
            # --- VÉRIFICATION DE VICTOIRE ---
            if new_x == self.win_x and new_y == self.win_y:
                print("VICTOIRE ATTEINTE !")
                self.jeu_gagne = True
                return # On arrête tout
            
            # Si ce n'est pas la victoire, on continue
            self.grille.joueur_x, self.grille.joueur_y = new_x, new_y
            self.joueur.perdre_pas(1) 
            print(f"Entrée dans {piece_destination.name}")
            self.collecter_objets_et_effets(piece_destination)

        # 4. Si la pièce est NOUVELLE (Porte fermée)
        else:
            print("Porte vers une pièce inconnue !")
            
            # --- NOUVELLE LOGIQUE DE PORTE (Section 2.8) ---
            # La difficulté dépend de la ligne (new_x)
            # Row 4 (départ) -> Nv 0
            # Row 3 -> 50% Nv 0, 50% Nv 1
            # Row 2 -> 33% Nv 0, 66% Nv 1
            # Row 1 -> 50% Nv 1, 50% Nv 2
            # Row 0 (fin) -> Nv 2
            
            niveau_porte = 0 # Par défaut
            if new_x == 4: # Rangée de départ
                niveau_porte = 0
            elif new_x == 3:
                niveau_porte = random.choice([0, 1])
            elif new_x == 2:
                niveau_porte = random.choice([0, 1, 1])
            elif new_x == 1:
                niveau_porte = random.choice([1, 1, 2])
            elif new_x == 0: # Rangée de la victoire
                niveau_porte = 2
            
            print(f"La porte vers la ligne {new_x} est de niveau {niveau_porte}.")

            # On vérifie si le joueur peut l'ouvrir (APPEL À VOTRE CODE)
            if self.joueur.peut_ouvrir_porte(niveau_porte): #
                print("Le joueur peut ouvrir la porte.")
                
                # On dépense une clé si nécessaire (APPEL À VOTRE CODE)
                if niveau_porte == 1 and not self.joueur.a_objet("Kit de crochetage"):
                    self.joueur.depenser_cle(1)
                elif niveau_porte == 2:
                    self.joueur.depenser_cle(1)
                
                # Lancer le tirage
                self.etat = "tirage"
                self.destination_tirage = (new_x, new_y)
                self.lancer_tirage()
                
            else:
                # Le joueur est bloqué
                print("Porte verrouillée ! Vous n'avez pas la clé ou le kit.")
                # (Le joueur ne bouge pas, ne perd pas de pas)
    def collecter_objets_et_effets(self, piece: RoomTemplate):
        """
        Ramasse les objets et applique les effets de la pièce.
        (Connexion entre le code de Tiantian et le vôtre)
        """
        # 1. Collecter les objets (clés, gemmes, or) 
        if "gem" in piece.items:
            qte = piece.items.pop("gem")
            self.joueur.gagner_gemmes(qte) # APPEL À VOTRE CODE
        if "coin" in piece.items:
            qte = piece.items.pop("coin")
            self.joueur.gagner_or(qte) # APPEL À VOTRE CODE
        # --- AJOUT POUR LES DÉS ---
        if "dice" in piece.items:
            qte = piece.items.pop("dice")
            self.joueur.gagner_des(qte) # APPEL À VOTRE CODE
        
        
        # 2. Appliquer les effets (exemples simples)
        if piece.effect == "restore_steps": # [cite: 100]
            self.joueur.gagner_pas(5) # Gagner 5 pas
            piece.effect = None # Effet appliqué une seule fois
        if piece.effect == "trap": # [cite: 102]
            self.joueur.perdre_pas(5) # Perdre 5 pas
            piece.effect = None

    def lancer_tirage(self):
        """Section 2.7 - Tirer 3 pièces dans la pioche."""
        self.choix_tirage = []
        
        # Simplification (on ne vérifie pas les contraintes, juste la rareté et coût 0)
        
        # 1. Assurer au moins une pièce à 0 gemme [cite: 130]
        pioche_0_gemme = [p for p in self.pioche if p.cost_gems == 0]
        if pioche_0_gemme:
            self.choix_tirage.append(random.choice(pioche_0_gemme))
        else:
            # Sécurité (si la pioche est vide de 0 gemmes)
            self.choix_tirage.append(random.choice(self.pioche))

        # 2. Ajouter 2 autres pièces (elles peuvent aussi être à 0)
        while len(self.choix_tirage) < 3 and len(self.pioche) > 0:
            self.choix_tirage.append(random.choice(self.pioche))
            
        self.selection_choix = 0
        print(f"Tirage: {[p.name for p in self.choix_tirage]}")

    def valider_choix_piece(self):
        """Le joueur appuie sur Entrée pour choisir une pièce."""
        if not self.choix_tirage:
            return

        piece_choisie = self.choix_tirage[self.selection_choix]
        cout = piece_choisie.cost_gems
        
        # Vérifier si le joueur a assez de gemmes (APPEL À VOTRE CODE)
        if self.joueur.a_assez_gemmes(cout): # [cite: 133]
            # Dépenser les gemmes (APPEL À VOTRE CODE)
            self.joueur.depenser_gemmes(cout) # [cite: 133]
            
            # Placer la pièce
            x, y = self.destination_tirage
            self.grille.placer_piece(piece_choisie, x, y) # [cite: 134]
            
            # La retirer de la pioche [cite: 93]
            if piece_choisie in self.pioche:
                self.pioche.remove(piece_choisie)
            
            # Revenir au mode déplacement
            self.etat = "deplacement"
            self.choix_tirage = []
            
            # Entrer dans la nouvelle pièce et bouger le joueur
            self.grille.joueur_x, self.grille.joueur_y = x, y
            self.joueur.perdre_pas(1) # Perdre le pas pour le déplacement
            self.collecter_objets_et_effets(piece_choisie)
            
        else:
            print(f"Pas assez de gemmes pour {piece_choisie.name} (coûte {cout})")
            # (On reste en mode "tirage")

            # ... (dans main.py, dans la classe Jeu) ...

    def afficher_ecran_fin(self, message):
        """Affiche un simple écran de fin."""
        print(message) # Pour le terminal
        
        screen.fill(BLACK)
        txt = font.render(message, True, WHITE)
        txt_rect = txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(txt, txt_rect)
        pygame.display.flip()
        
        # Attendre 3 secondes avant de quitter
        pygame.time.wait(3000)

        
  # ... (dans la classe Jeu) ...

    def dessiner(self):
        """Dessine l'état du jeu (Grille, UI, Tirage)."""
        screen.fill(BLACK)
        
        # 1. Dessiner la grille
        for x in range(self.grille.rows):
            for y in range(self.grille.cols):
                rect = pygame.Rect(y * self.taille_case + 50, x * self.taille_case + 50, self.taille_case - 2, self.taille_case - 2)
                
                piece = self.grille.get_piece(x, y)
                
                # --- CORRECTION : Dessiner les images ---
                if piece:
                    # On essaie de dessiner l'image
                    image_a_dessiner = self.room_images.get(piece.name)
                    
                    if image_a_dessiner:
                        # Si on a l'image, on la "blitte"
                        screen.blit(image_a_dessiner, rect.topleft)
                    else:
                        # SINON, on utilise l'ancienne méthode (carrés de couleur)
                        color_map = {
                            "green": (0, 100, 0), "yellow": (200, 200, 0),
                            "blue": (50, 50, 150), "red": (100, 0, 0),
                            "purple": (100, 0, 100), "orange": (200, 100, 0)
                        }
                        pygame.draw.rect(screen, color_map.get(piece.color, WHITE), rect)
                else:
                    # Pièce inconnue
                    pygame.draw.rect(screen, GREY, rect)
                # --- FIN DE LA CORRECTION ---
                    
                # Dessiner le joueur
                if x == self.grille.joueur_x and y == self.grille.joueur_y:
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, 10)

        # 2. Dessiner l'UI (VOTRE CODE)
        txt_pas = font.render(f"Pas: {self.joueur.consommables['pas']}", True, WHITE)
        screen.blit(txt_pas, (600, 50))
        txt_cles = font.render(f"Clés: {self.joueur.consommables['cles']}", True, WHITE)
        screen.blit(txt_cles, (600, 80))
        txt_gemmes = font.render(f"Gemmes: {self.joueur.consommables['gemmes']}", True, WHITE)
        screen.blit(txt_gemmes, (600, 110))
        txt_or = font.render(f"Or: {self.joueur.consommables['pieces_or']}", True, WHITE)
        screen.blit(txt_or, (600, 140))
        txt_des = font.render(f"Dés: {self.joueur.consommables['des']}", True, WHITE)
        screen.blit(txt_des, (600, 170)) 
        
        # 3. Dessiner l'écran de TIRAGE
        if self.etat == "tirage":
            pygame.draw.rect(screen, (10, 10, 10), (0, 400, 800, 200)) # Fond
            for i, piece in enumerate(self.choix_tirage):
                x_pos = 100 + i * 220
                box_rect = pygame.Rect(x_pos, 420, 200, 160)
                
                # Dessiner le cadre de sélection
                if i == self.selection_choix:
                    pygame.draw.rect(screen, WHITE, box_rect, 3)
                else:
                    pygame.draw.rect(screen, GREY, box_rect, 1)

                # --- CORRECTION : Dessiner l'image de la pièce ---
                image_a_dessiner = self.room_images.get(piece.name)
                
                if image_a_dessiner:
                    # On redimensionne l'image pour qu'elle rentre dans la boîte
                    img_scaled = pygame.transform.scale(image_a_dessiner, (180, 100)) # Nouvelle taille
                    img_rect = img_scaled.get_rect(centerx=box_rect.centerx, top=box_rect.top + 10)
                    screen.blit(img_scaled, img_rect)
                else:
                    # Fallback si l'image n'est pas trouvée
                    txt_nom = font.render(piece.name, True, WHITE)
                    screen.blit(txt_nom, (x_pos + 10, 430))
                
                # Infos (plus bas pour laisser la place à l'image)
                txt_cout = font.render(f"Coût: {piece.cost_gems} gemmes", True, WHITE)
                screen.blit(txt_cout, (x_pos + 10, box_rect.bottom - 45))
                txt_rarete = font.render(f"Rareté: {piece.rarity}", True, WHITE)
                screen.blit(txt_rarete, (x_pos + 10, box_rect.bottom - 25))

        # 4. Dessiner les Interactables
        if self.etat == "deplacement":
            piece = self.grille.get_piece(self.grille.joueur_x, self.grille.joueur_y)
            if piece and piece.interactables:
                interact_txt = f"Appuyez sur [E] pour interagir avec: {piece.interactables[0]}"
                txt = font.render(interact_txt, True, WHITE)
                txt_rect = txt.get_rect(center=(SCREEN_WIDTH // 2, 550))
                pygame.draw.rect(screen, BLACK, txt_rect.inflate(20, 10))
                screen.blit(txt, txt_rect)

    def interagir_avec_piece(self):
        """
        Gère l'interaction avec les objets de la pièce (Pelle, Marteau).
        (Fonctionnalité Syscom - Tableau 2)
        """
        piece = self.grille.get_piece(self.grille.joueur_x, self.grille.joueur_y)
        if not piece or not piece.interactables:
            print("Il n'y a rien avec quoi interagir ici.")
            return

        interactable = piece.interactables[0] # On prend le premier

        # 1. Logique pour CREUSER (APPEL À VOTRE CODE)
        if interactable == "dig_spot":
            if self.joueur.peut_creuser(): #
                print("Le joueur utilise la Pelle !")
                # Donner une récompense aléatoire
                self.joueur.gagner_or(random.randint(5, 15))
                piece.interactables.pop(0) # Retirer l'objet
            else:
                print("Il y a un endroit où creuser, mais vous n'avez pas de pelle.")
        
        # 2. Logique pour COFFRE (APPEL À VOTRE CODE)
        elif interactable == "chest":
            if self.joueur.peut_ouvrir_coffre(): #
                print("Le joueur ouvre le coffre !")
                
                # Dépenser une clé SI on n'a pas le marteau
                if not self.joueur.a_objet("Marteau"):
                    self.joueur.depenser_cle(1)
                
                # Donner une récompense aléatoire
                self.joueur.gagner_cles(random.randint(0, 2))
                self.joueur.gagner_gemmes(random.randint(0, 1))
                piece.interactables.pop(0) # Retirer l'objet
            else:
                print("Il y a un coffre, mais il vous faut une clé ou un marteau.")


    def charger_images_pieces(self):
        """
        Charge toutes les images des pièces depuis le dossier /assets.
        """
        print("Chargement des images des pièces...")
        images = {}
        
        # On doit importer 'build_templates'
        from room_defs import build_templates, ANTECHAMBER_TEMPLATE
        
        # On récupère tous les noms de pièces possibles
        tous_templates = build_templates()
        tous_templates.append(ANTECHAMBER_TEMPLATE) # Ne pas oublier la pièce de victoire
        noms_uniques = set(tpl.name for tpl in tous_templates)
        
        for name in noms_uniques:
            # Le chemin est "assets/Nom De La Piece.png"
            path = f"assets/{name}.png"
            try:
                img = pygame.image.load(path)
                # On redimensionne l'image à la taille de nos cases
                img_scaled = pygame.transform.scale(img, (self.taille_case - 2, self.taille_case - 2))
                images[name] = img_scaled
            except FileNotFoundError:
                # Si l'image n'est pas trouvée, on affichera une couleur
                print(f"AVERTISSEMENT: Image non trouvée pour '{name}'.")
                images[name] = None
        
        return images
# --- Point d'entrée ---
if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()
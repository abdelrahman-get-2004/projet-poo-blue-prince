# fichier: main.py
# (Ce fichier était la responsabilité d'Idris)

import pygame
import sys

# --- IMPORT DES MODULES DE L'ÉQUIPE ---pour regrouper le trravail 

from joueur import Joueur
from room_defs import build_initial_deck, RoomTemplate
from grille import Grille

# --- INITIALISATION PYGAME ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blue Prince - Moteur de Jeu")
clock = pygame.time.Clock()
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
font = pygame.font.SysFont(None, 24)

class Jeu:
    """
    Classe principale (Game Manager).
    Connecte le Joueur, la Grille et les Pièces.
    """
    def __init__(self):
        self.joueur = Joueur() # Module d'Abdelrahman
        self.grille = Grille(5, 9) # Module Grille
        
        # Module de Tiantian
        self.pioche = build_initial_deck()
        print(f"{len(self.pioche)} pièces chargées dans la pioche.")
        
        # Placer la pièce de départ (ex: Hall)
        piece_depart = self.pioche.pop(0) # On prend la 1ère pièce
        self.grille.placer_piece(piece_depart, self.grille.joueur_x, self.grille.joueur_y)

    def run(self):
        """Boucle de jeu principale."""
        running = True
        while running and self.joueur.a_assez_pas():
            
            # 1. Gérer les événements (clavier)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Gérer ZQSD (Déplacement)
                    if event.key == pygame.K_z: # Haut
                        self.tenter_deplacement(dx=-1, dy=0)
                    if event.key == pygame.K_s: # Bas
                        self.tenter_deplacement(dx=1, dy=0)
                    if event.key == pygame.K_q: # Gauche
                        self.tenter_deplacement(dx=0, dy=-1)
                    if event.key == pygame.K_d: # Droite
                        self.tenter_deplacement(dx=0, dy=1)

            # 2. Mettre à jour la logique (à venir)
            # ...

            # 3. Dessiner le jeu
            self.dessiner()

            # Mettre à jour l'écran
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()
        sys.exit()

    def tenter_deplacement(self, dx, dy):
        """
        Logique de déplacement (Section 2.5).
        C'est ici que vous connectez tout !
        """
        # 1. Tenter le mouvement sur la grille
        if self.grille.deplacer_joueur(dx, dy):
            # 2. Si réussi, perdre 1 pas (APPEL À VOTRE CODE)
            self.joueur.perdre_pas(1) # [cite: 47]
            
            # 3. Logique d'entrée dans la pièce (à faire)
            piece_actuelle = self.grille.get_piece(self.grille.joueur_x, self.grille.joueur_y)
            
            if piece_actuelle is None:
                # C'est une nouvelle pièce !
                print("Porte vers une pièce inconnue !")
                # (Ici, il faudra appeler le "Tirage de pièce" [Section 2.7])
            else:
                # Pièce déjà découverte
                print(f"Entrée dans {piece_actuelle.name}")
                # (Ici, il faudra gérer les effets)

    def dessiner(self):
        """Dessine l'état du jeu (Grille, UI)."""
        screen.fill(BLACK)
        
        # Dessiner la grille
        taille_case = 60
        for x in range(self.grille.rows):
            for y in range(self.grille.cols):
                rect = pygame.Rect(y * taille_case + 50, x * taille_case + 50, taille_case - 2, taille_case - 2)
                
                piece = self.grille.get_piece(x, y)
                if piece:
                    # Pièce découverte (on utilise le 'color' de Tiantian)
                    if piece.color == "green":
                        pygame.draw.rect(screen, (0, 100, 0), rect)
                    elif piece.color == "yellow":
                        pygame.draw.rect(screen, (200, 200, 0), rect)
                    else:
                        pygame.draw.rect(screen, (50, 50, 150), rect)
                else:
                    # Pièce inconnue
                    pygame.draw.rect(screen, (30, 30, 30), rect)
                    
                # Dessiner le joueur
                if x == self.grille.joueur_x and y == self.grille.joueur_y:
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, 10)

        # Dessiner l'UI (APPEL À VOTRE CODE)
        txt_pas = font.render(f"Pas: {self.joueur.consommables['pas']}", True, WHITE)
        screen.blit(txt_pas, (650, 50))
        txt_cles = font.render(f"Clés: {self.joueur.consommables['cles']}", True, WHITE)
        screen.blit(txt_cles, (650, 80))
        txt_gemmes = font.render(f"Gemmes: {self.joueur.consommables['gemmes']}", True, WHITE)
        screen.blit(txt_gemmes, (650, 110))

# --- Point d'entrée ---
if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()
import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Constantes de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Blue Prince (Projet POO)"

# Couleurs
BLACK = (0, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Horloge pour contrôler la vitesse de rafraîchissement
clock = pygame.time.Clock()

# --- Boucle de jeu principale ---
running = True
while running:
    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Exemple de gestion de touche (on pourra l'utiliser pour ZQSD)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Appuyer sur Echap pour quitter
                running = False

    # --- Logique du jeu (à venir) ---
    # ...

    # --- Dessin (Drawing) ---
    screen.fill(BLACK) # Remplir l'écran en noir

    # --- Mettre à jour l'écran ---
    pygame.display.flip()

    # Limiter à 60 images par seconde (FPS)
    clock.tick(60)

# --- Fin du jeu ---
pygame.quit()
sys.exit()
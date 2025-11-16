import pygame
import sys
from joueur import Joueur

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
# --- Créer les objets du jeu ---
joueur_principal = Joueur()

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

            #test de pas un clic = 1 pas
            if event.key == pygame.K_SPACE:
                joueur_principal.perdre_pas(1)
    # --- Logique du jeu (à venir) ---
    # ...

    # --- Dessin (Drawing) ---
    screen.fill(BLACK) # Remplir l'écran en noir

    # --- Mettre à jour l'écran ---
    pygame.display.flip()

    # Limiter à 60 images par seconde (FPS)
    clock.tick(60)

# ... (à la fin de la boucle 'while running:', avant pygame.quit())

# --- TEST D'ABDELRAHMAN ---
# On simule le fonctionnement de vos classes
print("--- DÉBUT DU TEST D'OBJETS ---")
from joueur import Joueur
from objets import POMME # On importe l'instance de la Pomme

# 1. Créer un joueur
test_joueur = Joueur()
print(f"Pas initiaux : {test_joueur.pas}") # Devrait être 70

# 2. Simuler la trouvaille d'une pomme
test_joueur.ajouter_objet(POMME)

# 3. Simuler l'utilisation de la pomme
# On prend le premier objet de l'inventaire et on l'utilise
objet_a_utiliser = test_joueur.inventaire_objets.pop(0) # On retire de l'inventaire
objet_a_utiliser.utiliser(test_joueur) # On l'utilise

print(f"Pas finaux : {test_joueur.pas}") # Devrait être 72
print("--- FIN DU TEST D'OBJETS ---")

# --- Fin du jeu ---
pygame.quit()
sys.exit()
# --- Fin du jeu ---
pygame.quit()
sys.exit()
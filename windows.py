import pygame
import sys


# Initialisation de Pygame
pygame.init()


font_path = "Ressources/Sevastopol-Interface.ttf"


# Définir les couleurs
GREEN = (0,190,99)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

text_color = GREEN


class StartPage:
    def __init__(self, screen):
        self.screen = screen
        self.is_start_pressed = False
        self.font = pygame.font.Font(font_path, 36)
        self.start_text_base = "Appuyez sur Entrée pour démarrer"
        self.start_text_rect = None
        self.animation_frame = 0
        self.animation_delay = 20
        self.update_text()

    def update_text(self):
        dots = "." * (self.animation_frame // self.animation_delay % 4)
        self.start_text = self.font.render(self.start_text_base + dots, True, text_color)
        self.start_text_rect = self.start_text.get_rect(
            bottomright=(self.screen.get_rect().bottomright[0] - 30,
                         self.screen.get_rect().bottomright[1] - 30)
        )

    def update(self):
        self.animation_frame += 1
        self.update_text()

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.start_text, self.start_text_rect)
        pygame.display.flip()

# Créer la classe de la deuxième fenêtre (faux temps de chargement)
class LoadingWindow:
    def __init__(self, screen):
        self.screen = screen
        self.is_loading_complete = False
        self.loading_bar_images = [pygame.image.load(f"Ressources/LoadingBars/LoadinBar{i:02d}.png") for i in range(16)]
        self.loading_bar_index = 0

    def update(self):
        index = 0
        while index < 10000000:
            index += 1
        if not self.is_loading_complete:
            self.loading_bar_index += 1
            if self.loading_bar_index >= len(self.loading_bar_images):
                self.is_loading_complete = True

    def draw(self):
        self.screen.fill(BLACK)

        # Dessiner la barre de chargement au centre de l'écran
        if self.loading_bar_index < len(self.loading_bar_images):
            loading_bar_image = self.loading_bar_images[self.loading_bar_index]
            bar_rect = loading_bar_image.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(loading_bar_image, bar_rect)

        pygame.display.flip()

class LoginPage:
    def __init__(self, screen):
        self.screen = screen

        # Couleurs
        self.is_login_complete = False
        self.is_login_failed = False
        self.text_color = (0, 0, 0)
        self.input_box_color = (200, 200, 200)

        # Police
        self.welcome_font = pygame.font.Font(font_path, 48)
        self.font = pygame.font.Font(font_path, 36)


        # Entrées
        self.password = ""

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.password == "mot_de_passe":
                        self.is_login_complete = True
                        print("Login successful")
                    else:
                        self.is_login_failed = True
                        print("Login failed")
                elif event.key == pygame.K_BACKSPACE:
                    # Gestion de la suppression
                    self.password = self.password[:-1]
                elif event.unicode:  # Vérifier si le caractère unicode est disponible
                    char = event.unicode
                    self.password += char
                    print(self.password)


    def update(self):
        if self.is_login_complete:
            # Vous pouvez ajouter ici la logique pour traiter les informations de connexion
            print("Password entered:", self.password)

    def draw(self):
        self.screen.fill(BLACK)

        welcome_message = "Bienvenue Professeur Lamindanlésak"
        # Affichage du message de bienvenue
        text_surface = self.welcome_font.render(welcome_message, True, text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() * 0.3))
        self.screen.blit(text_surface, text_rect)






        # Calcul de la position centrée de l'entrée du mot de passe
        input_box_x = (self.screen.get_width() - 240) // 2
        input_box_y = int(self.screen.get_height() * 0.55)

        # Dimensions ajustées
        input_box_width = 280
        input_box_height = 50

        # Couleurs
        border_color = GREEN  # Vert pour les bordures
        inside_color = BLACK

        # Affichage du champ de mot de passe
        pygame.draw.rect(self.screen, border_color, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(self.screen, inside_color, (
        input_box_x + 2, input_box_y + 2, input_box_width - 4, input_box_height - 4))  # Intérieur en noir

        #pygame.draw.rect(self.screen, text_color, (input_box_x + input_box_width, input_box_y, 2, 30))
        if self.is_login_failed:
            text_surface = self.font.render("Mot de passe incorrect", True, (255, 0, 0))
            self.screen.blit(text_surface, (input_box_x - 170, input_box_y + 60))

        # Affichage du texte "Mot de Passe :" à gauche de l'entrée
        text_surface = self.font.render("Mot de Passe :", True, text_color)
        self.screen.blit(text_surface, (input_box_x - 170, input_box_y+8))

        # Affichage du mot de passe masqué
        password_text_surface = self.font.render(self.password, True, text_color)
        self.screen.blit(password_text_surface, (input_box_x + 10, input_box_y + 10))

        pygame.display.flip()

class CongratulationPage:
    def __init__(self, screen):
        self.screen = screen
        self.is_running = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        pass

    def draw(self):
        pass
    def drawtime(self,minuteurtext):
        self.screen.fill(BLACK)

        # Affichage du texte de félicitations au centre de l'écran
        text_surface = pygame.font.Font(font_path, 80).render("VICTOIRE !", True, text_color)
        # Centré en haut de l'écran
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 300))
        self.screen.blit(text_surface, text_rect)

        #affichage "votre temps restant" au centre de l'écran
        text_surface = pygame.font.Font(font_path, 80).render("Vous avez mis " + minuteurtext+" minutes pour résoudre l’énigme", True, text_color)
        # Centré en haut de l'écran
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 500))
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
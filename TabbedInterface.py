import textwrap

import pygame
import sys


# Initialisation de Pygame
pygame.init()

font_path = "Ressources/Sevastopol-Interface.ttf"

# Définir les couleurs
GREEN = (0,190,99)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)




RED = (255, 0, 0)

class TabbedInterface:
    def __init__(self, screen):
        self.screen = screen
        self.current_tab = 0  # Indice de l'onglet actuel
        self.tab_images = self.load_tab_images()  # 5 images pour les onglets
        self.tab_sprites = self.get_tab_sprites()  # 5 sprites pour les onglets
        self.tab_content = [Onglet1(), Onglet2(), Onglet3(), Onglet4(), Onglet5()]  # Contenu de chaque onglet
        self.is_running = True

        self.tab_rect = self.get_tab_content_space()  # Rectangle du contenu des onglets



    # Importer les images des onglets
    def load_tab_images(self):
        # Charger les images pour chaque onglet
        tab_images = []
        for i in range(3):
            image_path = f"Ressources/Onglet/tab_image_{i}.png"
            image = pygame.image.load(image_path)
            if i == 0:
                for j in range(2):
                    tab_images.append(image)
            tab_images.append(image)
        return tab_images

    # Mettre les images sous forme de sprites
    def get_tab_sprites(self):
        tab_sprites = pygame.sprite.Group()

        # Calculer la position de départ pour centrer les onglets verticalement
        total_height = len(self.tab_images) * (self.screen.get_height() // 6 + 10) - 10
        start_y = (self.screen.get_height() - total_height) // 2

        for i, image in enumerate(self.tab_images):
            # Redimensionner l'image en fonction de la hauteur de l'écran
            tab_height = self.screen.get_height() // 6
            image = pygame.transform.scale(image, (tab_height, tab_height))

            tab_sprite = pygame.sprite.Sprite()
            tab_sprite.image = image
            tab_sprite.rect = image.get_rect()
            tab_sprite.rect.x = 10
            tab_sprite.rect.y = start_y + i * (tab_height + 10)
            tab_sprites.add(tab_sprite)

        return tab_sprites

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, tab_sprite in enumerate(self.tab_sprites):
                        if tab_sprite.rect.collidepoint(event.pos):
                            self.current_tab = i
                            print("Tab changed to", self.current_tab)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        # Afficher les onglets en une colonne à gauche
        self.tab_sprites.draw(self.screen)

        # Calculer la position de la barre verte
        line_x = self.tab_sprites.sprites()[-1].rect.right + 20
        line_rect = pygame.Rect(line_x, 0, 2, self.screen.get_height())

        # Dessiner la ligne verte à droite des onglets
        pygame.draw.rect(self.screen, GREEN, line_rect)

        # Passer tab_rect à la méthode draw de l'onglet actuel
        self.tab_content[self.current_tab].draw(self.screen.subsurface(self.tab_rect))

        # Afficher le contenu de l'onglet actuel à droite
        #self.tab_content[self.current_tab].draw(self.screen)

    def get_tab_content_space(self):
        # Marge en pourcentage de la taille de l'écran
        margin_percentage = 0.03  # 2% de marge

        # Calculer la taille de la marge en pixels
        margin_x = int(self.screen.get_width() * margin_percentage)
        margin_y = int(self.screen.get_height() * margin_percentage)

        # Calculer la position et la taille de la zone pour le contenu de l'onglet actuel avec marge
        tab_width = self.screen.get_width() - self.tab_sprites.sprites()[-1].rect.right - 2 * margin_x
        tab_x = self.tab_sprites.sprites()[-1].rect.right + margin_x
        tab_rect = pygame.Rect(tab_x, margin_y, tab_width, self.screen.get_height() - 2 * margin_y)

        # Dessiner les lignes rouges pour délimiter la zone de l'onglet actuel avec marge
        # pygame.draw.lines(self.screen, RED, False, [(tab_x, margin_y), (tab_x, self.screen.get_height() - margin_y)], 2)
        # pygame.draw.lines(self.screen, RED, False, [(tab_x + tab_width, margin_y), (tab_x + tab_width, self.screen.get_height() - margin_y)], 2)

        return tab_rect



class Onglet1:
    def draw(self, onglet_screen):
        screen_width, screen_height = onglet_screen.get_size()
        rightside = int(screen_width * 0.02)

        # Titre de l'onglet
        font_title = pygame.font.Font(font_path, int(screen_height * 0.14))  # Taille relative pour le titre
        title_text = font_title.render("L’art de l’acrostiche :", True, GREEN)
        title_rect = title_text.get_rect(
            topleft=(rightside, 0))  # Position relative pour le titre
        onglet_screen.blit(title_text, title_rect)

        # Titre de l'onglet
        paragraph1_text = font_title.render("Encrypter pour les nuls", True, GREEN)
        paragraph1_rect = paragraph1_text.get_rect(topleft=(
        rightside, int(screen_height * 0.10)))  # Position relative pour le premier paragraphe
        onglet_screen.blit(paragraph1_text, paragraph1_rect)

        # Chapeau de l'onglet
        font_paragraph = pygame.font.Font(font_path,
                                          int(screen_height * 0.045))  # Taille relative pour le deuxième paragraphe
        paragraph2_text = font_paragraph.render("Elias Fayette 23/10/17", True, GREEN)
        paragraph2_rect = paragraph2_text.get_rect(topleft=(
        rightside, int(screen_height * 0.23)))  # Position relative pour le deuxième paragraphe
        onglet_screen.blit(paragraph2_text, paragraph2_rect)

        onglet_width = int(screen_width * 0.47)
        # Nouveau paragraphe
        new_paragraphs = [
            "Cette technique, souvent utilisée pour dissimuler des significations secrètes, transforme la lecture en un jeu captivant.",
            "Observez bien votre texte car chaque initiale ou chiffre d’une nouvelle phrase, forme un mot, un message caché ou un code.",
            "Découvrez avec notre article l'acrostiche, une forme littéraire subtile, ajoute une touche d'énigme à l'écriture.",
            "Explorez l'art de l'acrostiche, où chaque mot devient une pièce du puzzle, invitant les lecteurs à déchiffrer des mystères cachés dans les plis de la prose.",
            "2. Commencez par lire attentivement le texte, en prêtant une attention particulière à la première lettre de chaque ligne. Ces lettres formeront probablement le mot ou le code caché.",
            "0. Essayez d'identifier le mot ou la phrase qui sert de guide à l'acrostiche. Cela peut être un nom, un thème, ou même un message clé que l'auteur souhaite transmettre.",
            "2. Identifiez le motif qui unit les premières lettres de chaque ligne. Cela pourrait être un concept, une idée, ou même une émotion que l'auteur souhaite transmettre de manière subtile à travers cette forme poétique.",
            "4. Une fois que vous avez organisé les lettres, interprétez le mot ou le message résultant. Il peut révéler un sens caché, une intention de l'auteur, ou même constituer une partie intégrante de l'énigme à résoudre."
        ]

        line_height = int(0)
        x, y = rightside, int(screen_height * 0.30)

        for paragraph in new_paragraphs:
            # Utiliser textwrap.wrap pour gérer le retour à la ligne
            wrapped_paragraph = textwrap.wrap(paragraph, width=int(onglet_width / font_paragraph.size(' ')[0]))# Nombre de caractères avant de faire un retour à la ligne

            for line in wrapped_paragraph:
                line_text = font_paragraph.render(line, True, GREEN)
                line_rect = line_text.get_rect(topleft=(x, y))

                onglet_screen.blit(line_text, line_rect)

                # Mettre à jour la position pour la prochaine ligne
                x = rightside
                y = line_rect.bottom + line_height

            y = y + int(screen_height * 0.02)  # Ajouter un espace entre les paragraphes


class Onglet2:
    def draw(self, screen):
        font = pygame.font.Font(font_path, 36)
        text = font.render("Contenu onglet 2", True, GREEN)
        text_rect = text.get_rect(center=(screen.get_width() - 200, screen.get_height() // 2))
        screen.blit(text, text_rect)


class Onglet3:
    def draw(self, screen):
        font = pygame.font.Font(font_path, 36)
        text = font.render("Contenu onglet 3", True, GREEN)
        text_rect = text.get_rect(center=(screen.get_width() - 200, screen.get_height() // 2))
        screen.blit(text, text_rect)

class Onglet4:
    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render("Contenu onglet 4", True, GREEN)
        text_rect = text.get_rect(center=(screen.get_width() - 200, screen.get_height() // 2))
        screen.blit(text, text_rect)


class Onglet5:
    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render("Contenu onglet 5", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() - 200, screen.get_height() // 2))
        screen.blit(text, text_rect)

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

        self.is_running = True

        self.tab_rect = self.get_tab_content_space()  # Rectangle du contenu des onglets
        self.onglet = [Onglet1(self.screen.subsurface(self.tab_rect)), Onglet2(), Onglet3(self.screen.subsurface(self.tab_rect)), Onglet4(), Onglet5()]  # Contenu de chaque onglet



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
        self.onglet[self.current_tab].handle_events(events, self.tab_rect)

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
        self.onglet[self.current_tab].draw()


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
    def __init__(self,onglet_screen):
        self.onglet_screen = onglet_screen
        self.screen_width, self.screen_height = onglet_screen.get_size()
        self.rightside = int(self.screen_width * 0.02)

        #Fonts
        self.font_title = pygame.font.Font(font_path, int(self.screen_height * 0.14))  # Taille relative pour le titre
        self.font_paragraph = pygame.font.Font(font_path, int(self.screen_height * 0.045))  # Taille relative pour le titre
        self.font_paragraph_bold = pygame.font.Font(font_path, int(self.screen_height * 0.045))  # Taille relative pour le titre
        self.font_paragraph_bold.set_bold(True)

    def handle_events(self, events, tab_rect):
        pass

    def print_formatted_text(self, paragraph_text):
        x = self.rightside
        y = int(self.screen_height * 0.30)

        for paragraph in paragraph_text:
            # Divisez le paragraphe en lignes
            lines = textwrap.wrap(paragraph, width=130)  # Ajustez la largeur selon vos besoins

            for line in lines:
                words = line.split()

                for word in words:
                    # Si le mot est en gras
                    if word.startswith("**") and word.endswith("**"):
                        word = word.strip("*")
                        word_text = self.font_paragraph_bold.render(word, True, GREEN)
                    # Si le mot n'est pas en gras
                    else:
                        word_text = self.font_paragraph.render(word, True, GREEN)

                    word_rect = word_text.get_rect(topleft=(x, y))

                    # Vérifiez si le texte dépasse self.onglet_screen
                    if word_rect.right > self.onglet_screen.get_width():
                        # Retour à la ligne
                        x = self.rightside
                        #y += word_rect.height + 10

                    self.onglet_screen.blit(word_text, word_rect)
                    x += word_rect.width + 6

                # Retour à la ligne pour la fin de la ligne
                x = self.rightside
                y += word_rect.height + 6
            y+= 10

    def draw(self):
        # Titre de l'onglet
        title_text = self.font_title.render("L’art de l’acrostiche :", True, GREEN)
        title_rect = title_text.get_rect(
            topleft=(self.rightside, 0))  # Position relative pour le titre
        self.onglet_screen.blit(title_text, title_rect)

        # Titre de l'onglet
        title_text2 = self.font_title.render("Encrypter pour les nuls", True, GREEN)
        title_text2_rect = title_text2.get_rect(topleft=(
        self.rightside, int(self.screen_height * 0.10)))  # Position relative pour le premier paragraphe
        self.onglet_screen.blit(title_text2, title_text2_rect)

        # Chapeau de l'onglet
        paragraph_text = self.font_paragraph.render("Elias Fayette 23/10/17", True, GREEN)
        paragraph_rect = paragraph_text.get_rect(topleft=(
        self.rightside, int(self.screen_height * 0.23)))  # Position relative pour le deuxième paragraphe
        self.onglet_screen.blit(paragraph_text, paragraph_rect)

        onglet_width = int(self.screen_width * 0.47)
        # Nouveau paragraphe
        new_paragraphs = [
            "**Cette** technique, souvent utilisée pour dissimuler des significations secrètes, transforme la lecture en un jeu captivant.",
            "**Observez** bien votre texte car chaque initiale ou chiffre d’une nouvelle phrase, forme un mot, un message caché ou un code.",
            "**Découvrez** avec notre article l'acrostiche, une forme littéraire subtile, ajoute une touche d'énigme à l'écriture.",
            "**Explorez** l'art de l'acrostiche, où chaque mot devient une pièce du puzzle, invitant les lecteurs à déchiffrer des mystères cachés dans les plis de la prose.",
            "**2.** Commencez par lire attentivement le texte, en prêtant une attention particulière à la première lettre de chaque ligne. Ces lettres formeront probablement le mot ou le code caché.",
            "**0.** Essayez d'identifier le mot ou la phrase qui sert de guide à l'acrostiche. Cela peut être un nom, un thème, ou même un message clé que l'auteur souhaite transmettre.",
            "**2.** Identifiez le motif qui unit les premières lettres de chaque ligne. Cela pourrait être un concept, une idée, ou même une émotion que l'auteur souhaite transmettre de manière subtile à travers cette forme poétique.",
            "**4.** Une fois que vous avez organisé les lettres, interprétez le mot ou le message résultant. Il peut révéler un sens caché, une intention de l'auteur, ou même constituer une partie intégrante de l'énigme à résoudre."
        ]
        self.print_formatted_text(new_paragraphs)
        #line_height = int(0)
        #x, y = self.rightside, int(self.screen_height * 0.30)
#
        #for paragraph in new_paragraphs:
        #    # Utiliser textwrap.wrap pour gérer le retour à la ligne
        #    wrapped_paragraph = textwrap.wrap(paragraph, width=int(onglet_width / self.font_paragraph.size(' ')[0]))# Nombre de caractères avant de faire un retour à la ligne
#
        #    for line in wrapped_paragraph:
        #        line_text = self.font_paragraph.render(line, True, GREEN)
        #        line_rect = line_text.get_rect(topleft=(x, y))
#
        #        self.onglet_screen.blit(line_text, line_rect)
#
        #        # Mettre à jour la position pour la prochaine ligne
        #        x = self.rightside
        #        y = line_rect.bottom + line_height
#
        #    y = y + int(self.screen_height * 0.02)  # Ajouter un espace entre les paragraphes


class Onglet2:
    def draw(self, screen):
        font = pygame.font.Font(font_path, 36)
        text = font.render("Contenu onglet 2", True, GREEN)
        text_rect = text.get_rect(center=(screen.get_width() - 200, screen.get_height() // 2))
        screen.blit(text, text_rect)


class Onglet3:
    def __init__(self, onglet_screen):
        self.pagenum = 1
        self.maxpages = 6
        self.onglet_screen = onglet_screen
        self.screen_width, self.screen_height = onglet_screen.get_size()
        self.rightside = int(self.screen_width * 0.02)

        # Fonts
        self.font_title = pygame.font.Font(font_path, int(self.screen_height * 0.10))  # Taille relative pour le titre
        self.font_paragraph = pygame.font.Font(font_path,
                                               int(self.screen_height * 0.045))  # Taille relative pour le titre
        self.font_paragraph_bold = pygame.font.Font(font_path,
                                                    int(self.screen_height * 0.045))  # Taille relative pour le titre
        self.font_paragraph_bold.set_bold(True)

        # Arrow
        # Place prise par le texte
        paragraph_text = self.font_paragraph.render("Rachel Perdita 03/06/21    Page : 123456   ", True, GREEN)
        place_prise_par_texte = paragraph_text.get_rect().width

        self.arrowup_image = pygame.image.load("Ressources/arrowup.png")
        # Mettre l'image sous forme de sprite
        self.arrowup_image = pygame.transform.scale(self.arrowup_image, (int(self.screen_width * 0.035), int(self.screen_height * 0.03)))
        # Récupérer le rectangle de l'image
        self.arrowup_rect = self.arrowup_image.get_rect(topleft=(int(self.rightside + place_prise_par_texte + 10), int(self.screen_height * 0.23)))


        self.arrowdown_image = pygame.image.load("Ressources/arrowdown.png")
        self.arrowdown_image = pygame.transform.scale(self.arrowdown_image, (int(self.screen_width * 0.035), int(self.screen_height * 0.03)))
        self.arrowdown_rect = self.arrowdown_image.get_rect(topleft=(int(self.arrowup_rect.right + 10), int(self.screen_height * 0.23)))

    def handle_events(self, events, tab_rect):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Additionner la position du rectangle de l'onglet avec la position de la souris
                    # pour obtenir la position de la souris dans l'onglet
                    mouse_pos = (event.pos[0] - tab_rect.x, event.pos[1] - tab_rect.y)
                    if self.arrowup_rect.collidepoint(mouse_pos):
                        if self.pagenum > 1:
                            self.pagenum -= 1
                    elif self.arrowdown_rect.collidepoint(mouse_pos):
                        if self.pagenum < self.maxpages:
                            self.pagenum += 1
    def print_formatted_text(self, paragraph_text):
        x = self.rightside
        y = int(self.screen_height * 0.30)

        for paragraph in paragraph_text:
            # Divisez le paragraphe en lignes
            lines = textwrap.wrap(paragraph, width=120)  # Ajustez la largeur selon vos besoins

            for line in lines:
                words = line.split()

                for word in words:
                    # Si le mot est en gras
                    if word.startswith("**") and word.endswith("**"):
                        word = word.strip("*")
                        word_text = self.font_paragraph_bold.render(word, True, GREEN)
                    # Si le mot n'est pas en gras
                    else:
                        word_text = self.font_paragraph.render(word, True, GREEN)

                    word_rect = word_text.get_rect(topleft=(x, y))

                    # Vérifiez si le texte dépasse self.onglet_screen
                    if word_rect.right > self.onglet_screen.get_width():
                        # Retour à la ligne
                        x = self.rightside
                        # y += word_rect.height + 10

                    self.onglet_screen.blit(word_text, word_rect)
                    x += word_rect.width + 6

                # Retour à la ligne pour la fin de la ligne
                x = self.rightside
                y += word_rect.height + 6
            y += 10

    def draw(self):
        # Titre de l'onglet
        title_text = self.font_title.render("L'Éventail des Méthodes d'Encryption :", True, GREEN)
        title_rect = title_text.get_rect(
            topleft=(self.rightside, 0))  # Position relative pour le titre
        self.onglet_screen.blit(title_text, title_rect)

        # Titre de l'onglet
        title_text2 = self.font_title.render("Une Exploration Profonde des 20 meilleures", True, GREEN)
        title_text2_rect = title_text2.get_rect(topleft=(
            self.rightside, int(self.screen_height * 0.10)))  # Position relative pour le premier paragraphe
        self.onglet_screen.blit(title_text2, title_text2_rect)

        # Chapeau de l'onglet
        paragraph_text = self.font_paragraph.render("Rachel Perdita 03/06/21    Page :  " + str(self.pagenum), True, GREEN)
        paragraph_rect = paragraph_text.get_rect(topleft=(
            self.rightside, int(self.screen_height * 0.23)))  # Position relative pour le deuxième paragraphe
        self.onglet_screen.blit(paragraph_text, paragraph_rect)

        onglet_width = int(self.screen_width * 0.47)
        # Nouveau paragraphe
        paragraph0 = [
            "Dans la quête constante de protéger l'information sensible dans le monde numérique, la cryptographie offre un arsenal diversifié de méthodes d'encryption. Chacune de ces techniques, allant des classiques aux plus avancées, joue un rôle crucial dans la sécurisation des données. Dans cette analyse approfondie, nous examinons 20 façons de crypter un message, mettant en lumière la sophistication et la diversité de ces méthodes.",

            "Substitution Monoalphabétique :\nChaque lettre est remplacée par une autre lettre selon une correspondance aléatoire, créant une substitution unique pour chaque lettre du message.",

            "Transposition :\nCette technique réarrange l'ordre des lettres dans le message en suivant un schéma prédéterminé, ajoutant une dimension supplémentaire de complexité à la lecture.",

            "Chiffrement de César :\nLa méthode de César consiste à décaler par la droite chaque lettre de l'alphabet ou chiffre par un nombre fixe caractérisé par une “clé”. Par exemple, un décalage de 6  places convertira A en G, B en H, et ainsi de suite.",

            "Chiffre de Playfair :\nFondé sur une grille 5x5, ce chiffre remplace les paires de lettres selon des règles spécifiques définies par la position des lettres dans la grille."]

        paragraph1 = [

            "Chiffre de Vigenère :\nÉvolution du chiffrement de César, le chiffre de Vigenère utilise une clé pour déterminer le décalage des lettres. Pour chiffrer un message, on aligne le texte original et la clé, puis on utilise une table de Vigenère, souvent représentée sous forme de grille. Chaque lettre du message est décalée par la lettre correspondante de la clé en utilisant la ligne et la colonne appropriées dans la table."

            "Chiffre d'Affine :\nCette technique combine les méthodes de substitution et de transposition en utilisant une fonction mathématique linéaire.",

            "Chiffre de Hill :\nEn utilisant une matrice, le chiffre de Hill effectue une transformation sur des groupes de lettres du message original.",

            "Chiffrement par Décalage Circulaire :\nLes lettres sont déplacées en rotation, introduisant une variante au chiffrement de César en rendant le texte chiffré plus difficile à décoder.",

            "Chiffrement de Vernam (OTP) :\nConsidéré comme inviolable, ce chiffrement utilise une clé aussi longue que le message et réalise un XOR avec chaque caractère, garantissant une sécurité maximale.",

            "Chiffrement DES :\nUn standard dans les communications sécurisées, utilise une clé de 56 bits pour encrypter les données par blocs.",

            "AES (Advanced Encryption Standard) :\nUn algorithme symétrique, utilisant des clés de 128, 192 ou 256 bits pour sécuriser l'information de manière efficace.",

            "RSA (Rivest–Shamir–Adleman) :\nUn algorithme asymétrique qui utilise une paire de clés publique/privée pour le chiffrement et le déchiffrement, assurant une communication sécurisée.",

            "Elliptic Curve Cryptography (ECC) :\nFondée sur les propriétés mathématiques des courbes elliptiques, ECC offre une sécurité accrue avec des clés plus courtes.",

            "Diffie-Hellman :\nCette méthode permet un échange sécurisé de clés sur un canal non sécurisé, une base fondamentale pour de nombreux protocoles de sécurité.",

            "PGP (Pretty Good Privacy) :\nUn programme de cryptographie qui fournit des services de confidentialité et d'authentification, utilisant une combinaison de chiffrement asymétrique et de hachage.",

            "Hashing MD5 :\nMD5 transforme les données en une chaîne de caractères de 128 bits, souvent utilisée pour vérifier l'intégrité des fichiers.",

            "SHA-256 (Secure Hash Algorithm 256-bit) :\nUne variante de la famille des algorithmes SHA, utilisée pour sécuriser les transactions dans les blockchains, produisant une empreinte de 256 bits.",

            "Blowfish :\nUn algorithme de chiffrement par bloc, conçu pour être rapide et sécurisé, utilisant une clé de longueur variable.",

            "Twofish :\nSuccesseur du Blowfish, utilisé pour le chiffrement de données avec une structure de blocs plus complexe.",

            "Camellia :\nUn algorithme de chiffrement par bloc, adopté comme standard au Japon, offrant une alternative robuste pour sécuriser les communications.",

            "Chacune de ces méthodes offre une solution unique pour protéger l'information, reflétant l'évolution constante de la cryptographie dans un monde numérique dynamique. Les professionnels de la sécurité doivent naviguer habilement parmi ces options pour garantir la confidentialité et l'intégrité des données dans un paysage de plus en plus complexe."
        ]

        paragraphoriginal = [
            ["Dans la quête constante de protéger l'information sensible dans le monde numérique, la cryptographie offre un arsenal diversifié de méthodes d'encryption. Chacune de ces techniques, allant des classiques aux plus avancées, joue un rôle crucial dans la sécurisation des données. Dans cette analyse approfondie, nous examinons 20 façons de crypter un message, mettant en lumière la sophistication et la diversité de ces méthodes.",

            "Substitution Monoalphabétique :\nChaque lettre est remplacée par une autre lettre selon une correspondance aléatoire, créant une substitution unique pour chaque lettre du message.",

            "Transposition :\nCette technique réarrange l'ordre des lettres dans le message en suivant un schéma prédéterminé, ajoutant une dimension supplémentaire de complexité à la lecture.",

            "Chiffrement de César :\nLa méthode de César consiste à décaler par la droite chaque lettre de l'alphabet ou chiffre par un nombre fixe caractérisé par une “clé”. Par exemple, un décalage de 6  places convertira A en G, B en H, et ainsi de suite.",

            "Chiffre de Playfair :\nFondé sur une grille 5x5, ce chiffre remplace les paires de lettres selon des règles spécifiques définies par la position des lettres dans la grille."],
            [
            "Chiffre de Vigenère :\nÉvolution du chiffrement de César, le chiffre de Vigenère utilise une clé pour déterminer le décalage des lettres. Pour chiffrer un message, on aligne le texte original et la clé, puis on utilise une table de Vigenère, souvent représentée sous forme de grille. Chaque lettre du message est décalée par la lettre correspondante de la clé en utilisant la ligne et la colonne appropriées dans la table.",

            "Chiffre d'Affine :\nCette technique combine les méthodes de substitution et de transposition en utilisant une fonction mathématique linéaire.",

            "Chiffre de Hill :\nEn utilisant une matrice, le chiffre de Hill effectue une transformation sur des groupes de lettres du message original."]]

        #self.print_formatted_text(paragraph0)
        self.print_formatted_text(paragraphoriginal[self.pagenum - 1])

        if self.pagenum < self.maxpages:
            self.onglet_screen.blit(self.arrowdown_image, self.arrowdown_rect)
        if self.pagenum > 1:
            self.onglet_screen.blit(self.arrowup_image, self.arrowup_rect)


        # line_height = int(0)
        # x, y = self.rightside, int(self.screen_height * 0.30)


#
# for paragraph in new_paragraphs:
#    # Utiliser textwrap.wrap pour gérer le retour à la ligne
#    wrapped_paragraph = textwrap.wrap(paragraph, width=int(onglet_width / self.font_paragraph.size(' ')[0]))# Nombre de caractères avant de faire un retour à la ligne
#
#    for line in wrapped_paragraph:
#        line_text = self.font_paragraph.render(line, True, GREEN)
#        line_rect = line_text.get_rect(topleft=(x, y))
#
#        self.onglet_screen.blit(line_text, line_rect)
#
#        # Mettre à jour la position pour la prochaine ligne
#        x = self.rightside
#        y = line_rect.bottom + line_height
#
#    y = y + int(self.screen_height * 0.02)  # Ajouter un espace entre les paragraphes

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

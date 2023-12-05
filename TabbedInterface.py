import textwrap

import pygame

from Onglet4 import Onglet4
from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID

import sys

# Initialisation de Pygame
#pygame.init()

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

        self.missing_usb_image = pygame.image.load("Ressources/missing_usb_opacity.png")
        # Redimensionner l'image avec la même taille que les sprites d'onglet
        self.missing_usb_image = pygame.transform.scale(self.missing_usb_image, self.tab_sprites.sprites()[0].rect.size)


        self.is_running = True

        self.tab_rect = self.get_tab_content_space()  # Rectangle du contenu des onglets
        self.subsurface = self.screen.subsurface(self.tab_rect)  # Surface virtuelle pour le contenu des onglets
        self.onglet = [Onglet1(self.subsurface), Onglet2(self.subsurface), Onglet3(self.subsurface), Onglet4(self.subsurface), Onglet5(self.subsurface)]  # Contenu de chaque onglet

        #USB
        self.usbconnected = False
        self.monitor = USBMonitor()

        # Start the daemon avec votre fonction de connexion
        self.monitor.start_monitoring(on_connect=self.on_usb_connect, on_disconnect=self.on_usb_disconnect)

    def on_usb_connect(self,device_id, device_info):
        self.usbconnected = True

    def on_usb_disconnect(self,device_id, device_info):
        pass  # Ne rien faire en cas de déconnexion


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
                            # If i est dans 2,3
                            if i in [1,2,3]:
                                if self.usbconnected:
                                    self.current_tab = i
                                    print("Tab changed to", self.current_tab)
                            else:
                                self.current_tab = i
                                print("Tab changed to", self.current_tab)
        self.onglet[self.current_tab].handle_events(events, self.tab_rect)

    def update(self):
        pass

    def draw(self):

        self.screen.fill(BLACK)
        # Afficher les onglets en une colonne à gauche
        self.tab_sprites.draw(self.screen)

        if not self.usbconnected :
            # Afficher l'image de l'USB manquant sur les onglets 2,3,4
            self.screen.blit(self.missing_usb_image, self.tab_sprites.sprites()[1].rect)
            self.screen.blit(self.missing_usb_image, self.tab_sprites.sprites()[2].rect)
            self.screen.blit(self.missing_usb_image, self.tab_sprites.sprites()[3].rect)


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

        # Texte
        self.paragraphs = [
            "**Cette** technique, souvent utilisée pour dissimuler des significations secrètes, transforme la lecture en un jeu captivant.",
            "**Observez** bien votre texte car chaque initiale ou chiffre d’une nouvelle phrase, forme un mot, un message caché ou un code.",
            "**Découvrez** avec notre article l'acrostiche, une forme littéraire subtile, ajoute une touche d'énigme à l'écriture.",
            "**Explorez** l'art de l'acrostiche, où chaque mot devient une pièce du puzzle, invitant les lecteurs à déchiffrer des mystères cachés dans les plis de la prose.",
            "**2.** Commencez par lire attentivement le texte, en prêtant une attention particulière à la première lettre de chaque ligne. Ces lettres formeront probablement le mot ou le code caché.",
            "**0.** Essayez d'identifier le mot ou la phrase qui sert de guide à l'acrostiche. Cela peut être un nom, un thème, ou même un message clé que l'auteur souhaite transmettre.",
            "**2.** Identifiez le motif qui unit les premières lettres de chaque ligne. Cela pourrait être un concept, une idée, ou même une émotion que l'auteur souhaite transmettre de manière subtile à travers cette forme poétique.",
            "**4.** Une fois que vous avez organisé les lettres, interprétez le mot ou le message résultant. Il peut révéler un sens caché, une intention de l'auteur, ou même constituer une partie intégrante de l'énigme à résoudre."
        ]

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

        self.print_formatted_text(self.paragraphs)


class Onglet2:
    def __init__(self, onglet_screen):
        self.pagenum = 1
        self.maxpages = 2
        self.onglet_screen = onglet_screen
        self.screen_width, self.screen_height = onglet_screen.get_size()
        self.rightside = int(self.screen_width * 0.02)

        # Fonts
        self.font_title = pygame.font.Font(font_path, int(self.screen_height * 0.12))  # Taille relative pour le titre
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


        # Texte
        self.paragraphs = [
            [
            "Depuis aussi longtemps que je me souvienne, les voyages ont toujours été ma passion, une source inépuisable d'émerveillement et d'inspiration. Chaque destination est une promesse de découvertes, une aventure qui élargit mes horizons et nourrit ma soif insatiable de nouvelles expériences.",
            "Mes destinations préférées ne se résument pas seulement à des endroits sur la carte, mais à des souvenirs vibrants d'histoires partagées, de cultures immergées et de paysages gravés dans ma mémoire. Des ruelles animées aux vastes étendues, chaque lieu a laissé une empreinte unique dans le livre de mes voyages.",
            "L'Italie, avec sa richesse culturelle et ses délices gastronomiques, m'a transporté dans une époque où l'art et la passion se mêlent harmonieusement.",
            "Le Canada, avec ses vastes étendues sauvages et ses lacs paisibles, m'a offert une évasion vers la nature brute, une bouffée d'air frais dans le tumulte de la vie quotidienne.",
            "Le Brésil, vibrant et envoûtant, a réveillé en moi une énergie festive, une célébration de la vie sous le rythme enivrant de la samba."],
            [
            "Le Japon, avec sa fusion unique de tradition et de modernité, a éveillé ma curiosité, me plongeant dans un monde où le respect de la tradition coexiste avec l'innovation futuriste.",
            "Et puis, il y a l'Algérie, un joyau niché en Afrique du Nord, qui m'appelle avec ses oasis mystiques, ses marchés animés et son histoire captivante. Chaque pays sur ma liste représente une quête personnelle, une exploration de l'inconnu, une opportunité de découvrir des facettes encore inexplorées du monde.",
            "Dans l'incertitude du futur, une chose reste certaine : mes pieds continueront à fouler le sol de nouvelles contrées, mes yeux à s'émerveiller devant des horizons inexplorés. Car pour moi, le voyage est bien plus qu'une simple activité, c'est une passion qui alimente mon âme et élargit mes perspectives, un chapitre infini d'aventures à écrire, de découvertes à faire, et de rêves à réaliser."
            ]
            ]

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
        title_text = self.font_title.render("À la Découverte de Mes Passions :", True, GREEN)
        title_rect = title_text.get_rect(
            topleft=(self.rightside, 0))  # Position relative pour le titre
        self.onglet_screen.blit(title_text, title_rect)

        # Titre de l'onglet
        title_text2 = self.font_title.render("Explorateur dans l' âme", True, GREEN)
        title_text2_rect = title_text2.get_rect(topleft=(
            self.rightside, int(self.screen_height * 0.10)))  # Position relative pour le premier paragraphe
        self.onglet_screen.blit(title_text2, title_text2_rect)

        # Chapeau de l'onglet
        paragraph_text = self.font_paragraph.render("                                                            Page :  " + str(self.pagenum), True, GREEN)
        paragraph_rect = paragraph_text.get_rect(topleft=(
            self.rightside, int(self.screen_height * 0.23)))  # Position relative pour le deuxième paragraphe
        self.onglet_screen.blit(paragraph_text, paragraph_rect)


        self.print_formatted_text(self.paragraphs[self.pagenum - 1])

        if self.pagenum < self.maxpages:
            self.onglet_screen.blit(self.arrowdown_image, self.arrowdown_rect)
        if self.pagenum > 1:
            self.onglet_screen.blit(self.arrowup_image, self.arrowup_rect)


class Onglet3:
    def __init__(self, onglet_screen):
        self.pagenum = 1
        self.maxpages = 4
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


        # Texte
        self.paragraphs = [
            ["Dans la quête constante de protéger l'information sensible dans le monde numérique, la cryptographie offre un arsenal diversifié de méthodes d'encryption. Chacune de ces techniques, allant des classiques aux plus avancées, joue un rôle crucial dans la sécurisation des données. Dans cette analyse approfondie, nous examinons 20 façons de crypter un message, mettant en lumière la sophistication et la diversité de ces méthodes.",

            "**Substitution** Monoalphabétique :\nChaque lettre est remplacée par une autre lettre selon une correspondance aléatoire, créant une substitution unique pour chaque lettre du message.",

            "**Transposition** :\nCette technique réarrange l'ordre des lettres dans le message en suivant un schéma prédéterminé, ajoutant une dimension supplémentaire de complexité à la lecture.",

            "Chiffrement de **César** :\nLa méthode de César consiste à décaler par la droite chaque lettre de l'alphabet ou chiffre par un nombre fixe caractérisé par une “clé”. Par exemple, un décalage de 6  places convertira A en G, B en H, et ainsi de suite.",

            "Chiffre de **Playfair** :\nFondé sur une grille 5x5, ce chiffre remplace les paires de lettres selon des règles spécifiques définies par la position des lettres dans la grille."
            ],
            [
            "Chiffre de **Vigenère** :\nÉvolution du chiffrement de César, le chiffre de Vigenère utilise une clé pour déterminer le décalage des lettres. Pour chiffrer un message, on aligne le texte original et la clé, puis on utilise une table de Vigenère, souvent représentée sous forme de grille. Chaque lettre du message est décalée par la lettre correspondante de la clé en utilisant la ligne et la colonne appropriées dans la table.",

            "Chiffre d' **Affine** :\nCette technique combine les méthodes de substitution et de transposition en utilisant une fonction mathématique linéaire.",

            "Chiffre de **Hill** :\nEn utilisant une matrice, le chiffre de Hill effectue une transformation sur des groupes de lettres du message original.",

            "Chiffrement par **Décalage** **Circulaire** :\nLes lettres sont déplacées en rotation, introduisant une variante au chiffrement de César en rendant le texte chiffré plus difficile à décoder.",

            "Chiffrement **de** **Vernam** (OTP) :\nConsidéré comme inviolable, ce chiffrement utilise une clé aussi longue que le message et réalise un XOR avec chaque caractère, garantissant une sécurité maximale."
            ],
            [

            "Chiffrement **DES** :\nUn standard dans les communications sécurisées, utilise une clé de 56 bits pour encrypter les données par blocs.",

            "**AES** (Advanced Encryption Standard) :\nUn algorithme symétrique, utilisant des clés de 128, 192 ou 256 bits pour sécuriser l'information de manière efficace.",

            "**RSA** (Rivest Shamir Adleman) :\nUn algorithme asymétrique qui utilise une paire de clés publique/privée pour le chiffrement et le déchiffrement, assurant une communication sécurisée.",

            "**Elliptic** Curve Cryptography (ECC) :\nFondée sur les propriétés mathématiques des courbes elliptiques, ECC offre une sécurité accrue avec des clés plus courtes.",

            "**Diffie-Hellman** :\nCette méthode permet un échange sécurisé de clés sur un canal non sécurisé, une base fondamentale pour de nombreux protocoles de sécurité.",

            "**PGP** (Pretty Good Privacy) :\nUn programme de cryptographie qui fournit des services de confidentialité et d'authentification, utilisant une combinaison de chiffrement asymétrique et de hachage."
            ],
            [
            "**Hashing** MD5 :\nMD5 transforme les données en une chaîne de caractères de 128 bits, souvent utilisée pour vérifier l'intégrité des fichiers.",

            "**SHA-256** (Secure Hash Algorithm 256-bit) :\nUne variante de la famille des algorithmes SHA, utilisée pour sécuriser les transactions dans les blockchains, produisant une empreinte de 256 bits.",

            "**Blowfish** :\nUn algorithme de chiffrement par bloc, conçu pour être rapide et sécurisé, utilisant une clé de longueur variable.",

            "vTwofish** :\nSuccesseur du Blowfish, utilisé pour le chiffrement de données avec une structure de blocs plus complexe.",

            "**Camellia** :\nUn algorithme de chiffrement par bloc, adopté comme standard au Japon, offrant une alternative robuste pour sécuriser les communications.",

            "Chacune de ces méthodes offre une solution unique pour protéger l'information, reflétant l'évolution constante de la cryptographie dans un monde numérique dynamique. Les professionnels de la sécurité doivent naviguer habilement parmi ces options pour garantir la confidentialité et l'intégrité des données dans un paysage de plus en plus complexe."
            ]
            ]

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


        self.print_formatted_text(self.paragraphs[self.pagenum - 1])

        if self.pagenum < self.maxpages:
            self.onglet_screen.blit(self.arrowdown_image, self.arrowdown_rect)
        if self.pagenum > 1:
            self.onglet_screen.blit(self.arrowup_image, self.arrowup_rect)


class Onglet5:
    def __init__(self,onglet_screen):
        self.screen = onglet_screen
        self.screen_width, self.screen_height = onglet_screen.get_size()
        self.rightside = int(self.screen_width * 0.02)

        self.is_finished = False
        self.is_login_failed = False
        self.text_color = (0, 0, 0)
        self.input_box_color = (200, 200, 200)

        #Fonts
        self.font_title = pygame.font.Font(font_path, int(self.screen_height * 0.18))  # Taille relative pour le titre
        self.font_password = pygame.font.Font(font_path, 36)

        # Entrées
        self.password = ""


    def handle_events(self, events, tab_rect):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.password == "REVOLVE4EVER":
                        self.is_finished = True
                        #print("REBOOT successful")
                    else:
                        self.is_login_failed = True
                        #print("Login failed")
                elif event.key == pygame.K_BACKSPACE:
                    # Gestion de la suppression
                    self.password = self.password[:-1]
                elif event.unicode:  # Vérifier si le caractère unicode est disponible
                    char = event.unicode
                    # Convertir en majuscule
                    char = char.upper()
                    self.password += char
                    #print(self.password)

    def draw(self):
        self.screen.fill(BLACK)

        if not self.is_finished:
            # Titre de l'onglet
            title_text = self.font_title.render("Reboot Mot De Passe", True, GREEN)
            title_rect = title_text.get_rect(
                topleft=((self.screen.get_width() - self.font_title.render("Reboot Mot De Passe", True, GREEN).get_width()) // 2, self.screen.get_height() * 0.25))  # Position relative pour le titre
            self.screen.blit(title_text, title_rect)

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

            # pygame.draw.rect(self.screen, text_color, (input_box_x + input_box_width, input_box_y, 2, 30))
            if self.is_login_failed:
                text_surface = self.font_password.render("Mot de passe incorrect", True, (255, 0, 0))
                self.screen.blit(text_surface, (input_box_x - 170, input_box_y + 60))

            # Affichage du texte "Mot de Passe :" à gauche de l'entrée
            text_surface = self.font_password.render("Mot de Passe :", True, GREEN)
            self.screen.blit(text_surface, (input_box_x - 170, input_box_y + 8))

            # Affichage du mot de passe masqué
            password_text_surface = self.font_password.render(self.password, True, GREEN)
            self.screen.blit(password_text_surface, (input_box_x + 10, input_box_y + 10))
        elif self.is_finished:
            self.screen.fill(BLACK)
            title_text = self.font_title.render("Mot de passe correct", True, GREEN)
            title_rect = title_text.get_rect(
                topleft=((self.screen.get_width() - self.font_title.render("Mot de passe correct", True, GREEN).get_width()) // 2, self.screen.get_height() * 0.25))
            self.screen.blit(title_text, title_rect)



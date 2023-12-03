import random

import pygame


font_path = "Ressources/Sevastopol-Interface.ttf"

# Définir les couleurs
GREEN = (0,190,99)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)




RED = (255, 0, 0)

class Onglet5:
    # In this class, we will create a snake game like
    def __init__(self, onglet_screen):
        self.screen = onglet_screen
        self.screen_width, self.screen_height = onglet_screen.get_size()
        # Definire la zone de jeu avec une marge de 100px
        self.playing_zone = pygame.Rect(100, 100, self.screen_width - 200, self.screen_height - 200)
        print(self.playing_zone.width)

        self.font = pygame.font.Font(font_path, 36)
        self.start_text_base = "Appuyez sur Entrée pour démarrer"
        self.start_text_rect = None

        self.animation_delay = 60

        self.status = "StartMenu" # StartMenu, Playing, GameOver, Win, Stop
        self.win = False
        self.win_text = self.font.render("clé = 2", True, GREEN)
        self.win_text_rect = self.win_text.get_rect(center=(self.screen_width/2, self.screen_height/2))

        self.score = 0

        self.snake_pos = [200, 150]
        self.snake_body = [[200, 150], [200 - 10, 150], [200 - (2 * 10), 150]]

        self.direction = 'RIGHT'
        self.change_to = self.direction

        # Food
        # Randomly spawn food in the playing zone
        self.food_pos = [random.randrange(self.playing_zone.left+20, self.playing_zone.right-20, 10), random.randrange(self.playing_zone.top+20, self.playing_zone.bottom-20, 10)]
        self.food_spawned = True

        # Game Over
        self.game_over_text = self.font.render("Game Over !", True, RED)
        self.game_over_text_rect = self.game_over_text.get_rect(center=(self.screen_width/2, self.screen_height/2))
        # Restart Button
        self.restart_button_text = self.font.render("Appuyez pour Redémarer", True, GREEN)
        self.restart_button_text_rect = self.restart_button_text.get_rect(center=(self.screen_width/2, self.screen_height/2 + 50))
        self.restart_button = pygame.Rect(self.restart_button_text_rect.left - 10, self.restart_button_text_rect.top - 10, self.restart_button_text_rect.width + 20, self.restart_button_text_rect.height + 20)

        # Start Menu
        self.start_button_text = self.font.render("Appuyez pour démarrer", True, GREEN)
        self.start_button_text_rect = self.start_button_text.get_rect(center=(self.screen_width/2, self.screen_height/2 + 50))
        self.start_button = pygame.Rect(self.start_button_text_rect.left - 10, self.start_button_text_rect.top - 10, self.start_button_text_rect.width + 20, self.start_button_text_rect.height + 20)

        # Score Text en haut à gauche
        self.score_text = self.font.render("Score : " + str(self.score), True, WHITE)
        self.score_text_rect = self.score_text.get_rect(topleft=(self.playing_zone.left, self.playing_zone.top - 50))



    def handle_events(self, events, tab_rect):
        self.update()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('q'):
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.change_to = 'RIGHT'
                if event.key == pygame.K_UP or event.key == ord('z'):
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.change_to = 'DOWN'
            # Detecter si start_button est cliqué avec la position
            if event.type == pygame.MOUSEBUTTONDOWN :
                # Additionner la position du rectangle de l'onglet avec la position de la souris
                # pour obtenir la position de la souris dans l'onglet
                mouse_pos = (event.pos[0] - tab_rect.left, event.pos[1] - tab_rect.top)
                if self.start_button.collidepoint(mouse_pos) and self.status == "StartMenu":
                    self.status = "Playing"

                if self.restart_button.collidepoint(mouse_pos) and self.status == "GameOver":
                    self.status = "Playing"
                    self.score = 0
                    self.snake_pos = [200, 150]
                    self.snake_body = [[200, 150], [200 - 10, 150], [200 - (2 * 10), 150]]
                    self.direction = 'RIGHT'
                    self.change_to = self.direction
                    self.food_pos = [random.randrange(self.playing_zone.left+20, self.playing_zone.right-20, 10), random.randrange(self.playing_zone.top+20, self.playing_zone.bottom-20, 10)]
                    self.food_spawned = True

        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def update(self):
        if self.status == "Playing":
            if self.score >=5:
                self.win = True

            # Moving the snake
            if self.direction == 'UP':
                self.snake_pos[1] -= 10
            if self.direction == 'DOWN':
                self.snake_pos[1] += 10
            if self.direction == 'LEFT':
                self.snake_pos[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_pos[0] += 10

            # Snake body growing mechanism
            self.snake_body.insert(0, list(self.snake_pos))
            if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
                self.score += 1
                self.food_spawned = False
            else:
                self.snake_body.pop()
            # Spawning food on the screen
            if not self.food_spawned:
                self.food_pos = [random.randrange(self.playing_zone.left+20, self.playing_zone.right-20, 10), random.randrange(self.playing_zone.top+20, self.playing_zone.bottom-20, 10)]
                self.food_spawned = True

            # Game Over conditions
            # Getting out of bounds playing zone
            if self.snake_pos[0] < self.playing_zone.left or self.snake_pos[0] > self.playing_zone.right - 10:
                self.status = "GameOver"
            if self.snake_pos[1] < self.playing_zone.top or self.snake_pos[1] > self.playing_zone.bottom - 10:
                self.status = "GameOver"
            # Touching the snake body
            for block in self.snake_body[1:]:
                if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                    self.status = "GameOver"
    def draw(self):
        if self.status == "StartMenu":
            self.screen.fill(BLACK)
            self.screen.blit(self.start_button_text, self.start_button_text_rect)
            pygame.draw.rect(self.screen, GREEN, self.start_button, 2)

        elif self.status == "Playing":
            # Wait for 20 milliseconds to elapse.
            pygame.time.delay(self.animation_delay)

            self.screen.fill(BLACK)
            # Draw rectangle for playing zone
            pygame.draw.rect(self.screen, WHITE, self.playing_zone, 2)

            # affichage du score en haut à gauche
            self.score_text = self.font.render("Score : " + str(self.score) + "  /5", True, WHITE)
            self.screen.blit(self.score_text, self.score_text_rect)

            # if win, affichez le message de victoire à droite du score
            if self.win == True:
                # mettre le message à droite du score
                self.win_text_rect = self.win_text.get_rect()
                self.win_text_rect.center = (self.score_text_rect.right + 100, self.score_text_rect.centery)
                self.screen.blit(self.win_text, self.win_text_rect)


            # Drawing Snake Body
            for pos in self.snake_body:
                # Snake body
                pygame.draw.rect(self.screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

            # Drawing food on screen
            pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
        elif self.status == "GameOver":
            self.screen.fill(BLACK)
            self.screen.blit(self.game_over_text, self.game_over_text_rect)
            self.screen.blit(self.restart_button_text, self.restart_button_text_rect)
            pygame.draw.rect(self.screen, GREEN, self.restart_button, 2)

            # affichage du texte de win en dessous du bouton restart
            if self.win == True:
                #mettre le message en dessous du bouton restart
                self.win_text_rect = self.win_text.get_rect()
                self.win_text_rect.center = (self.restart_button_text_rect.centerx, self.restart_button_text_rect.bottom + 50)
                self.screen.blit(self.win_text, self.win_text_rect)


        # Refresh game screen
        pygame.display.flip()
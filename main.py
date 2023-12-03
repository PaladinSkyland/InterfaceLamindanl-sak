import pygame
import sys
from windows import LoadingWindow, StartPage, LoginPage, CongratulationPage
from TabbedInterface import TabbedInterface

# Initialisation de Pygame
pygame.init()

font_path = "Ressources/Sevastopol-Interface.ttf"  # Remplace avec le chemin de ta police

# Définir les couleurs
BLACK = (0, 0, 0)
GREEN = (0,190,99)
WHITE = (255, 255, 255)

# Créer la classe principale de l'application
class Game:
    def __init__(self):

        info = pygame.display.Info()
        self.SCREEN_WIDTH = info.current_w
        self.SCREEN_HEIGHT = info.current_h

        # Mettre en plein écran
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)


        # Initialiser les différentes fenêtres ou pages
        self.start_page = StartPage(self.screen)
        self.loading_window = LoadingWindow(self.screen)
        self.login_page = LoginPage(self.screen)
        self.tabbed_interface = TabbedInterface(self.screen)
        self.congratulation_page = CongratulationPage(self.screen)

        # Définir l'état initial
        self.current_window = self.start_page

        # Initialiser le minuteur
        self.minuter_seconds = 1800
        self.start_ticks = 0
        self.minuter_affichage = False
        self.minuter_value = 0
        self.minuter_status = "Play" # Play, Stop
        self.minuteurtext = ""

        pygame.display.set_caption("Interface Lamindanlsak")
        self.clock = pygame.time.Clock()
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.current_window == self.congratulation_page:
                self.is_running = False  # Sortir du plein écran si la touche ESC est enfoncée

    def switch_window(self, new_window):
        # Changer la fenêtre courante
        self.current_window = new_window

    def handle_main_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.current_window == self.congratulation_page:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.current_window == self.start_page:
                    print ('ok')
                    self.start_page.is_start_pressed = True


    def timesectommss(self, t):
        if t < 0:
            return "00:00"
        m, s = divmod(t, 60)
        return "%02d:%02d" % (m, s)

    def run(self):
        while self.is_running:
            events = pygame.event.get()
            self.handle_main_events(events)  # Nouvelle fonction pour traiter les événements principaux

            if isinstance(self.current_window, StartPage) and self.current_window.is_start_pressed:
                self.switch_window(self.loading_window)
                self.start_ticks = pygame.time.get_ticks() #starter tick

            if self.loading_window.is_loading_complete:
                print("Loading complete")
                self.switch_window(self.login_page)
                self.loading_window.is_loading_complete = False

            if self.login_page.is_login_complete:
                print("Login complete")
                self.switch_window(self.tabbed_interface)
                self.minuter_affichage = True
                self.login_page.is_login_complete = False

            if self.current_window == self.login_page:
                self.login_page.handle_events(events)

            if self.current_window == self.tabbed_interface:
                self.tabbed_interface.handle_events(events)

            if self.tabbed_interface.onglet[3].is_finished:
                self.minuter_status = "Stop"
                self.minuter_affichage = False
                self.switch_window(self.congratulation_page)
            self.current_window.update()
            self.current_window.draw()


            # Minuteur
            if self.minuter_status == "Play":
                temps_ecoule = (pygame.time.get_ticks() - self.start_ticks) // 1000
                self.minuteurtext = self.timesectommss(self.minuter_seconds - temps_ecoule)

            if self.minuter_affichage:
                # Affichage du minuteur en haut à droite de l'écran dans un carrée noir de bordure verte
                pygame.draw.rect(self.screen, BLACK, [self.SCREEN_WIDTH - 250, 50, 200, 100], 0)
                pygame.draw.rect(self.screen, GREEN, [self.SCREEN_WIDTH - 250, 50, 200, 100], 2)
                font = pygame.font.Font(font_path, 60)
                text = font.render(self.minuteurtext, True, GREEN)
                self.screen.blit(text, [self.SCREEN_WIDTH - 200, 70])

            if self.current_window == self.congratulation_page:
                self.congratulation_page.drawtime(self.minuteurtext)

            #print(self.minute)
            #print(self.seconde)



            pygame.display.flip()# Si tu veux utiliser une valeur différente de FPS, ajuste-la ici
            self.clock.tick(60)

# Code principal
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

import pygame
import sys
from windows import LoadingWindow, StartPage, LoginPage
from TabbedInterface import TabbedInterface

# Initialisation de Pygame
pygame.init()

font_path = "Ressources/Sevastopol-Interface.ttf"  # Remplace avec le chemin de ta police

# Définir les couleurs
BLACK = (0, 0, 0)
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

        # Définir l'état initial
        self.current_window = self.tabbed_interface


        pygame.display.set_caption("Interface Lamindanlsak")
        self.clock = pygame.time.Clock()
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_running = False  # Sortir du plein écran si la touche ESC est enfoncée

    def switch_window(self, new_window):
        # Changer la fenêtre courante
        self.current_window = new_window

    def handle_main_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.current_window == self.start_page:
                    print ('ok')
                    self.start_page.is_start_pressed = True

    def run(self):
        while self.is_running:
            events = pygame.event.get()
            self.handle_main_events(events)  # Nouvelle fonction pour traiter les événements principaux

            if isinstance(self.current_window, StartPage) and self.current_window.is_start_pressed:
                self.switch_window(self.loading_window)

            if self.loading_window.is_loading_complete:
                print("Loading complete")
                self.switch_window(self.login_page)
                self.loading_window.is_loading_complete = False

            if self.login_page.is_login_complete:
                print("Login complete")
                self.switch_window(self.tabbed_interface)
                self.login_page.is_login_complete = False

            if self.current_window == self.login_page:
                self.login_page.handle_events(events)

            if self.current_window == self.tabbed_interface:
                self.tabbed_interface.handle_events(events)
            self.current_window.update()
            self.current_window.draw()




            pygame.display.flip()# Si tu veux utiliser une valeur différente de FPS, ajuste-la ici
            self.clock.tick(60)

# Code principal
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

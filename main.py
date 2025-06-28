import pygame
from assets import Assets
from game import Game
import gamesettings as gs


class BomberMan:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((gs.SCREENWIDTH, gs.SCREENHEIGHT))
        pygame.display.set_caption("BomberMan")

        self.ASSETS = Assets()
        self.GAME = Game(self, self.ASSETS)
        self.FPS = pygame.time.Clock()

        self.run = True


    def input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False
        self.GAME.input(events)


    def update(self):
        self.FPS.tick(gs.FPS)
        self.GAME.update()


    def draw(self, window):
        window.fill(gs.BLACK)
        self.GAME.draw(window)
        pygame.display.update()


    def rungame(self):
        while self.run == True:
            self.input()
            self.update()
            self.draw(self.screen)


if __name__=="__main__":
    game = BomberMan()
    game.rungame()
    pygame.quit()
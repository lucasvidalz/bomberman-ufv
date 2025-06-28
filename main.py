import pygame
from assets import Assets
from game import Game
import gamesettings as gs


class BomberMan:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Configurar a janela com comportamento padrão do Windows
        # Usar RESIZABLE para garantir que a janela tenha as bordas padrão
        self.screen = pygame.display.set_mode((gs.SCREENWIDTH, gs.SCREENHEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("BomberMan")
        
        # Centralizar a janela na tela
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()["window"]
            # Obter dimensões da tela
            screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            screen_height = ctypes.windll.user32.GetSystemMetrics(1)
            # Calcular posição central
            x = (screen_width - gs.SCREENWIDTH) // 2
            y = (screen_height - gs.SCREENHEIGHT) // 2
            # Posicionar a janela
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)
        except Exception as e:
            print(f"Não foi possível centralizar a janela: {e}")
        
        # Garantir que a janela tenha o ícone X e comportamento padrão
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()["window"]
            # Definir estilo da janela para ter bordas padrão
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
            style |= 0x00C00000  # WS_CAPTION | WS_SYSMENU
            style |= 0x00080000  # WS_BORDER
            style |= 0x00040000  # WS_THICKFRAME
            ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
            # Forçar redesenho da janela
            ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0004)
        except Exception as e:
            print(f"Não foi possível configurar as bordas da janela: {e}")

        self.ASSETS = Assets()
        self.GAME = Game(self, self.ASSETS)
        self.FPS = pygame.time.Clock()

        self.run = True


    def input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.VIDEORESIZE:
                # Manter o tamanho original se a janela for redimensionada
                self.screen = pygame.display.set_mode((gs.SCREENWIDTH, gs.SCREENHEIGHT), pygame.RESIZABLE)
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
import pygame
from core.assets import Assets
from core.game import Game
import core.gamesettings as gs

class BomberMan:
    """Classe principal que inicia e executa o jogo"""
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self._initialize_window()
        self._assets = Assets()
        self._game = Game(self, self._assets)
        self._FPS = pygame.time.Clock()
        self._run = True

    def _initialize_window(self):
        """Configura a janela do jogo"""
        self._screen = pygame.display.set_mode((gs.SCREENWIDTH, gs.SCREENHEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("BomberMan")
        self._center_window()
        self._set_window_style()

    def _center_window(self):
        """Centraliza a janela na tela"""
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()["window"]
            screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            screen_height = ctypes.windll.user32.GetSystemMetrics(1)
            x = (screen_width - gs.SCREENWIDTH) // 2
            y = (screen_height - gs.SCREENHEIGHT) // 2
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)
        except Exception as e:
            print(f"Não foi possível centralizar a janela: {e}")

    def _set_window_style(self):
        """Configura o estilo da janela"""
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()["window"]
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
            style |= 0x00C00000  # WS_CAPTION | WS_SYSMENU
            style |= 0x00080000  # WS_BORDER
            style |= 0x00040000  # WS_THICKFRAME
            ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
            ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0004)
        except Exception as e:
            print(f"Não foi possível configurar as bordas da janela: {e}")

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value):
        self._run = value

    def input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self._run = False
            elif event.type == pygame.VIDEORESIZE:
                self._screen = pygame.display.set_mode((gs.SCREENWIDTH, gs.SCREENHEIGHT), pygame.RESIZABLE)
        self._game.input(events)

    def update(self):
        self._FPS.tick(gs.FPS)
        self._game.update()

    def draw(self):
        self._screen.fill(gs.BLACK)
        self._game.draw(self._screen)
        pygame.display.update()

    def run_game(self):
        """Loop principal do jogo"""
        while self._run:
            self.input()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = BomberMan()
    game.run_game()
    pygame.quit()
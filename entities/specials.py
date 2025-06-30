import pygame
import core.gamesettings as gs
from ui.info_panel import Scoring

class Special(pygame.sprite.Sprite):
    """Classe base para os power-ups especiais"""
    # HERANÇA: Special herda de pygame.sprite.Sprite, obtendo funcionalidades 
    # básicas de sprite como grupos, colisões, etc.
    def __init__(self, game, image, name, group, row_num, col_num, size):
        # HERANÇA: Chama o construtor da classe pai (pygame.sprite.Sprite)
        super().__init__(group)
        # ENCAPSULAMENTO: Atributos privados protegem o estado interno dos power-ups
        self._game = game
        self._name = name
        self._row = row_num
        self._col = col_num
        self._size = size
        self._x = self._col * self._size
        self._y = (self._row * self._size) + gs.Y_OFFSET
        self._image = image
        self._rect = self._image.get_rect(topleft=(self._x, self._y))
        # POLIMORFISMO: Dicionário que mapeia nomes de power-ups para métodos específicos
        # Permite que diferentes power-ups tenham comportamentos diferentes
        self._power_up_activate = {
            "bomb_up": self._bomb_up_special,
            "fire_up": self._fire_up_special,
            "speed_up": self._speed_up_special,
            "wall_hack": self._wall_hack_special,
            "remote": self._remote_special,
            "bomb_pass": self._bomb_hack_special,
            "flame_pass": self._flame_pass_special,
            "invincible": self._invincible_special,
            "exit": self._end_stage
        }
        self._score = 1000 if self._name == "exit" else 500

    def update(self):
        # POLIMORFISMO: Método que implementa comportamento específico baseado no tipo de power-up
        if not self._game.player.rect.collidepoint(self._rect.center):
            return
            
        # POLIMORFISMO: Chama o método específico do power-up baseado no nome
        self._power_up_activate[self._name](self._game.player)
        
        if self._name == "exit":
            self._game.bg_music.stop()
            self._game.bg_music_special.stop()
            self._game.player.update_score(self._score)
            return
            
        self._game.level_matrix[self._row][self._col] = "_"
        self._game.assets.sounds["Bomberman SFX (4).wav"].play()
        self._game.bg_music.stop()
        self._game.bg_music_special.play(loops=-1)
        self.kill()
        self._game.player.update_score(self._score)

    def draw(self, window, x_offset):
        # POLIMORFISMO: Método que pode ser sobrescrito por subclasses 
        # para implementar renderização específica
        window.blit(self._image, (self._rect.x - x_offset, self._rect.y))

    def _bomb_up_special(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up bomb_up
        player.bomb_limit += 1

    def _fire_up_special(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up fire_up
        player.power += 1

    def _speed_up_special(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up speed_up
        player.speed += 1

    def _wall_hack_special(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up wall_hack
        player.wall_hack = True

    def _remote_special(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up remote
        player.remote = True

    def _bomb_hack_special(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up bomb_pass
        player.bomb_hack = True

    def _flame_pass_special(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up flame_pass
        player.flame_pass = True

    def _invincible_special(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up invincible
        player.invincibility = True
        player.invincibility_timer = pygame.time.get_ticks()

    def _end_stage(self, player):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica específica do power-up exit
        if len(self._game.groups["enemies"].sprites()) > 0:
            return

        self._game.new_stage()

    def hit_by_explosion(self):
        # ENCAPSULAMENTO: Método público que encapsula a lógica de resposta a explosões
        enemies = []
        for _ in range(10):
            enemies.append(gs.SPECIAL_CONNECTIONS[self._name])

        self._game._insert_enemies_into_level(self._game.level_matrix, enemies)
import pygame
import core.gamesettings as gs
from ui.info_panel import Scoring

class Special(pygame.sprite.Sprite):
    """Classe base para os power-ups especiais"""
    def __init__(self, game, image, name, group, row_num, col_num, size):
        super().__init__(group)
        self._game = game
        self._name = name
        self._row = row_num
        self._col = col_num
        self._size = size
        self._x = self._col * self._size
        self._y = (self._row * self._size) + gs.Y_OFFSET
        self._image = image
        self._rect = self._image.get_rect(topleft=(self._x, self._y))
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
        if not self._game.player.rect.collidepoint(self._rect.center):
            return
            
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
        window.blit(self._image, (self._rect.x - x_offset, self._rect.y))

    def _bomb_up_special(self, player):
        player.bomb_limit += 1

    def _fire_up_special(self, player):
        player.power += 1

    def _speed_up_special(self, player):
        player.speed += 1

    def _wall_hack_special(self, player):
        player.wall_hack = True

    def _remote_special(self, player):
        player.remote = True

    def _bomb_hack_special(self, player):
        player.bomb_hack = True

    def _flame_pass_special(self, player):
        player.flame_pass = True

    def _invincible_special(self, player):
        player.invincibility = True
        player.invincibility_timer = pygame.time.get_ticks()

    def _end_stage(self, player):
        if len(self._game.groups["enemies"].sprites()) > 0:
            return

        self._game.new_stage()

    def hit_by_explosion(self):
        enemies = []
        for _ in range(10):
            enemies.append(gs.SPECIAL_CONNECTIONS[self._name])

        self._game._insert_enemies_into_level(self._game.level_matrix, enemies)
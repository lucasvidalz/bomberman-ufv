import pygame
import gamesettings as gs
from info_panel import Scoring


class Special(pygame.sprite.Sprite):
    def __init__(self, game, image, name, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game

        self.name = name

        #  Posição da Matriz de Nível
        self.row = row_num
        self.col = col_num

        #  coordenadas x, y
        self.size = size
        self.x = self.col * self.size
        self.y = (self.row * self.size) + gs.Y_OFFSET

        #  Imagem
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        #  Habilidades de fortalecimento
        self.power_up_activate = {"bomb_up": self.bomb_up_special,
                                  "fire_up": self.fire_up_special,
                                  "speed_up": self.speed_up_special,
                                  "wall_hack": self.wall_hack_special,
                                  "remote": self.remote_special,
                                  "bomb_pass": self.bomb_hack_special,
                                  "flame_pass": self.flame_pass_special,
                                  "invincible": self.invincible_special,
                                  "exit": self.end_stage}

        self.score = 1000 if self.name == "exit" else 500


    def update(self):
        if self.GAME.player.rect.collidepoint(self.rect.center):
            #  Ative a inicialização
            self.power_up_activate[self.name](self.GAME.player)
            if self.name == "exit":
                self.GAME.bg_music.stop()
                self.GAME.bg_music_special.stop()
                self.GAME.player.update_score(self.score)
                return
            self.GAME.level_matrix[self.row][self.col] = "_"
            self.GAME.ASSETS.sounds["Bomberman SFX (4).wav"].play()
            self.GAME.bg_music.stop()
            self.GAME.bg_music_special.play(loops=-1)
            self.kill()
            self.GAME.player.update_score(self.score)
            return


    def draw(self,window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))


    def bomb_up_special(self, player):
        """Aumenta o limite de bombas do jogador"""
        player.bomb_limit += 1

    def fire_up_special(self, player):
        """Aumenta o poder das bombas"""
        player.power += 1

    def speed_up_special(self, player):
        """Aumenta a velocidade do jogador"""
        player.speed += 1

    def wall_hack_special(self, player):
        """Ativa o hack da parede do jogador"""
        player.wall_hack = True

    def remote_special(self, player):
        """Ativa a capacidade de detonação remota"""
        player.remote = True

    def bomb_hack_special(self, player):
        """Ligua a bomba Hack"""
        player.bomb_hack = True

    def flame_pass_special(self, player):
        """Ativa a capacidade de ignorar explosões de bombas"""
        player.flame_pass = True

    def invincible_special(self, player):
        """Ativa a invencibilidade dos jogadores"""
        player.invincibility = True
        player.invincibility_timer = pygame.time.get_ticks()

    def end_stage(self, player):
        """Termina o nível e gere um novo nível"""
        if len(self.GAME.groups["enemies"].sprites()) > 0:
            return

        self.GAME.new_stage()

    def hit_by_explosion(self):
        """A ação a ser tomada é que o item especial é atingido por uma explosão"""
        enemies = []
        for _ in range(10):
            enemies.append(gs.SPECIAL_CONNECTIONS[self.name])

        self.GAME.insert_enemies_into_level(self.GAME.level_matrix, enemies)
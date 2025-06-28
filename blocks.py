import pygame
from specials import Special
import gamesettings as gs


class Blocks(pygame.sprite.Sprite):
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game
        self.y_offset = gs.Y_OFFSET

        #  Posição na matriz de nivel
        self.row = row_num
        self.col = col_num

        #  Tamanho da celula
        self.size = size

        #  Coordenadas do bloco
        self.x = self.col * self.size
        self.y = (self.row * self.size) + self.y_offset

        #  Attributos
        self.passable = True

        #  Bloquear imagem
        self.image_list = images
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def update(self):
        pass


    def draw(self, window, offset):
        window.blit(self.image, (self.rect.x - offset, self.rect.y))


    def __repr__(self):
        return "'#'"


class Hard_Block(Blocks):
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(game, images, group, row_num, col_num, size)
        self.passable = False

class Soft_Block(Blocks):
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(game, images, group, row_num, col_num, size)
        self.passable = False
        self.anim_timer = pygame.time.get_ticks()
        self.anim_frame_time = 50

        self.destroyed = False


    def update(self):
        if self.destroyed:
            if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
                self.image_index += 1
                if self.image_index >= len(self.image_list) - 1:
                    self.kill()
                self.image = self.image_list[self.image_index]
                self.anim_timer = pygame.time.get_ticks()
            for enemy in self.GAME.groups["enemies"]:
                if enemy.destroyed:
                    continue
                if not self.rect.colliderect(enemy):
                    continue
                if pygame.sprite.collide_mask(self, enemy):
                    enemy.destroy()
            if self.rect.colliderect(self.GAME.player):
                if pygame.sprite.collide_mask(self, self.GAME.player):
                    self.GAME.player.alive = False
                    self.GAME.player.action = "dead_anim"


    def destroy_soft_block(self):
        """Se o soft block foi destruído, altere o booleano destruído para True e defina o temporizador"""
        if not self.destroyed:
            self.anim_timer = pygame.time.get_ticks()
            self.destroyed = True
            self.GAME.level_matrix[self.row][self.col] = "_"


    def __repr__(self):
        return "'@'"


class Special_Soft_Block(Soft_Block):
    def __init__(self, game, images, group, row_num, col_num, size, special_type):
        super().__init__(game, images, group, row_num, col_num, size)

        self.special_type = special_type
        print((self.row, self.col))


    def kill(self):
        super().kill()
        self.place_special_block()


    def place_special_block(self):
        special_cell = Special(self.GAME,
                               self.GAME.ASSETS.specials[self.special_type][0],
                               self.special_type,
                               self.GAME.groups["specials"],
                               self.row, self.col, self.size)
        self.GAME.level_matrix[self.row][self.col] = special_cell
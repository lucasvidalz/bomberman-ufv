import pygame
from specials import Special
import gamesettings as gs
from abc import ABC, abstractmethod

class Block(pygame.sprite.Sprite, ABC):
    """Classe abstrata base para todos os tipos de blocos"""
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(group)
        self._game = game
        self._y_offset = gs.Y_OFFSET
        self._row = row_num
        self._col = col_num
        self._size = size
        self._x = self._col * self._size
        self._y = (self._row * self._size) + self._y_offset
        self._passable = True
        self._image_list = images
        self._image_index = 0
        self._image = self._image_list[self._image_index]
        self._rect = self._image.get_rect(topleft=(self._x, self._y))
        
        # Atributos diretos para compatibilidade com pygame
        self.image = self._image
        self.rect = self._rect

    @property
    def passable(self):
        return self._passable

    @passable.setter
    def passable(self, value):
        self._passable = value

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @abstractmethod
    def update(self):
        pass

    def draw(self, window, offset):
        window.blit(self._image, (self._rect.x - offset, self._rect.y))

    def __repr__(self):
        return "'#'"

class HardBlock(Block):
    """Blocos indestrutíveis"""
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(game, images, group, row_num, col_num, size)
        self._passable = False

    def update(self):
        pass

    def __repr__(self):
        return "'#'"

class SoftBlock(Block):
    """Blocos destrutíveis"""
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(game, images, group, row_num, col_num, size)
        self._passable = False
        self._anim_timer = pygame.time.get_ticks()
        self._anim_frame_time = 50
        self._destroyed = False

    def update(self):
        if self._destroyed:
            self._handle_destruction()
            self._check_collisions()

    def _handle_destruction(self):
        if pygame.time.get_ticks() - self._anim_timer >= self._anim_frame_time:
            self._image_index += 1
            if self._image_index >= len(self._image_list):
                self.kill()
            else:
                self._image = self._image_list[self._image_index]
                # Atualizar o atributo direto para compatibilidade com pygame
                self.image = self._image
            self._anim_timer = pygame.time.get_ticks()

    def _check_collisions(self):
        for enemy in self._game.groups["enemies"]:
            if enemy.destroyed:
                continue
            if not self._rect.colliderect(enemy.rect):
                continue
            if pygame.sprite.collide_mask(self, enemy):
                enemy.destroy()
                
        if self._rect.colliderect(self._game.player.rect):
            if pygame.sprite.collide_mask(self, self._game.player):
                self._game.player.alive = False
                self._game.player.action = "dead_anim"

    def destroy_soft_block(self):
        """Destrói o bloco macio"""
        if not self._destroyed:
            self._anim_timer = pygame.time.get_ticks()
            self._destroyed = True
            self._game.level_matrix[self._row][self._col] = "_"

    def __repr__(self):
        return "'@'"

class SpecialSoftBlock(SoftBlock):
    """Blocos macios que contêm power-ups especiais"""
    def __init__(self, game, images, group, row_num, col_num, size, special_type):
        super().__init__(game, images, group, row_num, col_num, size)
        self._special_type = special_type

    def kill(self):
        super().kill()
        self._place_special_block()

    def _place_special_block(self):
        special_cell = Special(self._game,
                             self._game.assets.specials[self._special_type][0],
                             self._special_type,
                             self._game.groups["specials"],
                             self._row, self._col, self._size)
        self._game.level_matrix[self._row][self._col] = special_cell

    def __repr__(self):
        return "'@'"
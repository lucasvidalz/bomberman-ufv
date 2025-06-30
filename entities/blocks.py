import pygame
from entities.specials import Special
import core.gamesettings as gs
from abc import ABC, abstractmethod

class Block(pygame.sprite.Sprite, ABC):
    """Classe abstrata base para todos os tipos de blocos"""
    # HERANÇA: Block herda de pygame.sprite.Sprite e ABC (Abstract Base Class)
    # ABC permite definir métodos abstratos que devem ser implementados pelas subclasses
    def __init__(self, game, images, group, row_num, col_num, size):
        # HERANÇA: Chama o construtor da classe pai (pygame.sprite.Sprite)
        super().__init__(group)
        # ENCAPSULAMENTO: Atributos privados protegem o estado interno dos blocos
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
        # ENCAPSULAMENTO: Property getter para acesso controlado à propriedade passable
        return self._passable

    @passable.setter
    def passable(self, value):
        # ENCAPSULAMENTO: Property setter para modificação controlada da propriedade
        self._passable = value

    @property
    def row(self):
        # ENCAPSULAMENTO: Property getter para acesso controlado à linha
        return self._row

    @property
    def col(self):
        # ENCAPSULAMENTO: Property getter para acesso controlado à coluna
        return self._col

    @abstractmethod
    def update(self):
        # POLIMORFISMO: Método abstrato que deve ser implementado pelas subclasses
        # Cada tipo de bloco terá sua própria lógica de atualização
        pass

    def draw(self, window, offset):
        # POLIMORFISMO: Método que pode ser sobrescrito por subclasses 
        # para implementar renderização específica
        window.blit(self._image, (self._rect.x - offset, self._rect.y))

    def __repr__(self):
        return "'#'"

class HardBlock(Block):
    """Blocos indestrutíveis"""
    # HERANÇA: HardBlock herda de Block, obtendo funcionalidades básicas de bloco
    def __init__(self, game, images, group, row_num, col_num, size):
        # HERANÇA: Chama o construtor da classe pai (Block)
        super().__init__(game, images, group, row_num, col_num, size)
        # ENCAPSULAMENTO: Define propriedade específica dos blocos duros
        self._passable = False

    def update(self):
        # POLIMORFISMO: Implementa o método abstrato update da classe pai
        # Blocos duros não precisam de atualização
        pass

    def __repr__(self):
        return "'#'"

class SoftBlock(Block):
    """Blocos destrutíveis"""
    # HERANÇA: SoftBlock herda de Block, obtendo funcionalidades básicas de bloco
    def __init__(self, game, images, group, row_num, col_num, size):
        # HERANÇA: Chama o construtor da classe pai (Block)
        super().__init__(game, images, group, row_num, col_num, size)
        # ENCAPSULAMENTO: Atributos privados específicos dos blocos macios
        self._passable = False
        self._anim_timer = pygame.time.get_ticks()
        self._anim_frame_time = 50
        self._destroyed = False

    def update(self):
        # POLIMORFISMO: Implementa o método abstrato update da classe pai
        # Blocos macios têm lógica específica de destruição
        if self._destroyed:
            self._handle_destruction()
            self._check_collisions()

    def _handle_destruction(self):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica de destruição
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
        # ENCAPSULAMENTO: Método privado que encapsula a verificação de colisões durante destruição
        for enemy in self._game.groups["enemies"]:
            if enemy.destroyed:
                continue
            if not self._rect.colliderect(enemy.rect):
                continue
            if pygame.sprite.collide_mask(self, enemy):
                enemy.destroy()
                
        if self._rect.colliderect(self._game.player.rect):
            if pygame.sprite.collide_mask(self, self._game.player):
                self._game.player._alive = False
                self._game.player.action = "dead_anim"

    def destroy_soft_block(self):
        """Destrói o bloco macio"""
        # ENCAPSULAMENTO: Método público que controla a destruição do bloco
        if not self._destroyed:
            self._anim_timer = pygame.time.get_ticks()
            self._destroyed = True
            self._game.level_matrix[self._row][self._col] = "_"

    def __repr__(self):
        return "'@'"

class SpecialSoftBlock(SoftBlock):
    """Blocos macios que contêm power-ups especiais"""
    # HERANÇA: SpecialSoftBlock herda de SoftBlock, obtendo funcionalidades 
    # de bloco macio e adicionando comportamento específico para power-ups
    def __init__(self, game, images, group, row_num, col_num, size, special_type):
        # HERANÇA: Chama o construtor da classe pai (SoftBlock)
        super().__init__(game, images, group, row_num, col_num, size)
        # ENCAPSULAMENTO: Atributo privado específico dos blocos especiais
        self._special_type = special_type

    def kill(self):
        # POLIMORFISMO: Sobrescreve o método kill da classe pai para adicionar 
        # comportamento específico de criação de power-up
        super().kill()
        self._place_special_block()

    def _place_special_block(self):
        # ENCAPSULAMENTO: Método privado que encapsula a criação do power-up
        special_cell = Special(self._game,
                             self._game.assets.specials[self._special_type][0],
                             self._special_type,
                             self._game.groups["specials"],
                             self._row, self._col, self._size)
        self._game.level_matrix[self._row][self._col] = special_cell

    def __repr__(self):
        return "'@'"
import pygame
import core.gamesettings as gs
from ui.info_panel import Scoring
from random import choice
from entities.character import Character

class Enemy(Character):
    """Classe base para todos os inimigos"""
    # HERANÇA: Enemy herda de Character, obtendo todas as funcionalidades básicas 
    # de personagem como movimento, animação, colisões, etc.
    def __init__(self, game, image_dict, group, type, row_num, col_num, size):
        # HERANÇA: Chama o construtor da classe pai (Character)
        super().__init__(game, image_dict, group, row_num, col_num, size)
        # ENCAPSULAMENTO: Atributos privados específicos dos inimigos
        self._type = type
        self._speed = gs.ENEMIES[self._type]["speed"]
        self._wall_hack = gs.ENEMIES[self._type]["wall_hack"]
        self._chase_player = gs.ENEMIES[self._type]["chase_player"]
        self._LoS = gs.ENEMIES[self._type]["LoS"] * size
        self._see_player_hack = gs.ENEMIES[self._type]["see_player_hack"]
        self._destroyed = False
        self._direction = "left"
        self._dir_mvmt = {
            "left": -self._speed, 
            "right": self._speed,
            "up": -self._speed, 
            "down": self._speed
        }
        self._change_dir_timer = pygame.time.get_ticks()
        self._dir_time = 1500
        self.action = f"walk_{self._direction}"
        self._anim_frame_time = 100
        self._anim_timer = pygame.time.get_ticks()
        self.image = self.image_dict[self.action][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self._start_pos = self.rect.center
        self._end_pos = self.GAME.player.rect.center

    @property
    def destroyed(self):
        # ENCAPSULAMENTO: Property getter para acesso controlado ao estado de destruição
        return self._destroyed

    @destroyed.setter
    def destroyed(self, value):
        # ENCAPSULAMENTO: Property setter para modificação controlada do estado
        self._destroyed = value

    @property
    def type(self):
        # ENCAPSULAMENTO: Property getter para acesso controlado ao tipo do inimigo
        return self._type
    #polimorfismo - exemplo real
    def update(self):
        # POLIMORFISMO: Sobrescreve o método update da classe pai (Character) 
        # para implementar comportamento específico dos inimigos
        self._movement()
        self._update_line_of_sight_with_player()
        self.animate(self.action)

    def draw(self, window, x_offset):
        # POLIMORFISMO: Sobrescreve o método draw da classe pai (Character) 
        # para implementar renderização específica dos inimigos
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))

    def _movement(self):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica de movimento dos inimigos
        if self._destroyed:
            return

        move_direction = self.action.split("_")[1]
        if move_direction in ["left", "right"]:
            self.x += self._dir_mvmt[move_direction]
        else:
            self.y += self._dir_mvmt[move_direction]

        directions = ["left", "right", "up", "down"]
        self._handle_collisions(move_direction, directions)
        self._handle_chase_player(directions)
        self._change_directions(directions)
        self.rect.update(self.x, self.y, self.size, self.size)

    def _handle_collisions(self, move_direction, directions):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica de colisões
        self._new_direction(self.GAME.groups["hard_block"], move_direction, directions)
        
        if not self._wall_hack:
            self._new_direction(self.GAME.groups["soft_block"], move_direction, directions)
            
        self._new_direction(self.GAME.groups["bomb"], move_direction, directions)

    def _handle_chase_player(self, directions):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica de perseguição do jogador
        if not self._chase_player:
            return
            
        if (self._check_LoS_distance() or
            self._intersecting_items_with_LoS("hard_block") or
            self._intersecting_items_with_LoS("soft_block") or
            (self._intersecting_items_with_LoS("bomb") and not self._see_player_hack)):
            return
            
        self._chase_the_player()

    def _collision_detection_blocks(self, group, direction):
        # ENCAPSULAMENTO: Método privado que encapsula a detecção de colisão com blocos
        for block in group:
            if not block.rect.colliderect(self.rect):
                continue
                
            if direction == "left" and self.rect.right > block.rect.right:
                self.x = block.rect.right
                return direction
            if direction == "right" and self.rect.left < block.rect.left:
                self.x = block.rect.left - self.size
                return direction
            if direction == "up" and self.rect.bottom > block.rect.bottom:
                self.y = block.rect.bottom
                return direction
            if direction == "down" and self.rect.top < block.rect.top:
                self.y = block.rect.top - self.size
                return direction
        return None

    def _new_direction(self, group, move_direction, directions):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica de mudança de direção
        dir = self._collision_detection_blocks(group, move_direction)
        if dir:
            directions.remove(dir)
            new_direction = choice(directions)
            self.action = f"walk_{new_direction}"
            self._change_dir_timer = pygame.time.get_ticks()

    def _change_directions(self, direction_list):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica de mudança automática de direção
        if (pygame.time.get_ticks() - self._change_dir_timer < self._dir_time or
            self.x % self.size != 0 or (self.y - gs.Y_OFFSET) % self.size != 0):
            return

        row = int((self.y - gs.Y_OFFSET) // self.size)
        col = int(self.x // self.size)

        if row % 2 == 0 or col % 2 == 0:
            return

        if not self._wall_hack:
            self._determine_if_direction_valid(direction_list, row, col)

        new_direction = choice(direction_list)
        self.action = f"walk_{new_direction}"
        self._change_dir_timer = pygame.time.get_ticks()

    def _determine_if_direction_valid(self, directions, row, col):
        # ENCAPSULAMENTO: Método privado que encapsula a validação de direções
        if self.GAME.level_matrix[row - 1][col] != "_":
            directions.remove("up")
        if self.GAME.level_matrix[row + 1][col] != "_":
            directions.remove("down")
        if self.GAME.level_matrix[row][col - 1] != "_":
            directions.remove("left")
        if self.GAME.level_matrix[row][col + 1] != "_":
            directions.remove("right")

        if len(directions) == 0:
            directions.append("left")

    def animate(self, action):
        # POLIMORFISMO: Sobrescreve o método animate da classe pai (Character) 
        # para implementar animação específica dos inimigos
        if pygame.time.get_ticks() - self._anim_timer >= self._anim_frame_time:
            self.index += 1
            if self._destroyed and self.index == len(self.image_dict[self.action]):
                self.kill()
                Scoring(self.GAME, self.GAME.groups["scores"], 
                       gs.SCORES[self._type], self.x, self.y)
            self.index = self.index % len(self.image_dict[self.action])
            self.image = self.image_dict[self.action][self.index]
            self._anim_timer = pygame.time.get_ticks()

    def destroy(self):
        # ENCAPSULAMENTO: Método público que controla a destruição do inimigo
        self._destroyed = True
        self.index = 0
        self.action = "death"
        self.image = self.image_dict[self.action][self.index]

    def _update_line_of_sight_with_player(self):
        # ENCAPSULAMENTO: Método privado que encapsula a atualização da linha de visão
        self._start_pos = self.rect.center
        self._end_pos = self.GAME.player.rect.center

    def _chase_the_player(self):
        # ENCAPSULAMENTO: Método privado que encapsula a lógica de perseguição
        enemy_col = self._start_pos[0] // self.size
        enemy_row = self._start_pos[1] // self.size
        player_col = self._end_pos[0] // self.size
        player_row = self._end_pos[1] // self.size

        if (enemy_col > player_col and 
            ((self.y - gs.Y_OFFSET) % self.size) + 32 == self.size//2):
            self.action = "walk_left"
        elif (enemy_col < player_col and 
              ((self.y - gs.Y_OFFSET) % self.size) + 32 == self.size//2):
            self.action = "walk_right"
        elif (enemy_row > player_row and 
              (self.x % self.size) + 32 == self.size//2):
            self.action = "walk_up"
        elif (enemy_row < player_row and 
              (self.x % self.size) + 32 == self.size//2):
            self.action = "walk_down"

        self._change_dir_timer = pygame.time.get_ticks()

    def _check_LoS_distance(self):
        # ENCAPSULAMENTO: Método privado que encapsula a verificação de distância da linha de visão
        x_dist = abs(self._end_pos[0] - self._start_pos[0])
        y_dist = abs(self._end_pos[1] - self._start_pos[1])
        return x_dist > self._LoS or y_dist > self._LoS

    def _intersecting_items_with_LoS(self, group):
        # ENCAPSULAMENTO: Método privado que encapsula a verificação de interseção com a linha de visão
        for item in self.GAME.groups[group]:
            if item.rect.clipline(self._start_pos, self._end_pos):
                return True
        return False

    def reset_character(self):
        pass  # Inimigos não são resetados
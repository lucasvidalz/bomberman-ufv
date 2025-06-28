import pygame
import gamesettings as gs
from info_panel import Scoring
from random import choice


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, image_dict, group, type, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game
        #  Tipo de inimigo (os atributos do inimigo dependem do tipo)
        self.type = type

        #  Atributos (dependendo do nosso tipo de inimigo)
        self.speed = gs.ENEMIES[self.type]["speed"]        #  Velocidade do inimigo
        self.wall_hack = gs.ENEMIES[self.type]["wall_hack"]  #  O inimigo pode atravessar paredes
        self.chase_player = gs.ENEMIES[self.type]["chase_player"]   #  O inimigo irá perseguir o jogador
        self.LoS = gs.ENEMIES[self.type]["LoS"] * size            #  Distância o inimigo pode ver o jogador
        self.see_player_hack = gs.ENEMIES[self.type]["see_player_hack"]      #  O inimigo pode ver o jogador através das paredes

        #  Coordenadas de geração da Matriz de Nível
        self.row = row_num
        self.col = col_num

        #  Coordenadas de Spawn do Inimigo
        self.size = size
        self.x = self.col * self.size
        self.y = (self.row * self.size) + gs.Y_OFFSET

        #  Outros atributos
        self.destroyed = False
        self.direction = "left"
        self.dir_mvmt = {"left": -self.speed, "right": self.speed,
                         "up": -self.speed, "down": self.speed}
        self.change_dir_timer = pygame.time.get_ticks()
        self.dir_time = 1500

        #  Animação e imagens inimigas
        self.index = 0
        self.action = f"walk_{self.direction}"
        self.image_dict = image_dict
        self.anim_frame_time = 100
        self.anim_timer = pygame.time.get_ticks()

        self.image = self.image_dict[self.action][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        #  Linha de visão inimiga
        self.start_pos = self.rect.center
        self.end_pos = self.GAME.player.rect.center


    def update(self):
        self.movement()
        self.update_line_of_sight_with_player()
        self.animate()


    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))
        #pygame.draw.line(window, "black", (self.start_pos[0] - x_offset, self.start_pos[1]),(self.end_pos[0] - x_offset, self.end_pos[1]), 2)


    def movement(self):
        """Método que incorpora todas as condições de movimento para permitir que o inimigo se mova
        a área de jogo"""
        # Retorna se o inimigo for destruído
        if self.destroyed:
            return

        # Move o inimigo ao longo do eixo x ou y
        move_direction = self.action.split("_")[1]
        if move_direction in ["left", "right"]:
            self.x += self.dir_mvmt[move_direction]
        else:
            self.y += self.dir_mvmt[move_direction]

        # Redefinir opções de direção
        directions = ["left", "right", "up", "down"]

        # Colisão com blocos rígidos
        self.new_direction(self.GAME.groups["hard_block"], move_direction, directions)

        # Colisão com Soft Blocks (somente se wall_hack for False)
        if not self.wall_hack:
            self.new_direction(self.GAME.groups["soft_block"], move_direction, directions)

        # Colisão com bombas
        self.new_direction(self.GAME.groups["bomb"], move_direction, directions)

        # Perseguir o jogador, se aplicável
        if self.chase_player:
            if self.check_LoS_distance():
                pass
            elif self.intersecting_items_with_LoS("hard_block"):
                pass
            elif self.intersecting_items_with_LoS("soft_block"):
                pass
            elif self.intersecting_items_with_LoS("bomb") and not self.see_player_hack:
                pass
            else:
                self.chase_the_player()

        # Mudar a direção se necessário
        self.change_directions(directions)

        # Atualizar posição
        self.rect.update(self.x, self.y, self.size, self.size)


    def collision_detection_blocks(self, group, direction):
        #  Detecção de colisão
        for block in group:
            #  compare cada bloco para colisão com personagem inimigo
            if block.rect.colliderect(self.rect):
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


    def new_direction(self, group, move_direction, directions):
        dir = self.collision_detection_blocks(group, move_direction)
        if dir:
            directions.remove(dir)
            new_direction = choice(directions)
            self.action = f"walk_{new_direction}"
            self.change_dir_timer = pygame.time.get_ticks()


    def change_directions(self, direction_list):
        """Mudar de direção aleatoriamente após um determinado período de tempo decorrido"""
        # se o tempo não tiver decorrido, retorna fora do método
        if pygame.time.get_ticks() - self.change_dir_timer < self.dir_time:
            return

        #  se as coordenadas inimigas não estiverem alinhadas com as coordenadas da grade.
        if self.x % self.size != 0 or (self.y - gs.Y_OFFSET) % self.size != 0:
            return

        #  Calcule em qual linha e coluna o inimigo está atualmente.
        row = int((self.y - gs.Y_OFFSET) // self.size)
        col = int(self.x // self.size)

        #  Se a célula na linha/coluna não for uma interseção de 4 vias, retorne do método
        if row % 2 == 0 or col % 2 == 0:
            return

        #  Verifica as 4 direções para ver se o movimento é possível, atualize a lista de direções
        if self.wall_hack == False:
            self.determine_if_direction_valid(direction_list, row, col)

        #  Seleciona aleatoriamente uma nova direção na lista restante de direções
        new_direction = choice(direction_list)
        self.action = f"walk_{new_direction}"

        #  Redefinir o temporizador de mudança de direção
        self.change_dir_timer = pygame.time.get_ticks()
        return


    def determine_if_direction_valid(self, directions, row, col):
        """Verifique as 4 direções para determinar se o movimento é possível"""
        if self.GAME.level_matrix[row - 1][col] != "_":
            directions.remove("up")
        if self.GAME.level_matrix[row + 1][col] != "_":
            directions.remove("down")
        if self.GAME.level_matrix[row][col - 1] != "_":
            directions.remove("left")
        if self.GAME.level_matrix[row][col + 1] != "_":
            directions.remove("right")

        # se a lista de rotas estiver vazia, insira "esquerda"
        if len(directions) == 0:
            directions.append("left")
        return


    def animate(self):
        """Percorre as imagens de animação inimigas"""
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            if self.destroyed and self.index == len(self.image_dict[self.action]):
                self.kill()
                Scoring(self.GAME, self.GAME.groups["scores"], gs.SCORES[self.type], self.x, self.y)
            self.index = self.index % len(self.image_dict[self.action])
            self.image = self.image_dict[self.action][self.index]
            self.anim_timer = pygame.time.get_ticks()


    def destroy(self):
        """Desativa o inimigo quando morto"""
        self.destroyed = True
        self.index = 0
        self.action = "death"
        self.image = self.image_dict[self.action][self.index]


    def update_line_of_sight_with_player(self):
        """Atualiza as posições dos personagens inimigos e dos jogadores"""
        self.start_pos = self.rect.center
        self.end_pos = self.GAME.player.rect.center


    def chase_the_player(self):
        """Muda a direção em direção ao jogador se estiver na linha de visão"""
        # Converte coordenadas de pixel em linhas/colunas
        enemy_col = self.start_pos[0] // self.size
        enemy_row = self.start_pos[1] // self.size
        player_col = self.end_pos[0] // self.size
        player_row = self.end_pos[1] // self.size

        if enemy_col > player_col and ((self.y - gs.Y_OFFSET) % self.size) + 32 == self.size//2:
            self.action = "walk_left"
        elif enemy_col < player_col and ((self.y - gs.Y_OFFSET) % self.size) + 32 == self.size//2:
            self.action = "walk_right"
        elif enemy_row > player_row and (self.x % self.size) + 32 == self.size//2:
            self.action = "walk_up"
        elif enemy_row < player_row and (self.x % self.size) + 32 == self.size//2:
            self.action = "walk_down"

            #  Atualiza o temporizador de mudança de direção do personagem inimigo
            self.change_dir_timer = pygame.time.get_ticks()


    def check_LoS_distance(self):
        """Retorna Verdadeiro ou Falso, se a distância entre jogador e inimigo for menor que o atributo LoS"""
        x_dist = abs(self.end_pos[0] - self.start_pos[0])
        y_dist = abs(self.end_pos[1] - self.start_pos[1])

        if x_dist > self.LoS or y_dist > self.LoS:
            return True

        return False


    def intersecting_items_with_LoS(self, group):
        """Retorna Verdadeiro ou Falso, se o item estiver obstruindo o LoS"""
        for item in self.GAME.groups[group]:
            if item.rect.clipline(self.start_pos, self.end_pos):
                return True
        return False
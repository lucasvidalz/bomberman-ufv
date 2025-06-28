import pygame
import gamesettings as gs


class Character(pygame.sprite.Sprite):
    def __init__(self, game, image_dict, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game

        # Sons de personagens
        self.walk_sound_timer = pygame.time.get_ticks()
        self.death_sound_timer = pygame.time.get_ticks()

        self.death_sound_play = False

        self.delay = False
        self.delay_timer = pygame.time.get_ticks()

        #  Posição da Matriz de Nivel
        self.row_num = row_num
        self.col_num = col_num
        self.size = size

        self.set_player(image_dict)

        self.score = 0
        self.lives = 1


    def input(self, events=None):
        if events is None:
            events = pygame.event.get()
            
        for event in events:
            #  Verifique se a cruz vermelha foi clicada
            if event.type == pygame.QUIT:
                self.GAME.MAIN.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.GAME.MAIN.run = False
                elif event.key == pygame.K_SPACE:
                    print(f"ESPAÇO pressionado! Bombs planted: {self.bombs_planted}, Bomb limit: {self.bomb_limit}")
                    row, col = ((self.rect.centery - gs.Y_OFFSET)//gs.SIZE, self.rect.centerx // self.size)
                    print(f"Posição calculada: row={row}, col={col}")
                    print(f"Conteúdo da matriz nessa posição: {self.GAME.level_matrix[row][col]}")
                    if self.GAME.level_matrix[row][col] == "_" and self.bombs_planted < self.bomb_limit:
                        print("Plantando bomba!")
                        Bomb(self.GAME, self.GAME.ASSETS.bomb["bomb"],
                             self.GAME.groups["bomb"], self.power, row, col, gs.SIZE, self.remote)
                    else:
                        print(f"Não pode plantar bomba. Matriz: {self.GAME.level_matrix[row][col]}, Bombs: {self.bombs_planted}/{self.bomb_limit}")
                elif event.key == pygame.K_LCTRL and self.remote and self.GAME.groups["bomb"]:
                    bomb_list = self.GAME.groups["bomb"].sprites()
                    bomb_list[-1].explode()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.move("walk_right")
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.move("walk_left")
        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.move("walk_up")
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.move("walk_down")


    def update(self):
        if self.invincibility == False:
            #  Se houver chamas/explosões, execute uma verificação de colisão
            if len(self.GAME.groups["explosions"]) > 0 and self.flame_pass == False:
                self.deadly_collisions(self.GAME.groups["explosions"])

            #  Execute a detecção de colisão com inimigos
            self.deadly_collisions(self.GAME.groups["enemies"])

        #  reproduzir animação de morte
        if self.action == "dead_anim":
            self.animate(self.action)

        #  Contagem regressiva do temporizador de invencibilidade
        if not self.invincibility:
            return

        if pygame.time.get_ticks() - self.invincibility_timer >= 20000:
            self.invincibility = False
            self.invincibility_timer = None


    def draw(self, window, offset):
        if self.death_sound_play == False and self.delay == False:
            window.blit(self.image, (self.rect.x - offset, self.rect.y))
        #pygame.draw.rect(window, gs.RED, (self.rect.x - offset, self.rect.y, 64, 64), 1)


    def animate(self, action):
        """Alterna entre imagens para animar o movimento"""
        if self.delay == True:
            if pygame.time.get_ticks() - self.delay_timer >= 400 and \
                self.death_sound_play == False:
                self.death_sound_play = True
                self.death_sound_timer = pygame.time.get_ticks()
                self.GAME.ASSETS.sounds["BM - 09 Miss.mp3"].play()
                self.index = len(self.image_dict[action]) - 1
                self.delay = False
                return
            return

        if self.death_sound_play == True:
            if pygame.time.get_ticks() - self.death_sound_timer >= 2500:
                self.reset_player()
                return
            return

        if pygame.time.get_ticks() - self.anim_time_set >= self.anim_time:
            self.index += 1
            if self.index == len(self.image_dict[action]):
                self.index = 0
                if self.action == "dead_anim" and self.delay == False:
                    self.delay = True
                    self.delay_timer = pygame.time.get_ticks()
                    return
            #  self.index = self.index % len(self.image_dics[action])

            self.image = self.image_dict[action][self.index]
            self.anim_time_set = pygame.time.get_ticks()


    def move(self, action):
        """Lida com o movimento e as animações do personagem"""
        #  se o jogador não estiver vivo, não se mova
        if not self.alive:
            return

        #  Verifica se a ação é diferente da self.action atual, redefina o número do índice para 0
        if action != self.action:
            self.action = action
            self.index = 0

        direction = {"walk_left": -self.speed, "walk_right": self.speed, "walk_up": -self.speed, "walk_down": self.speed}

        #  Altera as coordenadas x e y do jogador com base no argumento de ação
        if action == "walk_left" or action == "walk_right":
            self.x += direction[action]
        elif action == "walk_up" or action == "walk_down":
            self.y += direction[action]

        #  Reproduz o som do personagem ao se mover
        if pygame.time.get_ticks() - self.walk_sound_timer >= 200:
            if self.action in ["walk_left", "walk_right"]:
                self.GAME.ASSETS.sounds["Bomberman SFX (1).wav"].play()
            elif self.action in ["walk_up", "walk_down"]:
                self.GAME.ASSETS.sounds["Bomberman SFX (2).wav"].play()
            self.walk_sound_timer = pygame.time.get_ticks()

        #  Chama o método de animação
        self.animate(action)

        #  Encaixa o player nas coordenadas da grade, facilitando a navegação
        self.snap_to_grid(action)

        #  Verifica se a posição x, y está na área de jogo
        self.play_area_restriction(64, (gs.COLS - 1) * 64, gs.Y_OFFSET + 64, ((gs.ROWS-1) * 64) + gs.Y_OFFSET)

        #  Atualiza o retângulo do player
        self.rect.topleft = (self.x, self.y)

        #  Verifica se há colisão entre o jogador e vários itens
        self.collision_detection_items(self.GAME.groups["hard_block"])
        if self.wall_hack == False:
            self.collision_detection_items(self.GAME.groups["soft_block"])
        if self.bomb_hack == False:
            self.collision_detection_items(self.GAME.groups["bomb"])

        #  Atualiza a posição X da câmera do jogo com a posição x do jogador
        self.GAME.update_x_camera_offset_player_position(self.rect.x)


    def collision_detection_items(self, item_list):
        for item in item_list:
            if self.rect.colliderect(item) and item.passable == False:
                if self.action == "walk_right":
                    if self.rect.right > item.rect.left:
                        self.rect.right = item.rect.left
                        self.x, self.y = self.rect.topleft
                        return
                if self.action == "walk_left":
                    if self.rect.left < item.rect.right:
                        self.rect.left = item.rect.right
                        self.x, self.y = self.rect.topleft
                        return
                if self.action == "walk_up":
                    if self.rect.top < item.rect.bottom:
                        self.rect.top = item.rect.bottom
                        self.x, self.y = self.rect.topleft
                        return
                if self.action == "walk_down":
                    if self.rect.bottom > item.rect.top:
                        self.rect.bottom = item.rect.top
                        self.x, self.y = self.rect.topleft
                        return


    def snap_to_grid(self, action):
        """Encaixa o player nas coordenadas da grade, facilitando a navegação"""
        x_pos = self.x % gs.SIZE
        y_pos = (self.y - gs.Y_OFFSET) % gs.SIZE
        if action in ["walk_up", "walk_down"]:
            if x_pos <= 12:
                self.x = self.x - x_pos
            if x_pos >= 52:
                self.x = self.x + (gs.SIZE - x_pos)
        elif action in ["walk_left", "walk_right"]:
            if y_pos <= 12:
                self.y = self.y - y_pos
            if y_pos >= 52:
                self.y = self.y + (gs.SIZE - y_pos)


    def play_area_restriction(self, left_x, right_x, top_y, bottom_y):
        """Verifica as coordenadas do jogador para garantir que permaneça dentro da área de jogo"""
        if self.x < left_x:
            self.x = left_x
        elif self.x > right_x:
            self.x = right_x
        elif self.y < top_y:
            self.y = top_y
        elif self.y > bottom_y:
            self.y = bottom_y


    def set_player_position(self):
        """Posição do personagem"""
        #  Posição do personagem
        self.x = self.col_num * self.size
        self.y = (self.row_num * self.size) + gs.Y_OFFSET


    def set_player_images(self):
        """Conjunto de imagens de personagens"""
        self.image = self.image_dict[self.action][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def set_player(self, image_dict):
        """Atributos iniciais do personagem"""
        self.set_player_position()

        #  Atributos de personagem
        self.alive = True
        self.speed = 3
        self.bomb_limit = 2
        self.remote = True
        self.power = 1
        self.wall_hack = False
        self.bomb_hack = True
        self.flame_pass = False
        self.invincibility = False
        self.invincibility_timer = None

        #  Ação do personagem
        self.action = "walk_right"

        #  Bombas Plantadas
        self.bombs_planted = 0

        #  Exibição de caracteres
        self.index = 0
        self.anim_time = 50
        self.anim_time_set = pygame.time.get_ticks()
        self.image_dict = image_dict
        self.set_player_images()

        self.death_sound_play = False


    def reset_player(self):
        self.lives -= 1
        if self.lives < 0:
            self.GAME.game_on = False
            self.GAME.check_top_score(self.score)
            self.GAME.start_screen_music.play(loops=-1)
            self.GAME.music_playing = False
            #self.GAME.MAIN.run = False
            return
        self.GAME.save_game()
        self.GAME.regenerate_stage()
        self.set_player(self.image_dict)


    def deadly_collisions(self, group):
        if not self.alive:
            return

        for item in group:
            if not self.rect.colliderect(item.rect):
                continue
            if pygame.sprite.collide_mask(self, item):
                self.action = "dead_anim"
                self.alive = False
                self.GAME.bg_music.stop()
                self.GAME.bg_music_special.stop()
                self.GAME.ASSETS.sounds["Bomberman SFX (5).wav"].play()
                return


    def update_score(self, score):
        """Atualiza a pontuação do jogador"""
        self.score += score
        
    def __str__(self):
        return f"Jogador - Score: {self.score} | Vidas: {self.lives} | Posição: ({self.row_num},{self.col_num})"


class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, image_list, group, power, row_num, col_num, size, remote):
        super().__init__(group)
        self.GAME = game

        #  Posição da Matriz de Nível
        self.row = row_num
        self.col = col_num

        #  Coordenadas
        self.size = size
        self.x = self.col * self.size
        self.y = (self.row * self.size) + gs.Y_OFFSET

        #  Atributos da bomba
        self.bomb_counter = 1
        self.bomb_timer = 12
        self.passable = True
        self.remote = remote
        self.power = power

        #  imagem
        self.index = 0
        self.image_list = image_list
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        #  Configurações de animação
        self.anim_length = len(self.image_list)
        self.anim_frame_time = 200
        self.anim_timer = pygame.time.get_ticks()

        #  Inserir na matriz de nível
        self.insert_bomb_into_grid()

        #  Reproduzir som quando a bomba for colocada
        self.GAME.ASSETS.sounds["Bomberman SFX (3).wav"].play()


    def update(self):
        self.animation()
        self.planted_bomb_player_collision()
        if self.bomb_counter == self.bomb_timer and not self.remote:
            self.explode()


    def draw(self, window, offset):
        window.blit(self.image, (self.rect.x - offset, self.rect.y))


    def insert_bomb_into_grid(self):
        """Adiciona o objeto bomba à matriz de nível"""
        self.GAME.level_matrix[self.row][self.col] = self
        self.GAME.player.bombs_planted += 1


    def animation(self):
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            self.index = self.index % self.anim_length
            self.image = self.image_list[self.index]
            self.anim_timer = pygame.time.get_ticks()
            self.bomb_counter += 1


    def remove_bomb_from_grid(self):
        """Remove o objeto bomba da matriz de nível"""
        self.GAME.level_matrix[self.row][self.col] = "_"
        self.GAME.player.bombs_planted -= 1


    def explode(self):
        """Destroi a bomba e remove da matriz de nível"""
        self.kill()
        Explosion(self.GAME, self.GAME.ASSETS.explosions, "centre", self.power,
                  self.GAME.groups["explosions"], self.row, self.col, self.size)
        self.remove_bomb_from_grid()


    def planted_bomb_player_collision(self):
        if not self.passable:
            return
        if not self.rect.colliderect(self.GAME.player):
            self.passable = False


    def __repr__(self):
        return "'!'"


class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, image_dict, image_type, power, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game

        #  Posição da Matriz de Nível
        self.row_num = row_num
        self.col_num = col_num

        #  Coordenadas Sprite
        self.size = size
        self.y = (self.row_num * self.size) + gs.Y_OFFSET
        self.x = self.col_num * self.size

        #  Imagem de explosão e animações
        self.index = 0
        self.anim_frame_time = 75
        self.anim_timer = pygame.time.get_ticks()

        self.image_dict = image_dict
        self.image_type = image_type

        self.image = self.image_dict[self.image_type][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        #  Força
        self.power = power
        self.passable = False
        self.calculate_explosive_path()

        #  Reproduz som de explosão
        self.GAME.ASSETS.sounds["Bomberman SFX (7).wav"].play()


    def update(self):
        self.animate()


    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))


    def animate(self):
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            if self.index == len(self.image_dict[self.image_type]):
                self.kill()
                return
            self.image = self.image_dict[self.image_type][self.index]
            self.anim_timer = pygame.time.get_ticks()


    def calculate_explosive_path(self):
        """Explode células adjacentes, dependendo da energia e das células disponíveis"""
        #                   esquerda, direita, cima, baixo
        valid_directions = [True, True, True, True]
        for power_cell in range(self.power):
            #  Obtem uma lista das 4 direções, tupla de valores de células
            directions = self.calculate_direction_cells(power_cell)
            #  Verifica as células em cada direção de acordo com a lista de instruções acima
            for ind, dir in enumerate(directions):
                #  Se a direção correspondente na lista valid_directions for Falsa, pule
                if not valid_directions[ind]:
                    continue
                #  Se a célula atual que está sendo verificada for uma célula vazia, verifique a próxima célula nessa direção
                #  para determinar o tipo de imagem a ser exibida, seja ela intermediária ou final
                if self.GAME.level_matrix[dir[0]][dir[1]] == "_":
                    #  se for o fim da faixa de potência, use a peça final
                    if power_cell == self.power - 1:
                        FireBall(self.image_dict[dir[4]], self.GAME.groups["explosions"], dir[0], dir[1], gs.SIZE)
                    #  Verifica se a próxima célula na sequência é uma barreira, use a peça final se for verdade,
                    #  e altere as direções válidas para False
                    elif self.GAME.level_matrix[dir[2]][dir[3]] in self.GAME.groups["hard_block"].sprites():
                        FireBall(self.image_dict[dir[4]], self.GAME.groups["explosions"], dir[0], dir[1], gs.SIZE)
                        valid_directions[ind] = False
                    #  se a próxima célula na sequência não for uma barreira e não for o fim do poder da chama, use a imagem intermediária
                    else:
                        FireBall(self.image_dict[dir[5]], self.GAME.groups["explosions"], dir[0], dir[1], gs.SIZE)
                #  Se a célula atual que está sendo verificada não estiver vazia, mas for uma bomba, detone a bomba
                elif self.GAME.level_matrix[dir[0]][dir[1]] in self.GAME.groups["bomb"].sprites():
                    self.GAME.level_matrix[dir[0]][dir[1]].explode()
                    valid_directions[ind] = False
                #  Se a célula atual que está sendo verificada não estiver vazia, mas for um bloco flexível - destrua-a.
                elif self.GAME.level_matrix[dir[0]][dir[1]] in self.GAME.groups["soft_block"].sprites():
                    self.GAME.level_matrix[dir[0]][dir[1]].destroy_soft_block()
                    valid_directions[ind] = False
                #  Se a célula atual que está sendo verificada não estiver vazia, mas for um bloco especial
                elif self.GAME.level_matrix[dir[0]][dir[1]] in self.GAME.groups["specials"].sprites():
                    self.GAME.level_matrix[dir[0]][dir[1]].hit_by_explosion()
                    valid_directions[ind] = False
                #  Se a célula atual que está sendo verificada não for uma célula vazia, ou uma bomba, ou uma célula suave, ou especial
                else:
                    valid_directions[ind] = False
                    continue


    def calculate_direction_cells(self, cell):
        """Retorna uma lista das quatro células nas direções para cima e para baixo, esquerda e direita"""
        left = (self.row_num, self.col_num - (cell + 1),  # Verifica a célula imediatamente à esquerda
                self.row_num, self.col_num - (cell + 2),  # Verifica a célula à esquerda disso
                "left_end", "left_mid")
        right = (self.row_num, self.col_num + (cell + 1),  # Verifica a célula imediatamente à direita
                self.row_num, self.col_num + (cell + 2),  # Verifica a célula à direita disso
                "right_end", "right_mid")
        up = (self.row_num - (cell + 1), self.col_num,  # Verifica a célula imediatamente
              self.row_num - (cell + 2), self.col_num,  #  Verifique a célula acima disso
              "up_end", "up_mid")
        down = (self.row_num + (cell + 1), self.col_num,  # Verifica a célula imediatamente inativa
              self.row_num + (cell + 2), self.col_num,  # Verifica a célula abaixo disso
              "down_end", "down_mid")
        return [left, right, up, down]


class FireBall(pygame.sprite.Sprite):
    def __init__(self, image_list, group, row_num, col_num, size):
        super().__init__(group)
        self.row_num = row_num
        self.col_num = col_num

        self.size = size
        self.y = self.row_num * self.size + gs.Y_OFFSET
        self.x = self.col_num * self.size

        self.index = 0
        self.anim_frame_time = 75
        self.anim_timer = pygame.time.get_ticks()
        self.image_list = image_list
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.passable = False


    def update(self):
        self.animate()


    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))


    def animate(self):
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            if self.index == len(self.image_list):
                self.kill()
                return
            self.image = self.image_list[self.index]
            self.anim_timer = pygame.time.get_ticks()
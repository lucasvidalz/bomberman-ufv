import pygame
from character import Character
from enemy import Enemy
from blocks import Hard_Block, Soft_Block, Special_Soft_Block
from random import choice, randint
from info_panel import InfoPanel
import gamesettings as gs


class Game:
    def __init__(self, main, assets):
        # Link com a classe principal e ativos
        self.MAIN = main
        self.ASSETS = assets

        # Deslocamento da câmera
        self.camera_x_offset = 0

        # Grupos
        self.groups = {
            "hard_block": pygame.sprite.Group(),
            "soft_block": pygame.sprite.Group(),
            "bomb": pygame.sprite.Group(),
            "specials": pygame.sprite.Group(),
            "explosions": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(),
            "player": pygame.sprite.Group(),
            "scores": pygame.sprite.Group()
        }

        # Transição de nível
        self.transition = False
        self.level_transition = None

        # Configurações do jogo
        self.game_on = False
        self.point_position = [(384, 530), (384, 580)]
        self.point_pos = 0
        self.pointer_pos = self.point_position[self.point_pos]

        self.music_playing = False
        self.start_screen_music = self.ASSETS.sounds["BM - 01 Title Screen.mp3"]
        self.bg_music = self.ASSETS.sounds["BM - 03 Main BGM.mp3"]
        self.bg_music_special = self.ASSETS.sounds["BM - 04 Power-Up Get.mp3"]
        self.stage_ending_music = self.ASSETS.sounds["BM - 05 Stage Clear.mp3"]
        self.music_volume = 0.5
        self.sfx_volume = 0.5

        self.start_screen_music.play(loops=-1)

        self.top_score = 0
        self.top_score_img = self.top_score_image()
        
        self.start_screen_music.set_volume(self.music_volume)
        self.bg_music.set_volume(self.music_volume)
        self.bg_music_special.set_volume(self.music_volume)
        self.stage_ending_music.set_volume(self.music_volume)

        # Inicializa atributos que podem ser None
        self.player = None
        self.level_info = None
        self.level_matrix = None
        self.level = 0
        self.level_special = None

    def input(self, events):
        if not self.game_on:
            for event in events:
                if event.type == pygame.QUIT:
                    self.MAIN.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.point_pos -= 1
                        if self.point_pos < 0:
                            self.point_pos = 1
                    if event.key == pygame.K_DOWN:
                        self.point_pos += 1
                        if self.point_pos > 1:
                            self.point_pos = 0
                    self.pointer_pos = self.point_position[self.point_pos]

                    if event.key == pygame.K_1:  # Aumentar Música
                        self.music_volume = min(1.0, self.music_volume + 0.1)
                        pygame.mixer.music.set_volume(self.music_volume)
                        self.start_screen_music.set_volume(self.music_volume)
                        self.bg_music.set_volume(self.music_volume)
                        self.bg_music_special.set_volume(self.music_volume)
                        self.stage_ending_music.set_volume(self.music_volume)
                        print(f"Volume Música: {self.music_volume:.1f}")

                    if event.key == pygame.K_2:  # Diminuir Música
                        self.music_volume = max(0.0, self.music_volume - 0.1)
                        pygame.mixer.music.set_volume(self.music_volume)
                        self.start_screen_music.set_volume(self.music_volume)
                        self.bg_music.set_volume(self.music_volume)
                        self.bg_music_special.set_volume(self.music_volume)
                        self.stage_ending_music.set_volume(self.music_volume)
                        print(f"Volume Música: {self.music_volume:.1f}")

                    if event.key == pygame.K_3:  # Aumentar Efeitos
                        self.sfx_volume = min(1.0, self.sfx_volume + 0.1)
                        for sound in self.ASSETS.sounds.values():
                            sound.set_volume(self.sfx_volume)
                        print(f"Volume SFX: {self.sfx_volume:.1f}")

                    if event.key == pygame.K_4:  # Diminuir Efeitos
                        self.sfx_volume = max(0.0, self.sfx_volume - 0.1)
                        for sound in self.ASSETS.sounds.values():
                            sound.set_volume(self.sfx_volume)
                        print(f"Volume SFX: {self.sfx_volume:.1f}")

                    if event.key == pygame.K_ESCAPE:
                        self.bg_music.stop()
                        self.bg_music_special.stop()
                        self.stage_ending_music.stop()
                        self.start_screen_music.play(-1)
                        self.start_screen_music.set_volume(self.music_volume)
                        self.game_on = False
                        print("Jogador voltou ao menu inicial.")    

                    if event.key == pygame.K_RETURN:
                        if self.point_pos == 0:
                            self.new_game()
                        elif self.point_pos == 1:
                            self.load_game()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    print(f"Clique do mouse em: x={mouse_x}, y={mouse_y}")
                    start_rect = pygame.Rect(384, 530, 256, 40)
                    continue_rect = pygame.Rect(384, 580, 256, 40)
                    if start_rect.collidepoint(mouse_x, mouse_y):
                        print("Clique detectado em START!")
                        self.point_pos = 0
                        self.pointer_pos = self.point_position[self.point_pos]
                        self.new_game()
                    elif continue_rect.collidepoint(mouse_x, mouse_y):
                        print("Clique detectado em CONTINUE!")
                        self.point_pos = 1
                        self.pointer_pos = self.point_position[self.point_pos]
                        self.load_game()
            return

        if self.player is not None:
            for event in events:
                if event.type == pygame.QUIT:
                    self.MAIN.run = False
                    return
            self.player.input(events)

    def update(self):
        if not self.game_on:
            return

        if self.transition and self.level_transition is not None:
            self.level_transition.update()
            return

        if (self.game_on and not self.transition and not self.music_playing and 
            len(self.groups["enemies"].sprites()) > 0):
            self.music_playing = True
            self.bg_music.play(loops=-1)

        if (len(self.groups["enemies"].sprites()) == 0 and 
            self.music_playing):
            self.music_playing = False
            self.bg_music.stop()
            self.bg_music_special.stop()
            self.stage_ending_music.play()

        if self.level_info is not None:
            self.level_info.update()

        for value in self.groups.values():
            for item in value:
                item.update()

        if self.groups["explosions"]:
            killed_enemies = pygame.sprite.groupcollide(
                self.groups["explosions"], self.groups["enemies"], False, False)
            if killed_enemies:
                for flame, enemies in killed_enemies.items():
                    for enemy in enemies:
                        if pygame.sprite.collide_mask(flame, enemy):
                            enemy.destroy()

    def draw(self, window):
        window.fill(gs.GREY)

        if not self.game_on:
            window.blit(self.ASSETS.start_screen, (0, 0))
            window.blit(self.ASSETS.start_screen_pointer, self.pointer_pos)
            if self.top_score_img:
                for i, img in enumerate(self.top_score_img):
                    window.blit(img, (638 + ((i - len(self.top_score_img)) * 32), 655))
            return

        if self.transition and self.level_transition is not None:
            self.level_transition.draw(window)
            return

        if self.level_info is not None:
            self.level_info.draw(window)

        if self.level_matrix is not None:
            for row_num, row in enumerate(self.level_matrix):
                for col_num, col in enumerate(row):
                    window.blit(
                        self.ASSETS.background["background"][0],
                        ((col_num * gs.SIZE) - self.camera_x_offset, 
                         (row_num * gs.SIZE) + gs.Y_OFFSET))
        else:
            window.fill(gs.BLACK)

        for value in self.groups.values():
            for item in value:
                item.draw(window, self.camera_x_offset)

    def generate_level_matrix(self, rows, cols):
        """Gere a matriz de nível básico"""
        matrix = []
        for row in range(rows + 1):
            line = []
            for col in range(cols + 1):
                line.append("_")
            matrix.append(line)
        self.insert_hard_blocks_into_matrix(matrix)
        self.insert_soft_blocks_into_matrix(matrix)
        for special in gs.SPECIALS.keys():
            if special != "exit":
                self.insert_power_up_into_matrix(matrix, special)
        self.insert_power_up_into_matrix(matrix, "exit")
        self.insert_enemies_into_level(matrix)
        return matrix

    def insert_hard_blocks_into_matrix(self, matrix):
        """Insere todos os blocos de barreira rígida na matriz de nível"""
        for row_num, row in enumerate(matrix):
            for col_num, col in enumerate(row):
                if (row_num == 0 or row_num == len(matrix)-1 or 
                    col_num == 0 or col_num == len(row)-1 or 
                    (row_num % 2 == 0 and col_num % 2 == 0)):
                    matrix[row_num][col_num] = Hard_Block(
                        self, self.ASSETS.hard_block["hard_block"],
                        self.groups["hard_block"], row_num, col_num, gs.SIZE)
        return

    def insert_soft_blocks_into_matrix(self, matrix):
        """Insire aleatoriamente blocos flexíveis na matriz de nível"""
        for row_num, row in enumerate(matrix):
            for col_num, col in enumerate(row):
                if (row_num == 0 or row_num == len(matrix) - 1 or
                    col_num == 0 or col_num == len(row) - 1 or
                    (row_num % 2 == 0 and col_num % 2 == 0)):
                    continue
                elif row_num in [2, 3, 4] and col_num in [1, 2, 3]:
                    continue
                else:
                    cell = choice(["@", "_", "_", "_"])
                    if cell == "@":
                        cell = Soft_Block(
                            self, self.ASSETS.soft_block["soft_block"],
                            self.groups["soft_block"], row_num, col_num, gs.SIZE)
                    matrix[row_num][col_num] = cell
        return

    def insert_power_up_into_matrix(self, matrix, special):
        """Insire aleatoriamente o bloco especial na matriz de nível"""
        power_up = special
        valid = False
        while not valid:
            row = randint(0, gs.ROWS)
            col = randint(0, gs.COLS)
            if (row == 0 or row == len(matrix) - 1 or 
                col == 0 or col == len(matrix[0]) - 1):
                continue
            elif row % 2 == 0 and col % 2 == 0:
                continue
            elif row in [2, 3, 4] and col in [1, 2, 3]:
                continue
            elif matrix[row][col] != "_":
                continue
            else:
                valid = True
        cell = Special_Soft_Block(
            self,
            self.ASSETS.soft_block["soft_block"],
            self.groups["soft_block"],
            row, col, gs.SIZE, power_up)
        matrix[row][col] = cell

    def update_x_camera_offset_player_position(self, player_x_pos):
        """Atualiza a posição x da câmera de acordo com a posição x do jogador"""
        if player_x_pos >= 576 and player_x_pos <= 1280:
            self.camera_x_offset = player_x_pos - 576

    def insert_enemies_into_level(self, matrix, enemies=None):
        """Insire inimigos aleatoriamente no nível"""
        if self.player is None:
            return

        enemies_list = self.select_enemies_to_spawn() if enemies is None else enemies
        pl_col = self.player.col_num
        pl_row = self.player.row_num

        for enemy in enemies_list:
            valid_choice = False
            while not valid_choice:
                row = randint(0, gs.ROWS)
                col = randint(0, gs.COLS)

                if (row in [pl_row-3, pl_row-2, pl_row-1, pl_row, 
                           pl_row+1, pl_row+2, pl_row+3] and 
                    col in [pl_col-3, pl_col-2, pl_col-1, pl_col, 
                           pl_col+1, pl_col+2, pl_col+3]):
                    continue
                elif matrix[row][col] == "_":
                    valid_choice = True
                    Enemy(
                        self, self.ASSETS.enemies[enemy], 
                        self.groups["enemies"], enemy, row, col, gs.SIZE)
                else:
                    continue

    def regenerate_stage(self):
        """Reinicia um estágio/nível"""
        for key in self.groups.keys():
            if key == "player":
                continue
            self.groups[key].empty()

        self.level_matrix.clear()
        if self.level_info is not None:
            self.level_info.set_timer()
        self.level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)
        self.camera_x_offset = 0
        self.level_transition = LevelTransition(self, self.ASSETS, self.level)
        self.music_playing = False

    def select_enemies_to_spawn(self):
        """Gere uma lista de inimigos para gerar"""
        enemies_list = []
        enemies = {
            0: "ballom", 1: "ballom", 2: "onil", 3: "dahl", 
            4: "minvo", 5: "doria", 6: "ovape", 7: "pass", 8: "pontan"
        }

        if self.level <= 8:
            self.add_enemies_to_list(8, 2, 0, enemies, enemies_list)
        elif self.level <= 17:
            self.add_enemies_to_list(7, 2, 1, enemies, enemies_list)
        elif self.level <= 26:
            self.add_enemies_to_list(6, 3, 1, enemies, enemies_list)
        elif self.level <= 35:
            self.add_enemies_to_list(5, 3, 2, enemies, enemies_list)
        elif self.level <= 45:
            self.add_enemies_to_list(4, 4, 2, enemies, enemies_list)
        else:
            self.add_enemies_to_list(3, 4, 4, enemies, enemies_list)
        return enemies_list

    def add_enemies_to_list(self, num_1, num_2, num_3, enemies, enemies_list):
        for num in range(num_1):
            enemies_list.append("ballom")
            enemies_list.append("pontan")
        for num in range(num_2):
            enemies_list.append(enemies[(self.level % 9)])
        for num in range(num_3):
            enemies_list.append(choice(list(enemies.values())))
        return

    def select_a_special(self):
        specials = list(gs.SPECIALS.keys())
        specials.remove("exit")
        
        if self.level == 4:
            return "speed_up"
        elif self.level == 1:
            return "bomb_up"
        elif self.player is None:
            return choice(specials)
            
        if self.player.bomb_limit <= 2 or self.player.power <= 2:
            return choice(["bomb_up", "fire_up"])
        
        if hasattr(self.player, 'wall_hack') and self.player.wall_hack:
            specials.remove("wall_hack")
        if hasattr(self.player, 'remote_detonate') and self.player.remote_detonate:
            specials.remove("remote")
        if hasattr(self.player, 'bomb_hack') and self.player.bomb_hack:
            specials.remove("bomb_pass")
        if hasattr(self.player, 'flame_hack') and self.player.flame_hack:
            specials.remove("flame_pass")
        if hasattr(self.player, 'bomb_limit') and self.player.bomb_limit == 10:
            specials.remove("bomb_up")
        if hasattr(self.player, 'power') and self.player.power == 10:
            specials.remove("fire_up")
            
        return choice(specials)

    def new_stage(self):
        """Aumenta o número do nível do estágio e selecione um novo nível especial"""
        self.level += 1
        self.level_special = self.select_a_special()
        if self.player is not None:
            self.player.set_player_position()
            self.player.set_player_images()
        self.regenerate_stage()
        self.save_game()

    def new_game(self):
        for keys, values in self.groups.items():
            self.groups[keys].empty()

        self.player = Character(
            self, self.ASSETS.player_char, self.groups["player"], 3, 2, gs.SIZE)

        self.game_on = True
        self.level = 1
        self.level_special = self.select_a_special()
        self.level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)
        self.level_info = InfoPanel(self, self.ASSETS)

        self.level_transition = LevelTransition(self, self.ASSETS, self.level)
        self.start_screen_music.stop()

    def check_top_score(self, player_score):
        """Compara a pontuação do jogador com a pontuação máxima."""
        if player_score > self.top_score:
            self.top_score = player_score
            self.top_score_img = self.top_score_image()

    def top_score_image(self):
        score = [item for item in str(self.top_score)]
        score_image = [self.ASSETS.numbers_white[int(image)][0] for image in score]
        if self.top_score == 0:
            score_image.append(self.ASSETS.numbers_white[0][0])
        return score_image
    
    def save_game(self):
        try:
            with open("savegame.txt", "w") as file:
                if self.player is None:
                    return
                    
                file.write(f"{self.level}\n")
                file.write(f"{self.player.score}\n")
                file.write(f"{self.player.lives}\n")
                file.write(f"{self.player.row_num},{self.player.col_num}\n")

                for enemy in self.groups["enemies"]:
                    file.write(f"{enemy.type},{enemy.row},{enemy.col}\n")

            print("Progresso salvo!")
        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")

    def load_game(self):
        try:
            with open("savegame.txt", "r") as file:
                lines = file.readlines()

                self.level = int(lines[0].strip())
                self.level_special = self.select_a_special()
                player_score = int(lines[1].strip())
                player_lives = int(lines[2].strip())
                row_col = lines[3].strip().split(",")
                player_row = int(row_col[0])
                player_col = int(row_col[1])

                for key in self.groups.keys():
                    self.groups[key].empty()

                self.player = Character(
                    self, self.ASSETS.player_char, 
                    self.groups["player"], player_row, player_col, gs.SIZE)
                self.player.score = player_score
                self.player.lives = player_lives

                for line in lines[4:]:
                    if line.strip() == "":
                        continue
                    enemy_data = line.strip().split(",")
                    enemy_type = enemy_data[0]
                    enemy_row = int(enemy_data[1])
                    enemy_col = int(enemy_data[2])
                    Enemy(
                        self, self.ASSETS.enemies[enemy_type], 
                        self.groups["enemies"], enemy_type, enemy_row, enemy_col, gs.SIZE)

                self.level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)
                self.level_info = InfoPanel(self, self.ASSETS)
                self.level_transition = LevelTransition(self, self.ASSETS, self.level)
                self.start_screen_music.stop()
                self.game_on = True

            print("Progresso carregado!")
        except Exception as e:
            print(f"Erro ao carregar o jogo: {e}")


class LevelTransition(pygame.sprite.Sprite):
    def __init__(self, game, assets, stage_num):
        super().__init__()
        self.GAME = game
        self.GAME.transition = True
        self.ASSETS = assets
        self.stage_num = stage_num

        self.time = 2800
        self.timer = pygame.time.get_ticks()

        self.image = self.ASSETS.stage_word
        self.xpos = (gs.SCREENWIDTH // 2) - self.image.get_width() - 64
        self.ypos = (gs.SCREENHEIGHT // 2) - self.image.get_height()
        self.rect = self.image.get_rect(topleft=(self.xpos, self.ypos))

        self.stage_num_img = self.generate_stage_number_image()
        self.ASSETS.sounds["BM - 02 Stage Start.mp3"].play()

    def generate_stage_number_image(self):
        """Gere a imagem para o número do estágio"""
        num_imgs = []
        for num in str(self.stage_num):
            num_imgs.append(self.ASSETS.numbers_white[int(num)][0])
        return num_imgs

    def update(self):
        if pygame.time.get_ticks() - self.timer >= self.time:
            self.GAME.transition = False
            self.kill()

    def draw(self, window):
        window.fill((0, 0, 0))
        window.blit(self.image, self.rect)
        if len(self.stage_num_img) == 2:
            for ind, img in enumerate(self.stage_num_img):
                xpos = (gs.SCREENWIDTH//2) + 32 + (ind * 32)
                ypos = (gs.SCREENHEIGHT // 2) - self.image.get_height()
                window.blit(img, (xpos, ypos))
        else:
            xpos = (gs.SCREENWIDTH // 2) + 64
            ypos = (gs.SCREENHEIGHT // 2) - self.image.get_height()
            window.blit(self.stage_num_img[0], (xpos, ypos))
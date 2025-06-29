import pygame
from character import Character
from enemy import Enemy
from blocks import HardBlock, SoftBlock, SpecialSoftBlock
from random import choice, randint
from info_panel import InfoPanel
import gamesettings as gs

class GameState:
    """Classe para gerenciar o estado do jogo"""
    def __init__(self):
        self._game_on = False
        self._transition = False
        self._music_playing = False
        self._level = 0
        self._top_score = 0

    @property
    def game_on(self):
        return self._game_on

    @game_on.setter
    def game_on(self, value):
        self._game_on = value

    @property
    def transition(self):
        return self._transition

    @transition.setter
    def transition(self, value):
        self._transition = value

    @property
    def music_playing(self):
        return self._music_playing

    @music_playing.setter
    def music_playing(self, value):
        self._music_playing = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def top_score(self):
        return self._top_score

    @top_score.setter
    def top_score(self, value):
        self._top_score = value

class Game:
    """Classe principal do jogo"""
    def __init__(self, main, assets):
        self._main = main
        self._assets = assets
        self._camera_x_offset = 0
        self._state = GameState()
        
        self._initialize_groups()
        self._initialize_music()
        self._initialize_menu()
        
        # Inicializa atributos que podem ser None
        self._player = None
        self._level_info = None
        self._level_matrix = None
        self._level_transition = None
        self._level_special = None

    def _initialize_groups(self):
        """Inicializa todos os grupos de sprites"""
        self._groups = {
            "hard_block": pygame.sprite.Group(),
            "soft_block": pygame.sprite.Group(),
            "bomb": pygame.sprite.Group(),
            "specials": pygame.sprite.Group(),
            "explosions": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(),
            "player": pygame.sprite.Group(),
            "scores": pygame.sprite.Group()
        }

    def _initialize_music(self):
        """Inicializa a música e efeitos sonoros"""
        self._start_screen_music = self._assets.sounds["BM - 01 Title Screen.mp3"]
        self._bg_music = self._assets.sounds["BM - 03 Main BGM.mp3"]
        self._bg_music_special = self._assets.sounds["BM - 04 Power-Up Get.mp3"]
        self._stage_ending_music = self._assets.sounds["BM - 05 Stage Clear.mp3"]
        self._music_volume = 0.5
        self._sfx_volume = 0.5
        self._start_screen_music.play(loops=-1)
        self._set_volumes()

    def _initialize_menu(self):
        """Inicializa as configurações do menu"""
        self._point_position = [(384, 530), (384, 580)]
        self._point_pos = 0
        self._pointer_pos = self._point_position[self._point_pos]
        self._top_score_img = self._top_score_image()

    def _set_volumes(self):
        """Configura os volumes de música e efeitos sonoros"""
        self._start_screen_music.set_volume(self._music_volume)
        self._bg_music.set_volume(self._music_volume)
        self._bg_music_special.set_volume(self._music_volume)
        self._stage_ending_music.set_volume(self._music_volume)
        for sound in self._assets.sounds.values():
            if sound:
                sound.set_volume(self._sfx_volume)

    @property
    def main(self):
        return self._main

    @property
    def assets(self):
        return self._assets

    @property
    def groups(self):
        return self._groups

    @property
    def player(self):
        return self._player

    @property
    def level_matrix(self):
        return self._level_matrix

    @level_matrix.setter
    def level_matrix(self, value):
        self._level_matrix = value

    @property
    def game_on(self):
        return self._state.game_on

    @game_on.setter
    def game_on(self, value):
        self._state.game_on = value

    @property
    def music_playing(self):
        return self._state.music_playing

    @music_playing.setter
    def music_playing(self, value):
        self._state.music_playing = value

    @property
    def transition(self):
        return self._state.transition

    @transition.setter
    def transition(self, value):
        self._state.transition = value

    @property
    def level(self):
        return self._state.level

    @level.setter
    def level(self, value):
        self._state.level = value

    @property
    def start_screen_music(self):
        return self._start_screen_music

    @property
    def bg_music(self):
        return self._bg_music

    @property
    def bg_music_special(self):
        return self._bg_music_special

    @property
    def stage_ending_music(self):
        return self._stage_ending_music

    def input(self, events):
        if not self.game_on:
            self._handle_menu_input(events)
            return

        if self._player is not None:
            self._player.input(events)

    def _handle_menu_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._main.run = False

            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_UP:
            self._point_pos = max(0, self._point_pos - 1)
        elif event.key == pygame.K_DOWN:
            self._point_pos = min(1, self._point_pos + 1)
        self._pointer_pos = self._point_position[self._point_pos]

        if event.key == pygame.K_1:  # Aumentar Música
            self._adjust_volume(0.1, "music")
        elif event.key == pygame.K_2:  # Diminuir Música
            self._adjust_volume(-0.1, "music")
        elif event.key == pygame.K_3:  # Aumentar Efeitos
            self._adjust_volume(0.1, "sfx")
        elif event.key == pygame.K_4:  # Diminuir Efeitos
            self._adjust_volume(-0.1, "sfx")
        elif event.key == pygame.K_ESCAPE:
            self._return_to_menu()
        elif event.key == pygame.K_RETURN:
            self._handle_menu_selection()

    def _adjust_volume(self, change, volume_type):
        if volume_type == "music":
            self._music_volume = max(0.0, min(1.0, self._music_volume + change))
            pygame.mixer.music.set_volume(self._music_volume)
            self._start_screen_music.set_volume(self._music_volume)
            self._bg_music.set_volume(self._music_volume)
            self._bg_music_special.set_volume(self._music_volume)
            self._stage_ending_music.set_volume(self._music_volume)
            print(f"Volume Música: {self._music_volume:.1f}")
        else:
            self._sfx_volume = max(0.0, min(1.0, self._sfx_volume + change))
            for sound in self._assets.sounds.values():
                if sound:
                    sound.set_volume(self._sfx_volume)
            print(f"Volume SFX: {self._sfx_volume:.1f}")

    def _return_to_menu(self):
        self._bg_music.stop()
        self._bg_music_special.stop()
        self._stage_ending_music.stop()
        self._start_screen_music.play(-1)
        self._start_screen_music.set_volume(self._music_volume)
        self.game_on = False
        print("Jogador voltou ao menu inicial.")

    def _handle_menu_selection(self):
        if self._point_pos == 0:
            self.new_game()
        elif self._point_pos == 1:
            self.load_game()

    def _handle_mouse_click(self, event):
        mouse_x, mouse_y = event.pos
        print(f"Clique do mouse em: x={mouse_x}, y={mouse_y}")
        start_rect = pygame.Rect(384, 530, 256, 40)
        continue_rect = pygame.Rect(384, 580, 256, 40)
        
        if start_rect.collidepoint(mouse_x, mouse_y):
            print("Clique detectado em START!")
            self._point_pos = 0
            self._pointer_pos = self._point_position[self._point_pos]
            self.new_game()
        elif continue_rect.collidepoint(mouse_x, mouse_y):
            print("Clique detectado em CONTINUE!")
            self._point_pos = 1
            self._pointer_pos = self._point_position[self._point_pos]
            self.load_game()

    def update(self):
        if not self.game_on:
            return

        if self.transition and self._level_transition is not None:
            self._level_transition.update()
            return

        self._handle_music_transitions()
        
        if self._level_info is not None:
            self._level_info.update()

        for group in self._groups.values():
            group.update()

        self._check_enemy_collisions()

    def _handle_music_transitions(self):
        if (self.game_on and not self.transition and not self.music_playing and 
            len(self._groups["enemies"].sprites()) > 0):
            self.music_playing = True
            self._bg_music.play(loops=-1)

        if (len(self._groups["enemies"].sprites()) == 0 and 
            self.music_playing):
            self.music_playing = False
            self._bg_music.stop()
            self._bg_music_special.stop()
            self._stage_ending_music.play()

    def _check_enemy_collisions(self):
        if self._groups["explosions"]:
            killed_enemies = pygame.sprite.groupcollide(
                self._groups["explosions"], self._groups["enemies"], False, False)
            if killed_enemies:
                for flame, enemies in killed_enemies.items():
                    for enemy in enemies:
                        if pygame.sprite.collide_mask(flame, enemy):
                            enemy.destroy()

    def draw(self, window):
        window.fill(gs.GREY)

        if not self.game_on:
            self._draw_menu(window)
            return

        if self.transition and self._level_transition is not None:
            self._level_transition.draw(window)
            return

        if self._level_info is not None:
            self._level_info.draw(window)

        self._draw_game_background(window)
        self._draw_sprites(window)

    def _draw_menu(self, window):
        window.blit(self._assets.start_screen, (0, 0))
        window.blit(self._assets.start_screen_pointer, self._pointer_pos)
        if self._top_score_img:
            for i, img in enumerate(self._top_score_img):
                window.blit(img, (638 + (i - len(self._top_score_img)) * 32, 655))

    def _draw_game_background(self, window):
        if self._level_matrix is not None:
            for row_num, row in enumerate(self._level_matrix):
                for col_num, col in enumerate(row):
                    window.blit(
                        self._assets.background["background"][0],
                        ((col_num * gs.SIZE) - self._camera_x_offset, 
                         (row_num * gs.SIZE) + gs.Y_OFFSET))
        else:
            window.fill(gs.BLACK)

    def _draw_sprites(self, window):
        for group in self._groups.values():
            for item in group:
                item.draw(window, self._camera_x_offset)

    def generate_level_matrix(self, rows, cols):
        """Gera a matriz do nível"""
        matrix = []
        for row in range(rows + 1):
            line = []
            for col in range(cols + 1):
                line.append("_")
            matrix.append(line)
            
        self._insert_hard_blocks_into_matrix(matrix)
        self._insert_soft_blocks_into_matrix(matrix)
        
        for special in gs.SPECIALS.keys():
            if special != "exit":
                self._insert_power_up_into_matrix(matrix, special)
                
        self._insert_power_up_into_matrix(matrix, "exit")
        self._insert_enemies_into_level(matrix)
        
        return matrix

    def _insert_hard_blocks_into_matrix(self, matrix):
        """Insere blocos rígidos na matriz"""
        for row_num, row in enumerate(matrix):
            for col_num, col in enumerate(row):
                if (row_num == 0 or row_num == len(matrix)-1 or 
                    col_num == 0 or col_num == len(row)-1 or 
                    (row_num % 2 == 0 and col_num % 2 == 0)):
                    matrix[row_num][col_num] = HardBlock(
                        self, self._assets.hard_block["hard_block"],
                        self._groups["hard_block"], row_num, col_num, gs.SIZE)

    def _insert_soft_blocks_into_matrix(self, matrix):
        """Insere blocos macios na matriz"""
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
                        cell = SoftBlock(
                            self, self._assets.soft_block["soft_block"],
                            self._groups["soft_block"], row_num, col_num, gs.SIZE)
                    matrix[row_num][col_num] = cell

    def _insert_power_up_into_matrix(self, matrix, special):
        """Insere power-ups especiais na matriz"""
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
                
        cell = SpecialSoftBlock(
            self,
            self._assets.soft_block["soft_block"],
            self._groups["soft_block"],
            row, col, gs.SIZE, power_up)
        matrix[row][col] = cell

    def update_x_camera_offset_player_position(self, player_x_pos):
        """Atualiza o deslocamento da câmera com base na posição do jogador"""
        if player_x_pos >= 576 and player_x_pos <= 1280:
            self._camera_x_offset = player_x_pos - 576

    def _insert_enemies_into_level(self, matrix, enemies=None):
        """Insere inimigos no nível"""
        if self._player is None:
            return

        enemies_list = self._select_enemies_to_spawn() if enemies is None else enemies
        pl_col = self._player.col_num
        pl_row = self._player.row_num

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
                        self, self._assets.enemies[enemy], 
                        self._groups["enemies"], enemy, row, col, gs.SIZE)

    def regenerate_stage(self):
        """Regenera o estágio atual"""
        for key in self._groups.keys():
            if key == "player":
                continue
            self._groups[key].empty()

        if self._level_matrix is not None:
            self._level_matrix.clear()
        if self._level_info is not None:
            self._level_info._set_timer()
            
        self._level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)
        self._camera_x_offset = 0
        self._level_transition = LevelTransition(self, self._assets, self.level)
        self.music_playing = False

    def _select_enemies_to_spawn(self):
        """Seleciona inimigos para spawnar"""
        enemies_list = []
        enemies = {
            0: "ballom", 1: "ballom", 2: "onil", 3: "dahl", 
            4: "minvo", 5: "doria", 6: "ovape", 7: "pass", 8: "pontan"
        }

        if self.level <= 8:
            self._add_enemies_to_list(8, 2, 0, enemies, enemies_list)
        elif self.level <= 17:
            self._add_enemies_to_list(7, 2, 1, enemies, enemies_list)
        elif self.level <= 26:
            self._add_enemies_to_list(6, 3, 1, enemies, enemies_list)
        elif self.level <= 35:
            self._add_enemies_to_list(5, 3, 2, enemies, enemies_list)
        elif self.level <= 45:
            self._add_enemies_to_list(4, 4, 2, enemies, enemies_list)
        else:
            self._add_enemies_to_list(3, 4, 4, enemies, enemies_list)
            
        return enemies_list

    def _add_enemies_to_list(self, num_1, num_2, num_3, enemies, enemies_list):
        for num in range(num_1):
            enemies_list.append("ballom")
            enemies_list.append("pontan")
        for num in range(num_2):
            enemies_list.append(enemies[(self.level % 9)])
        for num in range(num_3):
            enemies_list.append(choice(list(enemies.values())))

    def _select_a_special(self):
        """Seleciona um power-up especial"""
        specials = list(gs.SPECIALS.keys())
        specials.remove("exit")
        
        if self.level == 4:
            return "speed_up"
        elif self.level == 1:
            return "bomb_up"
        elif self._player is None:
            return choice(specials)
            
        if self._player.bomb_limit <= 2 or self._player.power <= 2:
            return choice(["bomb_up", "fire_up"])
        
        if hasattr(self._player, 'wall_hack') and self._player.wall_hack:
            specials.remove("wall_hack")
        if hasattr(self._player, 'remote') and self._player.remote:
            specials.remove("remote")
        if hasattr(self._player, 'bomb_hack') and self._player.bomb_hack:
            specials.remove("bomb_pass")
        if hasattr(self._player, 'flame_pass') and self._player.flame_pass:
            specials.remove("flame_pass")
        if hasattr(self._player, 'bomb_limit') and self._player.bomb_limit == 10:
            specials.remove("bomb_up")
        if hasattr(self._player, 'power') and self._player.power == 10:
            specials.remove("fire_up")
            
        return choice(specials)

    def new_stage(self):
        """Avança para um novo estágio"""
        self.level += 1
        self._level_special = self._select_a_special()
        if self._player is not None:
            self._player.set_player_position()
            self._player.set_player_images()
            
        self.regenerate_stage()
        self.save_game()

    def new_game(self):
        """Inicia um novo jogo"""
        for group in self._groups.values():
            group.empty()

        self._player = Character(
            self, self._assets.player_char, self._groups["player"], 3, 2, gs.SIZE)

        self.game_on = True
        self.level = 1
        self._level_special = self._select_a_special()
        self._level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)
        self._level_info = InfoPanel(self, self._assets)

        self._level_transition = LevelTransition(self, self._assets, self.level)
        self._start_screen_music.stop()

    def check_top_score(self, player_score):
        """Verifica e atualiza a pontuação máxima"""
        if player_score > self._state.top_score:
            self._state.top_score = player_score
            self._top_score_img = self._top_score_image()

    def _top_score_image(self):
        score = [item for item in str(self._state.top_score)]
        score_image = [self._assets.numbers_white[int(image)][0] for image in score]
        if self._state.top_score == 0:
            score_image.append(self._assets.numbers_white[0][0])
        return score_image
    
    def save_game(self):
        """Salva o progresso do jogo"""
        try:
            with open("savegame.txt", "w") as file:
                if self._player is None:
                    return
                    
                file.write(f"{self.level}\n")
                file.write(f"{self._player.score}\n")
                file.write(f"{self._player.lives}\n")
                file.write(f"{self._player.row_num},{self._player.col_num}\n")

                for enemy in self._groups["enemies"]:
                    file.write(f"{enemy.type},{enemy.row_num},{enemy.col_num}\n")

            print("Progresso salvo!")
        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")

    def load_game(self):
        """Carrega um jogo salvo"""
        try:
            with open("savegame.txt", "r") as file:
                lines = file.readlines()

                self.level = int(lines[0].strip())
                self._level_special = self._select_a_special()
                player_score = int(lines[1].strip())
                player_lives = int(lines[2].strip())
                row_col = lines[3].strip().split(",")
                player_row = int(row_col[0])
                player_col = int(row_col[1])

                for group in self._groups.values():
                    group.empty()

                self._player = Character(
                    self, self._assets.player_char, 
                    self._groups["player"], player_row, player_col, gs.SIZE)
                self._player.score = player_score
                self._player.lives = player_lives

                for line in lines[4:]:
                    if line.strip() == "":
                        continue
                    enemy_data = line.strip().split(",")
                    enemy_type = enemy_data[0]
                    enemy_row = int(enemy_data[1])
                    enemy_col = int(enemy_data[2])
                    Enemy(
                        self, self._assets.enemies[enemy_type], 
                        self._groups["enemies"], enemy_type, enemy_row, enemy_col, gs.SIZE)

                self._level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)
                self._level_info = InfoPanel(self, self._assets)
                self._level_transition = LevelTransition(self, self._assets, self.level)
                self._start_screen_music.stop()
                self.game_on = True

            print("Progresso carregado!")
        except Exception as e:
            print(f"Erro ao carregar o jogo: {e}")

class LevelTransition(pygame.sprite.Sprite):
    """Classe para a transição entre níveis"""
    def __init__(self, game, assets, stage_num):
        super().__init__()
        self._game = game
        self._game.transition = True
        self._assets = assets
        self._stage_num = stage_num
        self._time = 2800
        self._timer = pygame.time.get_ticks()
        self._image = self._assets.stage_word
        self._xpos = (gs.SCREENWIDTH // 2) - self._image.get_width() - 64
        self._ypos = (gs.SCREENHEIGHT // 2) - self._image.get_height()
        self._rect = self._image.get_rect(topleft=(self._xpos, self._ypos))
        self._stage_num_img = self._generate_stage_number_image()
        self._assets.sounds["BM - 02 Stage Start.mp3"].play()

    def _generate_stage_number_image(self):
        """Gera a imagem do número do estágio"""
        num_imgs = []
        for num in str(self._stage_num):
            num_imgs.append(self._assets.numbers_white[int(num)][0])
        return num_imgs

    def update(self):
        if pygame.time.get_ticks() - self._timer >= self._time:
            self._game.transition = False
            self.kill()

    def draw(self, window):
        window.fill((0, 0, 0))
        window.blit(self._image, self._rect)
        
        if len(self._stage_num_img) == 2:
            for ind, img in enumerate(self._stage_num_img):
                xpos = (gs.SCREENWIDTH//2) + 32 + (ind * 32)
                ypos = (gs.SCREENHEIGHT // 2) - self._image.get_height()
                window.blit(img, (xpos, ypos))
        else:
            xpos = (gs.SCREENWIDTH // 2) + 64
            ypos = (gs.SCREENHEIGHT // 2) - self._image.get_height()
            window.blit(self._stage_num_img[0], (xpos, ypos))
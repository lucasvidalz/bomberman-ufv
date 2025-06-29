import pygame
import gamesettings as gs

class InfoPanel:
    """Classe para o painel de informações do jogo"""
    def __init__(self, game, images):
        self._game = game
        self._images = images
        self._black_nums = self._images.numbers_black
        self._player_lives_left_word = self._images.left_word
        self._score_image = self._update_score_image(self._game.player.score)
        self._set_timer()

    def _set_timer(self):
        """Configura o temporizador do nível"""
        self._time_total = gs.STAGE_TIME
        self._timer_start = pygame.time.get_ticks()
        self._time = 200
        self._time_image = self._update_time_image()
        self._time_word_image = self._images.time_word
        self._time_word_rect = self._time_word_image.get_rect(topleft=(32, 32))

    def _update_time_image(self):
        """Atualiza a imagem do temporizador"""
        num_string_list = [item for item in str(self._time)]
        images = [self._black_nums[int(image)] for image in num_string_list]
        return images

    def update(self):
        """Atualiza o painel de informações"""
        self._score_image = self._update_score_image(self._game.player.score)

        if self._time == 0:
            return

        if pygame.time.get_ticks() - self._timer_start >= 1000:
            self._timer_start = pygame.time.get_ticks()
            self._time -= 1
            self._time_image = self._update_time_image()
            if self._time == 0:
                self._game.insert_enemies_into_level(
                    self._game.level_matrix, ["pontan" for _ in range(10)])

    def draw(self, window):
        """Desenha o painel de informações"""
        # Temporizador
        window.blit(self._time_word_image, self._time_word_rect)
        start_x = 192 if len(self._time_image) == 3 else 224 if len(self._time_image) == 2 else 256
        for num, image in enumerate(self._time_image):
            window.blit(image, (start_x + (32 * num), 32))
            
        # Pontuação
        start_x = ((gs.SCREENWIDTH // 2) + 64) - (len(self._score_image) * 32)
        for num, image in enumerate(self._score_image):
            window.blit(image, (start_x + (32 * num), 32))

        # Vidas
        window.blit(self._player_lives_left_word, (1032, 32))
        window.blit(self._black_nums[self._game.player.lives], (1184, 32))

    def _update_score_image(self, score):
        """Atualiza a imagem da pontuação"""
        if score == 0:
            score_images = [self._black_nums[0], self._black_nums[0]]
        else:
            score_images = [self._black_nums[int(digit)] for digit in str(score)]
        return score_images

class Scoring(pygame.sprite.Sprite):
    """Classe para mostrar a pontuação ao derrotar inimigos"""
    _score_bonus = 0

    def __init__(self, game, group, score, xpos, ypos):
        super().__init__(group)
        Scoring._score_bonus += 1

        self._game = game
        self._score = score if Scoring._score_bonus <= 1 else score * 2
        self._time = pygame.time.get_ticks()
        self._x = xpos
        self._y = ypos

        if self._score in self._game.assets.score_images:
            self._image = self._game.assets.score_images[self._score][0]
        else:
            self._image = self._game.assets.score_images[100][0]
        self._rect = self._image.get_rect(topleft=(self._x, self._y))

    def update(self):
        if pygame.time.get_ticks() - self._time >= 1000:
            self.kill()
            Scoring._score_bonus -= 1
            self._game.player.update_score(self._score)

    def draw(self, window, x_offset):
        window.blit(self._image, (self._rect.x - x_offset, self._rect.y))
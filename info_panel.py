import pygame
import gamesettings as gs


class InfoPanel:
    def __init__(self, game, images):
        self.GAME = game
        self.images = images

        self.black_nums = self.images.numbers_black

        #  Temporizador de nível
        self.set_timer()

        #  Vidas dos jogadores
        self.player_lives_left_word = self.images.left_word

        #  Pontuação do jogador
        self.score_image = self.update_score_image(self.GAME.player.score)


    def set_timer(self):
        #  Temporizador de nível
        self.time_total = gs.STAGE_TIME
        self.timer_start = pygame.time.get_ticks()
        self.time = 200

        #  Imagens para painel de informações
        self.time_image = self.update_time_image()
        self.time_word_image = self.images.time_word
        self.time_word_rect = self.time_word_image.get_rect(topleft=(32, 32))


    def update_time_image(self):
        """Atualiza a lista de imagens do indicador de tempo no painel de informações"""
        num_string_list = [item for item in str(self.time)]
        images = [self.black_nums[int(image)][0] for image in num_string_list]
        return images


    def update(self):
        #  Atualizar a pontuação
        self.score_image = self.update_score_image(self.GAME.player.score)

        #  Se o cronômetro chegar a zero, pare o contador
        if self.time == 0:
            return

        #  Contagem regressiva do temporizador, altere a imagem do temporizador a cada segundo
        if pygame.time.get_ticks() - self.timer_start >= 1000:
            self.timer_start = pygame.time.get_ticks()
            self.time -= 1
            self.time_image = self.update_time_image()
            if self.time == 0:
                self.GAME.insert_enemies_into_level(self.GAME.level_matrix, ["pontan" for _ in range(10)])


    def draw(self, window):
        #  Desenhe o indicador de tempo na tela
        window.blit(self.time_word_image, self.time_word_rect)
        start_x = 192 if len(self.time_image) == 3 else 224 if len(self.time_image) == 2 else 256
        for num, image in enumerate(self.time_image):
            window.blit(image, (start_x + (32 * num), 32))
        #  Imagens de pontuação do jogador
        start_x = ((gs.SCREENWIDTH // 2) + 64) - (len(self.score_image) * 32)
        for num, image in enumerate(self.score_image):
            window.blit(image, (start_x + (32 * num), 32))

        #  Vidas restantes dos jogadores
        window.blit(self.player_lives_left_word, (1032, 32))
        window.blit(self.black_nums[self.GAME.player.lives][0], (1184, 32))


    def update_score_image(self, score):
        """ATUALIZA a pontuação do jogador com a pontuação mais recente"""
        if score == 0:
            score_images = [self.black_nums[0][0], self.black_nums[0][0]]
        else:
            score_images = [self.black_nums[int(digit)][0] for digit in str(score)]
        return score_images


class Scoring(pygame.sprite.Sprite):
    score_bonus = 0

    def __init__(self, game, group, score, xpos, ypos):
        super().__init__(group)
        Scoring.score_bonus += 1

        self.GAME = game
        self.score = score if Scoring.score_bonus <= 1 else score * 2

        self.time = pygame.time.get_ticks()

        self.x = xpos
        self.y = ypos

        if self.score in self.GAME.ASSETS.score_images:
            self.image = self.GAME.ASSETS.score_images[self.score][0]
        else:
            self.image = self.GAME.ASSETS.score_images[100][0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        if pygame.time.get_ticks() - self.time >= 1000:
            self.kill()
            Scoring.score_bonus -= 1
            self.GAME.player.update_score(self.score)

    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))
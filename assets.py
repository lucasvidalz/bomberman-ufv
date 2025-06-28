import pygame
import gamesettings as gs


class Assets:
    def __init__(self):
        self.spritesheet = self.load_sprite_sheet("images", "spritesheet.png", 192*4, 272*4)

        self.player_char = self.load_sprite_range(gs.PLAYER, self.spritesheet)
        self.hard_block = self.load_sprite_range(gs.HARD_BLOCK, self.spritesheet)
        self.soft_block = self.load_sprite_range(gs.SOFT_BLOCK, self.spritesheet)
        self.background = self.load_sprite_range(gs.BACKGROUND, self.spritesheet)
        self.bomb = self.load_sprite_range(gs.BOMB, self.spritesheet)
        self.explosions = self.load_sprite_range(gs.EXPLOSIONS, self.spritesheet)
        for image_list in ["right_end", "right_mid", "down_end", "down_mid"]:
            self.rotate_images_in_list(self.explosions[image_list], 180)
        #self.ballom = self.load_sprite_range(gs.BALLOM, self.spritesheet)
        self.enemies = {"ballom" : self.load_sprite_range(gs.BALLOM, self.spritesheet),
                        "onil" : self.load_sprite_range(gs.ONIL, self.spritesheet),
                        "dahl" : self.load_sprite_range(gs.DAHL, self.spritesheet),
                        "minvo" : self.load_sprite_range(gs.MINVO, self.spritesheet),
                        "doria" : self.load_sprite_range(gs.DORIA, self.spritesheet),
                        "ovape" : self.load_sprite_range(gs.OVAPE, self.spritesheet),
                        "pass" : self.load_sprite_range(gs.PASS, self.spritesheet),
                        "pontan" : self.load_sprite_range(gs.PONTAN, self.spritesheet)}
        self.specials = self.load_sprite_range(gs.SPECIALS, self.spritesheet)

        self.time_word = pygame.transform.scale(self.load_sprites(self.spritesheet, 4*64, 13*64, 64*4, 64), (32*4, 32))

        self.left_word = pygame.transform.scale(self.load_sprites(self.spritesheet, 0*64, 13*64, 64*4, 64), (32*4, 32))

        self.numbers_black = self.load_sprite_range(gs.NUMBERS_BLACK, self.spritesheet, resize=True)
        self.numbers_white = self.load_sprite_range(gs.NUMBERS_WHITE, self.spritesheet, resize=True)

        self.score_images = self.load_sprite_range(gs.SCORE_IMAGES, self.spritesheet, 64, 64, 64, 32)

        self.start_screen = self.load_sprite_sheet("images", "Bomberman start screen.png",
                                                   gs.SCREENWIDTH, gs.SCREENHEIGHT)
        self.start_screen_pointer = self.load_sprite_sheet("images", "pointer.png", 32, 32)

        self.stage_word = pygame.transform.scale(self.load_sprites(self.spritesheet, 0*64, 14*64, 64*5, 64), (32*5, 32)) 

        self.sounds = self.load_sound_effects()

    def load_sprite_sheet(self, path, filename, width, height):
        """Load in the sprite sheet image, and resize it"""
        image = pygame.image.load(f"{path}/{filename}").convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image


    def load_sprites(self, spritesheet, xcoord, ycoord, width, height):
        """Carrega uma imagem de sprite individual"""
        #  Cria uma superfície vazia
        image = pygame.Surface((width, height))
        #  Preenche a superfície com uma cor preta
        image.fill((0, 0, 1))
        #  Coloca o sprite na nova superfície
        image.blit(spritesheet, (0, 0), (xcoord, ycoord, width, height))
        #  Converte as cores pretas da nova imagem em transparentes
        image.set_colorkey(gs.BLACK)
        return image


    def load_sprite_range(self, image_dict, spritesheet, row=gs.SIZE, col=gs.SIZE, width=gs.SIZE, height=gs.SIZE, resize=False):
        """Retorna um dicionário contendo listas de imagens para as animações"""
        animation_images = {}
        for animation in image_dict.keys():
            animation_images[animation] = []
            for coord in image_dict[animation]:
                image = self.load_sprites(spritesheet, coord[1] * col, coord[0] * row, width, height)
                if resize:
                    image = pygame.transform.scale(image, (32, 32))
                animation_images[animation].append(image)
        return animation_images


    def rotate_images_in_list(self, image_list, rotation):
        """Percorre a lista de imagens e gire cada uma das imagens"""
        for ind, image in enumerate(image_list):
            image = pygame.transform.rotate(image, rotation)
            image_list[ind] = image


    def load_sound_effects(self):
        sound_files = {}
        for sound in gs.SOUNDS:
            sound_files[sound] = pygame.mixer.Sound(f"sounds/{sound}")
        return sound_files 


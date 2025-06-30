import pygame
import core.gamesettings as gs
from abc import ABC, abstractmethod

class AssetLoader(ABC):
    """Classe abstrata para carregamento de assets"""
    @abstractmethod
    def load(self):
        pass

class SpriteSheetLoader(AssetLoader):
    def __init__(self, path, filename, width, height):
        self.path = path
        self.filename = filename
        self.width = width
        self.height = height
    
    def load(self):
        """Carrega a sprite sheet e redimensiona"""
        try:
            image = pygame.image.load(f"{self.path}/{self.filename}").convert_alpha()
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error as e:
            print(f"Erro ao carregar sprite sheet: {e}")
            return pygame.Surface((self.width, self.height))

class SoundLoader(AssetLoader):
    def __init__(self, sound_files):
        self.sound_files = sound_files
    
    def load(self):
        """Carrega os efeitos sonoros"""
        sound_files = {}
        for sound in self.sound_files:
            try:
                sound_files[sound] = pygame.mixer.Sound(f"assets/sounds/{sound}")
            except pygame.error as e:
                print(f"Erro ao carregar som {sound}: {e}")
                sound_files[sound] = None
        return sound_files

class Assets:
    def __init__(self):
        self._spritesheet = None
        self._player_char = None
        self._hard_block = None
        self._soft_block = None
        self._background = None
        self._bomb = None
        self._explosions = None
        self._enemies = None
        self._specials = None
        self._numbers_black = None
        self._numbers_white = None
        self._score_images = None
        self._start_screen = None
        self._start_screen_pointer = None
        self._stage_word = None
        self._sounds = None
        
        self._load_all_assets()

    def _load_all_assets(self):
        """Carrega todos os assets do jogo"""
        # SpriteSheet principal - carrega no tamanho original e depois redimensiona
        # A spritesheet original é 192x272 pixels (12 colunas x 17 linhas de sprites 16x16)
        loader = SpriteSheetLoader("assets/images", "spritesheet.png", 192, 272)
        original_spritesheet = loader.load()
        
        # Redimensiona para o tamanho do jogo (64x64 por sprite)
        self._spritesheet = pygame.transform.scale(original_spritesheet, (192*4, 272*4))

        # Carrega sprites
        self._player_char = self._load_sprite_range(gs.PLAYER, self._spritesheet)
        self._hard_block = self._load_sprite_range(gs.HARD_BLOCK, self._spritesheet)
        self._soft_block = self._load_sprite_range(gs.SOFT_BLOCK, self._spritesheet)
        self._background = self._load_sprite_range(gs.BACKGROUND, self._spritesheet)
        self._bomb = self._load_sprite_range(gs.BOMB, self._spritesheet)
        self._explosions = self._load_sprite_range(gs.EXPLOSIONS, self._spritesheet)
        
        # Rotaciona imagens de explosão
        for image_list in ["right_end", "right_mid", "down_end", "down_mid"]:
            self._rotate_images_in_list(self._explosions[image_list], 180)
        
        # Inimigos
        self._enemies = {
            "ballom": self._load_sprite_range(gs.BALLOM, self._spritesheet),
            "onil": self._load_sprite_range(gs.ONIL, self._spritesheet),
            "dahl": self._load_sprite_range(gs.DAHL, self._spritesheet),
            "minvo": self._load_sprite_range(gs.MINVO, self._spritesheet),
            "doria": self._load_sprite_range(gs.DORIA, self._spritesheet),
            "ovape": self._load_sprite_range(gs.OVAPE, self._spritesheet),
            "pass": self._load_sprite_range(gs.PASS, self._spritesheet),
            "pontan": self._load_sprite_range(gs.PONTAN, self._spritesheet)
        }
        
        self._specials = self._load_sprite_range(gs.SPECIALS, self._spritesheet)
        
        # Palavras de interface - usando coordenadas do gamesettings
        time_coord = gs.TIME_WORD["time_word"][0]
        left_coord = gs.LEFT_WORD["left_word"][0]
        stage_coord = gs.STAGE_WORD["stage_word"][0]
        
        self._time_word = pygame.transform.scale(
            self._load_sprite(self._spritesheet, time_coord[1]*16*4, time_coord[0]*16*4, 64*4, 64), (32*4, 32))
        self._left_word = pygame.transform.scale(
            self._load_sprite(self._spritesheet, left_coord[1]*16*4, left_coord[0]*16*4, 64*4, 64), (32*4, 32))
        self._numbers_black = self._load_numbers(gs.NUMBERS_BLACK, self._spritesheet)
        self._numbers_white = self._load_numbers(gs.NUMBERS_WHITE, self._spritesheet)
        self._score_images = self._load_sprite_range(gs.SCORE_IMAGES, self._spritesheet, 16, 16, 64, 64)
        
        # Telas
        loader = SpriteSheetLoader("assets/images", "Bomberman start screen.png", gs.SCREENWIDTH, gs.SCREENHEIGHT)
        self._start_screen = loader.load()
        
        loader = SpriteSheetLoader("assets/images", "pointer.png", 32, 32)
        self._start_screen_pointer = loader.load()
        
        # Palavra "STAGE" - usando coordenadas do gamesettings
        self._stage_word = pygame.transform.scale(
            self._load_sprite(self._spritesheet, stage_coord[1]*16*4, stage_coord[0]*16*4, 64*5, 64), (32*5, 32))
        
        # Sons
        sound_loader = SoundLoader(gs.SOUNDS)
        self._sounds = sound_loader.load()

    def _load_sprite(self, spritesheet, xcoord, ycoord, width, height):
        """Carrega um sprite individual"""
        try:
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.blit(spritesheet, (0, 0), (xcoord, ycoord, width, height))
            return image
        except Exception as e:
            print(f"Erro ao carregar sprite: {e}")
            return pygame.Surface((width, height), pygame.SRCALPHA)

    def _load_sprite_range(self, image_dict, spritesheet, row=16, col=16, 
                          width=64, height=64, resize=False):
        """Carrega um conjunto de sprites para animações"""
        animation_images = {}
        for animation in image_dict.keys():
            animation_images[animation] = []
            for coord in image_dict[animation]:
                # Coordenadas corretas: coord[0] = linha, coord[1] = coluna
                # Cada sprite é 16x16 na spritesheet original, mas escalado para 64x64
                x = coord[1] * 16 * 4  # coluna * 16 * 4 (escala)
                y = coord[0] * 16 * 4  # linha * 16 * 4 (escala)
                image = self._load_sprite(spritesheet, x, y, width, height)
                if resize:
                    image = pygame.transform.scale(image, (32, 32))
                animation_images[animation].append(image)
        return animation_images

    def _rotate_images_in_list(self, image_list, rotation):
        """Rotaciona imagens em uma lista"""
        for ind, image in enumerate(image_list):
            image = pygame.transform.rotate(image, rotation)
            image_list[ind] = image

    def _load_numbers(self, numbers_dict, spritesheet):
        """Carrega números individuais"""
        numbers_images = {}
        for number in numbers_dict.keys():
            coord = numbers_dict[number][0]  # Pega a primeira (e única) coordenada
            # Coordenadas corretas: coord[0] = linha, coord[1] = coluna
            x = coord[1] * 16 * 4  # coluna * 16 * 4 (escala)
            y = coord[0] * 16 * 4  # linha * 16 * 4 (escala)
            image = self._load_sprite(spritesheet, x, y, 64, 64)
            image = pygame.transform.scale(image, (32, 32))
            numbers_images[number] = image
        return numbers_images

    # Propriedades para acesso seguro aos assets
    @property
    def spritesheet(self):
        return self._spritesheet
    
    @property
    def player_char(self):
        return self._player_char
    
    @property
    def hard_block(self):
        return self._hard_block
    
    @property
    def soft_block(self):
        return self._soft_block
    
    @property
    def background(self):
        return self._background
    
    @property
    def bomb(self):
        return self._bomb
    
    @property
    def explosions(self):
        return self._explosions
    
    @property
    def enemies(self):
        return self._enemies
    
    @property
    def specials(self):
        return self._specials
    
    @property
    def time_word(self):
        return self._time_word
    
    @property
    def left_word(self):
        return self._left_word
    
    @property
    def numbers_black(self):
        return self._numbers_black
    
    @property
    def numbers_white(self):
        return self._numbers_white
    
    @property
    def score_images(self):
        return self._score_images
    
    @property
    def start_screen(self):
        return self._start_screen
    
    @property
    def start_screen_pointer(self):
        return self._start_screen_pointer
    
    @property
    def stage_word(self):
        return self._stage_word
    
    @property
    def sounds(self):
        return self._sounds
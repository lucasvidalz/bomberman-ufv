# Configurações da janela do jogo
SCREENWIDTH = 1024
SCREENHEIGHT = 768

# Quadros por segundo
FPS = 60

# Deslocamento de coordenadas Y
Y_OFFSET = 92

# Tempo de nível
STAGE_TIME = 200

# Tempo de explosão das bombas (ms)
BOMB_EXPLOSION_TIME = 1500

# Atributos dos inimigos
ENEMIES = {
    "ballom": {"speed": 1, "wall_hack": False, "chase_player": False, "LoS": 0, "see_player_hack": False},
    "onil": {"speed": 2, "wall_hack": False, "chase_player": True, "LoS": 4, "see_player_hack": False},
    "dahl": {"speed": 2, "wall_hack": False, "chase_player": False, "LoS": 0, "see_player_hack": False},
    "minvo": {"speed": 2, "wall_hack": False, "chase_player": True, "LoS": 4, "see_player_hack": True},
    "doria": {"speed": 0.5, "wall_hack": False, "chase_player": True, "LoS": 6, "see_player_hack": True},
    "ovape": {"speed": 1, "wall_hack": False, "chase_player": True, "LoS": 8, "see_player_hack": False},
    "pass": {"speed": 2, "wall_hack": False, "chase_player": True, "LoS": 12, "see_player_hack": False},
    "pontan": {"speed": 4, "wall_hack": False, "chase_player": True, "LoS": 30, "see_player_hack": False}
}

# Matriz de jogo
SIZE = 64
ROWS = 12
COLS = 30

# Cores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (188, 188, 188)

# Coordenadas dos sprites (corrigidas para o spritesheet real)
# Formato: (linha, coluna) - cada sprite é 16x16 pixels na spritesheet original
PLAYER = {
    "walk_left": [(0, 0), (0, 1), (0, 2)],
    "walk_right": [(0, 3), (0, 4), (0, 5)],
    "walk_up": [(0, 6), (0, 7), (0, 8)],
    "walk_down": [(0, 9), (0, 10), (0, 11)],
    "dead_anim": [(1, 0), (1, 1), (1, 2)]
}

# Blocos rígidos
HARD_BLOCK = {
    "hard_block": [(2, 3)]
}

# Blocos macios
SOFT_BLOCK = {
    "soft_block": [(2, 4)]
}

# Fundo
BACKGROUND = {
    "background": [(1, 5)]
}

# Bombas
BOMB = {
    "bomb": [(1, 6), (1, 7), (1, 8)]
}

# Explosões
EXPLOSIONS = {
    "centre": [(1, 9), (1, 10), (1, 11)],
    "left_end": [(2, 0)],
    "left_mid": [(2, 1)],
    "right_end": [(2, 2)],
    "right_mid": [(2, 5)],
    "up_end": [(2, 6)],
    "up_mid": [(2, 7)],
    "down_end": [(2, 8)],
    "down_mid": [(2, 9)]
}

# Power-ups e especiais
SPECIALS = {
    "bomb_up": [(2, 10)],
    "fire_up": [(2, 11)],
    "speed_up": [(3, 0)],
    "wall_hack": [(3, 1)],
    "remote": [(3, 2)],
    "bomb_pass": [(3, 3)],
    "flame_pass": [(3, 4)],
    "exit": [(3, 5)]
}

# Sprites dos inimigos
BALLOM = {
    "walk_left": [(3, 6), (3, 7), (3, 8)],
    "walk_right": [(3, 9), (3, 10), (3, 11)],
    "walk_up": [(4, 0), (4, 1), (4, 2)],
    "walk_down": [(4, 3), (4, 4), (4, 5)],
    "dead_anim": [(4, 6), (4, 7), (4, 8)]
}
ONIL = {
    "walk_left": [(4, 9), (4, 10), (4, 11)],
    "walk_right": [(5, 0), (5, 1), (5, 2)],
    "walk_up": [(5, 3), (5, 4), (5, 5)],
    "walk_down": [(5, 6), (5, 7), (5, 8)],
    "dead_anim": [(5, 9), (5, 10), (5, 11)]
}
DAHL = {
    "walk_left": [(6, 0), (6, 1), (6, 2)],
    "walk_right": [(6, 3), (6, 4), (6, 5)],
    "walk_up": [(6, 6), (6, 7), (6, 8)],
    "walk_down": [(6, 9), (6, 10), (6, 11)],
    "dead_anim": [(7, 0), (7, 1), (7, 2)]
}
MINVO = {
    "walk_left": [(7, 3), (7, 4), (7, 5)],
    "walk_right": [(7, 6), (7, 7), (7, 8)],
    "walk_up": [(7, 9), (7, 10), (7, 11)],
    "walk_down": [(8, 0), (8, 1), (8, 2)],
    "dead_anim": [(8, 3), (8, 4), (8, 5)]
}
DORIA = {
    "walk_left": [(8, 6), (8, 7), (8, 8)],
    "walk_right": [(8, 9), (8, 10), (8, 11)],
    "walk_up": [(9, 0), (9, 1), (9, 2)],
    "walk_down": [(9, 3), (9, 4), (9, 5)],
    "dead_anim": [(9, 6), (9, 7), (9, 8)]
}
OVAPE = {
    "walk_left": [(9, 9), (9, 10), (9, 11)],
    "walk_right": [(10, 0), (10, 1), (10, 2)],
    "walk_up": [(10, 3), (10, 4), (10, 5)],
    "walk_down": [(10, 6), (10, 7), (10, 8)],
    "dead_anim": [(10, 9), (10, 10), (10, 11)]
}
PASS = {
    "walk_left": [(11, 0), (11, 1), (11, 2)],
    "walk_right": [(11, 3), (11, 4), (11, 5)],
    "walk_up": [(11, 6), (11, 7), (11, 8)],
    "walk_down": [(11, 9), (11, 10), (11, 11)],
    "dead_anim": [(12, 0), (12, 1), (12, 2)]
}
PONTAN = {
    "walk_left": [(12, 3), (12, 4), (12, 5)],
    "walk_right": [(12, 6), (12, 7), (12, 8)],
    "walk_up": [(12, 9), (12, 10), (12, 11)],
    "walk_down": [(13, 0), (13, 1), (13, 2)],
    "dead_anim": [(13, 3), (13, 4), (13, 5)]
}

# Números pretos (para HUD)
NUMBERS_BLACK = {
    0: [(13, 6)],
    1: [(13, 7)],
    2: [(13, 8)],
    3: [(13, 9)],
    4: [(13, 10)],
    5: [(13, 11)],
    6: [(14, 0)],
    7: [(14, 1)],
    8: [(14, 2)],
    9: [(14, 3)]
}

# Números brancos (para HUD)
NUMBERS_WHITE = {
    0: [(14, 4)],
    1: [(14, 5)],
    2: [(14, 6)],
    3: [(14, 7)],
    4: [(14, 8)],
    5: [(14, 9)],
    6: [(14, 10)],
    7: [(14, 11)],
    8: [(15, 0)],
    9: [(15, 1)]
}

# Imagens de pontuação
SCORE_IMAGES = {
    10: [(15, 2)],
    50: [(15, 3)],
    100: [(15, 4)],
    200: [(15, 5)],
    400: [(15, 6)],
    800: [(15, 7)],
    1000: [(15, 8)]
}

# Palavras de interface
TIME_WORD = [(15, 9)]  # Coordenada para a palavra "TIME"
LEFT_WORD = [(15, 10)]  # Coordenada para a palavra "LEFT"
STAGE_WORD = [(15, 11)]  # Coordenada para a palavra "STAGE"

# Sons do jogo
SOUNDS = [
    "BM - 01 Title Screen.mp3",
    "BM - 02 Stage Start.mp3",
    "BM - 03 Main BGM.mp3",
    "BM - 04 Power-Up Get.mp3",
    "BM - 05 Stage Clear.mp3",
    "BM - 07 Special Power-Up Get.mp3",
    "BM - 09 Miss.mp3",
    "Bomberman SFX (1).wav",
    "Bomberman SFX (2).wav",
    "Bomberman SFX (3).wav",
    "Bomberman SFX (4).wav",
    "Bomberman SFX (5).wav",
    "Bomberman SFX (6).wav",
    "Bomberman SFX (7).wav"
]

# Conexões especiais (exemplo, ajuste conforme necessário)
SPECIAL_CONNECTIONS = {
    "bomb_up": "ballom",
    "fire_up": "onil",
    "speed_up": "dahl",
    "wall_hack": "minvo",
    "remote": "doria",
    "bomb_pass": "ovape",
    "flame_pass": "pass",
    "exit": "pontan"
}

# Pontuação dos inimigos
SCORES = {
    "ballom": 100,
    "onil": 200,
    "dahl": 400,
    "minvo": 800,
    "doria": 1000,
    "ovape": 2000,
    "pass": 4000,
    "pontan": 8000
}

# ... (restante do arquivo permanece igual)
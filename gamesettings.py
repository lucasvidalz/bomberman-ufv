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

# Coordenadas dos sprites (o restante permanece igual)
PLAYER = {
    "walk_left": [(0, 1), (0, 0), (0, 2)],
    "walk_right": [(1, 1), (1, 0), (1, 2)],
    "walk_up": [(2, 1), (2, 0), (2, 2)],
    "walk_down": [(3, 1), (3, 0), (3, 2)],
    "dead_anim": [(4, 0), (4, 1), (4, 2)]
}

# Blocos rígidos
HARD_BLOCK = {
    "hard_block": [(1, 0)]
}

# Blocos macios
SOFT_BLOCK = {
    "soft_block": [(1, 1)]
}

# Fundo
BACKGROUND = {
    "background": [(0, 3)]
}

# Bombas
BOMB = {
    "bomb": [(2, 0), (2, 1), (2, 2)]
}

# Explosões
EXPLOSIONS = {
    "centre": [(3, 0), (3, 1), (3, 2)],
    "left_end": [(4, 0)],
    "left_mid": [(4, 1)],
    "right_end": [(4, 2)],
    "right_mid": [(4, 3)],
    "up_end": [(5, 0)],
    "up_mid": [(5, 1)],
    "down_end": [(5, 2)],
    "down_mid": [(5, 3)]
}

# Power-ups e especiais
SPECIALS = {
    "bomb_up": [(6, 0)],
    "fire_up": [(6, 1)],
    "speed_up": [(6, 2)],
    "wall_hack": [(6, 3)],
    "remote": [(6, 4)],
    "bomb_pass": [(6, 5)],
    "flame_pass": [(6, 6)],
    "exit": [(6, 7)]
}

# Sprites dos inimigos
BALLOM = {
    "walk_left": [(7, 0), (7, 1), (7, 2)],
    "walk_right": [(8, 0), (8, 1), (8, 2)],
    "walk_up": [(9, 0), (9, 1), (9, 2)],
    "walk_down": [(10, 0), (10, 1), (10, 2)],
    "dead_anim": [(11, 0), (11, 1), (11, 2)]
}
ONIL = {
    "walk_left": [(7, 3), (7, 4), (7, 5)],
    "walk_right": [(8, 3), (8, 4), (8, 5)],
    "walk_up": [(9, 3), (9, 4), (9, 5)],
    "walk_down": [(10, 3), (10, 4), (10, 5)],
    "dead_anim": [(11, 3), (11, 4), (11, 5)]
}
DAHL = {
    "walk_left": [(7, 6), (7, 7), (7, 8)],
    "walk_right": [(8, 6), (8, 7), (8, 8)],
    "walk_up": [(9, 6), (9, 7), (9, 8)],
    "walk_down": [(10, 6), (10, 7), (10, 8)],
    "dead_anim": [(11, 6), (11, 7), (11, 8)]
}
MINVO = {
    "walk_left": [(7, 9), (7, 10), (7, 11)],
    "walk_right": [(8, 9), (8, 10), (8, 11)],
    "walk_up": [(9, 9), (9, 10), (9, 11)],
    "walk_down": [(10, 9), (10, 10), (10, 11)],
    "dead_anim": [(11, 9), (11, 10), (11, 11)]
}
DORIA = {
    "walk_left": [(12, 0), (12, 1), (12, 2)],
    "walk_right": [(13, 0), (13, 1), (13, 2)],
    "walk_up": [(14, 0), (14, 1), (14, 2)],
    "walk_down": [(15, 0), (15, 1), (15, 2)],
    "dead_anim": [(16, 0), (16, 1), (16, 2)]
}
OVAPE = {
    "walk_left": [(12, 3), (12, 4), (12, 5)],
    "walk_right": [(13, 3), (13, 4), (13, 5)],
    "walk_up": [(14, 3), (14, 4), (14, 5)],
    "walk_down": [(15, 3), (15, 4), (15, 5)],
    "dead_anim": [(16, 3), (16, 4), (16, 5)]
}
PASS = {
    "walk_left": [(12, 6), (12, 7), (12, 8)],
    "walk_right": [(13, 6), (13, 7), (13, 8)],
    "walk_up": [(14, 6), (14, 7), (14, 8)],
    "walk_down": [(15, 6), (15, 7), (15, 8)],
    "dead_anim": [(16, 6), (16, 7), (16, 8)]
}
PONTAN = {
    "walk_left": [(12, 9), (12, 10), (12, 11)],
    "walk_right": [(13, 9), (13, 10), (13, 11)],
    "walk_up": [(14, 9), (14, 10), (14, 11)],
    "walk_down": [(15, 9), (15, 10), (15, 11)],
    "dead_anim": [(16, 9), (16, 10), (16, 11)]
}

# Números pretos (para HUD)
NUMBERS_BLACK = {
    0: [(12, 12)],
    1: [(12, 13)],
    2: [(12, 14)],
    3: [(12, 15)],
    4: [(13, 12)],
    5: [(13, 13)],
    6: [(13, 14)],
    7: [(13, 15)],
    8: [(14, 12)],
    9: [(14, 13)]
}

# Números brancos (para HUD)
NUMBERS_WHITE = {
    0: [(14, 14)],
    1: [(14, 15)],
    2: [(15, 12)],
    3: [(15, 13)],
    4: [(15, 14)],
    5: [(15, 15)],
    6: [(16, 12)],
    7: [(16, 13)],
    8: [(16, 14)],
    9: [(16, 15)]
}

# Imagens de pontuação
SCORE_IMAGES = {
    10: [(16, 1)],
    50: [(16, 2)],
    100: [(16, 3)],
    200: [(16, 4)],
    400: [(16, 5)],
    800: [(16, 6)],
    1000: [(16, 7)]
}

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
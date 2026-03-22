# constants.py
# Constantes para tipos de célula, mapa, cores e configuração

import pygame

# --- Configuração da Grade ---
LARGURA_GRADE = 26
ALTURA_GRADE = 13
TAMANHO_CELULA = 40

# --- Configuração da Janela ---
LARGURA_JANELA = LARGURA_GRADE * TAMANHO_CELULA
ALTURA_JANELA = ALTURA_GRADE * TAMANHO_CELULA
FPS = 60

# --- Cores ---
COR_FUNDO = (255, 255, 255)
COR_RODOVIA = (190, 190, 190)
COR_RODOVIA2 = (211, 211, 211)
COR_RODOVIA3 = (200, 200, 200)
COR_INTERSECAO = (255, 165, 0) # Laranja
COR_EDIFICIO = (100, 100, 100)
COR_CARRO_RAPIDO = (255, 0, 0)   # Vermelho
COR_CARRO_MEDIO = (255, 255, 0)  # Amarelo
COR_CARRO_LENTO = (0, 255, 0)    # Verde
COR_AMBULANCIA = (0, 0, 255)     # Azul

COR_SEMAFORO_VERMELHO = (200, 0, 0)
COR_SEMAFORO_VERDE = (0, 200, 0)

# --- Mapeamento de Direções ---
# 0 = Edifício
# 'D' = Baixo, 'U' = Cima, 'R' = Direita, 'L' = Esquerda
# 'DR' = Baixo & Direita (Interseção)
# 'DL' = Baixo & Esquerda (Interseção)
# 'UR' = Cima & Direita (Interseção)
# 'UL' = Cima & Esquerda (Interseção)
#
# Interseções acontecem onde estradas se cruzam.
# Estradas horizontais: Linhas 3 (R), 4 (L), 8 (R), 9 (L)
# Estradas verticais:
# Colunas 3 (D), 4 (U)
# Colunas 9 (D), 10 (D)
# Colunas 15 (U), 16 (U)
# Colunas 21 (D), 22 (U)


def construir_mapa():
    grade = [['0' for _ in range(LARGURA_GRADE)] for _ in range(ALTURA_GRADE)]

    # Preencher estradas horizontais
    for r in (3, 8):
        for c in range(LARGURA_GRADE):
            grade[r][c] = 'R'
    for r in (4, 9):
        for c in range(LARGURA_GRADE):
            grade[r][c] = 'L'

    # Preencher estradas verticais e interseções
    colunas_verticais = {
        3: 'D', 4: 'U',
        9: 'D', 10: 'D',
        15: 'U', 16: 'U',
        21: 'D', 22: 'U'
    }

    for c, dir_vert in colunas_verticais.items():
        for r in range(ALTURA_GRADE):
            if grade[r][c] == '0':
                grade[r][c] = dir_vert
            else:
                dir_hor = grade[r][c]
                # É uma interseção
                grade[r][c] = f"{dir_vert}{dir_hor}"

    return grade

MAPA_GRADE = construir_mapa()

# Mapear direção para (dx, dy)
DESLOCAMENTOS_DIRECAO = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

# Pontos iniciais de surgimento de carros
# R -> aparece em col 0, linha 3 ou 8
# L -> aparece em col 25, linha 4 ou 9
# D -> aparece em linha 0, cols 3, 9, 10, 21
# U -> aparece em linha 12, cols 4, 15, 16, 22
PONTOS_APARECIMENTO = [
    (0, 3, 'R'), (0, 8, 'R'),
    (25, 4, 'L'), (25, 9, 'L'),
    (3, 0, 'D'), (9, 0, 'D'), (10, 0, 'D'), (21, 0, 'D'),
    (4, 12, 'U'), (15, 12, 'U'), (16, 12, 'U'), (22, 12, 'U')
]

# Configurações de ticks
CLOCK_TICK_MS = 200

# Velocidades = número de ticks necessários para mover 1 célula
VELOCIDADES = {
    'FAST': 1,
    'MEDIUM': 2,
    'SLOW': 4
}

# Configuração de probabilidade
MAX_CARS = 20
MIN_CARS = 10

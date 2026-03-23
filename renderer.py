import pygame
from constants import (LARGURA_GRADE, ALTURA_GRADE, TAMANHO_CELULA, LARGURA_JANELA, ALTURA_JANELA,
                       COR_FUNDO, COR_RODOVIA3, COR_INTERSECAO, COR_EDIFICIO,
                       COR_CARRO_RAPIDO, COR_CARRO_MEDIO, COR_CARRO_LENTO, COR_AMBULANCIA,
                       COR_SEMAFORO_VERMELHO, COR_SEMAFORO_VERDE, MAPA_GRADE)

class Renderizador:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
        pygame.display.set_caption("Simulador de Tráfego")
        self.fonte = pygame.font.SysFont(None, 24)

    def desenhar_fundo(self):
        for y in range(ALTURA_GRADE):
            for x in range(LARGURA_GRADE):
                rect = pygame.Rect(x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
                valor_celula = MAPA_GRADE[y][x]
                if valor_celula == '0':
                    pygame.draw.rect(self.tela, COR_EDIFICIO, rect)
                elif len(valor_celula) > 1:
                    pygame.draw.rect(self.tela, COR_INTERSECAO, rect)
                else:
                    pygame.draw.rect(self.tela, COR_RODOVIA3, rect)
                pygame.draw.rect(self.tela, (50, 50, 50), rect, 1)

    def desenhar_semaforos(self, gerenciador_semaforo):
        for inter in gerenciador_semaforo.intersecoes:
            cor_h = COR_SEMAFORO_VERDE if inter.direcao_verde == 'H' else COR_SEMAFORO_VERMELHO
            cor_v = COR_SEMAFORO_VERDE if inter.direcao_verde == 'V' else COR_SEMAFORO_VERMELHO

            inter_x = inter.faixa_x[0] * TAMANHO_CELULA
            inter_y = inter.faixa_y[0] * TAMANHO_CELULA

            pygame.draw.rect(self.tela, cor_h, (inter_x - 10, inter_y + 10, 10, 20))
            pygame.draw.rect(self.tela, cor_v, (inter_x + 10, inter_y - 10, 20, 10))

    def desenhar_carros(self, grade):
        with grade.lock_carros:
            for carro in grade.carros:
                if carro.eh_ambulancia:
                    cor = COR_AMBULANCIA
                elif carro.etiqueta_velocidade == 'FAST':
                    cor = COR_CARRO_RAPIDO
                elif carro.etiqueta_velocidade == 'MEDIUM':
                    cor = COR_CARRO_MEDIO
                else:
                    cor = COR_CARRO_LENTO

                rect = pygame.Rect(carro.x * TAMANHO_CELULA + 5, carro.y * TAMANHO_CELULA + 5, TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)
                pygame.draw.rect(self.tela, cor, rect)

    def renderizar(self, grade, gerenciador_semaforo, tick_atual):
        self.tela.fill(COR_FUNDO)
        self.desenhar_fundo()
        self.desenhar_semaforos(gerenciador_semaforo)
        self.desenhar_carros(grade)

        texto = self.fonte.render(f"Ticks: {tick_atual}", True, (255, 255, 255), (0, 0, 0))
        self.tela.blit(texto, (10, 10))

        pygame.display.flip()

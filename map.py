import threading
from constants import ALTURA_GRADE, LARGURA_GRADE, MAPA_GRADE, DESLOCAMENTOS_DIRECAO

class Grade:
    def __init__(self):
        # Um lock por célula
        self.locks = [[threading.Lock() for _ in range(LARGURA_GRADE)] for _ in range(ALTURA_GRADE)]

        # Acompanhar qual carro está em cada célula para renderizar e debugar
        self.carros = []
        self.lock_carros = threading.Lock() # Protege a lista de carros

    def adicionar_carro(self, carro):
        with self.lock_carros:
            self.carros.append(carro)

    def remover_carro(self, carro):
        with self.lock_carros:
            if carro in self.carros:
                self.carros.remove(carro)

    def posicao_valida(self, x, y):
        return 0 <= x < LARGURA_GRADE and 0 <= y < ALTURA_GRADE

    def adquirir(self, x, y):
        if self.posicao_valida(x, y):
            self.locks[y][x].acquire()

    def liberar(self, x, y):
        if self.posicao_valida(x, y):
            self.locks[y][x].release()

    def proxima_posicao(self, x, y, direcao):
        dx, dy = DESLOCAMENTOS_DIRECAO[direcao]
        return x + dx, y + dy

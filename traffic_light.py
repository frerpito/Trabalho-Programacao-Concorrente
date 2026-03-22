import threading
from constants import MAPA_GRADE

class Intersecao:
    def __init__(self, faixa_x, faixa_y):
        self.faixa_x = faixa_x
        self.faixa_y = faixa_y
        self.direcao_verde = 'H' # 'H' ou 'V'
        self.lock = threading.Lock()
        self.condicao = threading.Condition(self.lock)
        self.override_ambulancia = False

    def contem(self, x, y):
        return x in self.faixa_x and y in self.faixa_y

    def alternar(self):
        with self.condicao:
            if not self.override_ambulancia:
                self.direcao_verde = 'V' if self.direcao_verde == 'H' else 'H'
                self.condicao.notify_all()

    def definir_ambulancia(self, orientacao):
        # orientacao 'H' ou 'V'
        with self.condicao:
            self.override_ambulancia = True
            self.direcao_verde = orientacao
            self.condicao.notify_all()

    def limpar_ambulancia(self):
        with self.condicao:
            self.override_ambulancia = False
            self.condicao.notify_all()

    def aguardar_verde(self, orientacao_carro):
        """orientacao_carro 'H' (Direita/Esquerda) ou 'V' (Cima/Baixo)"""
        with self.condicao:
            while self.direcao_verde != orientacao_carro:
                self.condicao.wait()

class GerenciadorSemaforos(threading.Thread):
    def __init__(self, relogio):
        super().__init__()
        self.relogio = relogio
        self.intersecoes = []
        self._inicializar_intersecoes()
        self.executando = True

    def _inicializar_intersecoes(self):
        # 8 interseções
        # Linhas: 3,4 e 8,9
        # Colunas: 3,4 e 9,10 e 15,16 e 21,22
        grupos_x = [(3,4), (9,10), (15,16), (21,22)]
        grupos_y = [(3,4), (8,9)]

        for faixa_y in grupos_y:
            for faixa_x in grupos_x:
                self.intersecoes.append(Intersecao(faixa_x, faixa_y))

    def run(self):
        # a cada 15 ticks, alternar
        while self.executando:
            self.relogio.wait_ticks(15)
            if not self.executando:
                break
            for inter in self.intersecoes:
                inter.alternar()

    def obter_intersecao(self, x, y):
        for inter in self.intersecoes:
            if inter.contem(x, y):
                return inter
        return None

    def stop(self):
        self.executando = False

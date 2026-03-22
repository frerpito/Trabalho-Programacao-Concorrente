import uuid
import threading
from constants import VELOCIDADES

class Carro(threading.Thread):
    def __init__(self, grade, relogio, gerenciador_semáforo, inicio_x, inicio_y, direcao, etiqueta_velocidade):
        super().__init__()
        self.grade = grade
        self.relogio = relogio
        self.gerenciador_semaforo = gerenciador_semáforo
        self.x = inicio_x
        self.y = inicio_y
        self.direcao = direcao # 'U', 'D', 'L', 'R'
        self.etiqueta_velocidade = etiqueta_velocidade
        self.ticks_para_mover = VELOCIDADES[etiqueta_velocidade]
        self.executando = True
        self.finalizado = False
        self.eh_ambulancia = False
        self.id = str(uuid.uuid4())[:6]

    def run(self):
        # Espera inicial para não aparecer todos de uma vez se a célula já estiver ocupada
        while self.executando and not self.finalizado:
            self.grade.adquirir(self.x, self.y)
            break

        if not self.executando:
            return

        self.grade.adicionar_carro(self)

        while self.executando and not self.finalizado:
            self.relogio.wait_ticks(self.ticks_para_mover)
            if not self.executando:
                break

            nx, ny = self.grade.proxima_posicao(self.x, self.y, self.direcao)

            if not self.grade.posicao_valida(nx, ny):
                self.finalizado = True
                break

            intersecao_destino = self.gerenciador_semaforo.obter_intersecao(nx, ny)
            if intersecao_destino is not None:
                intersecao_atual = self.gerenciador_semaforo.obter_intersecao(self.x, self.y)
                if intersecao_atual is None:
                    orientacao = 'H' if self.direcao in ('L', 'R') else 'V'
                    if self.eh_ambulancia:
                        self.handle_ambulancia_aproxima(intersecao_destino, orientacao)
                    else:
                        intersecao_destino.aguardar_verde(orientacao)

            self.grade.adquirir(nx, ny)

            antigo_x, antigo_y = self.x, self.y
            self.x, self.y = nx, ny

            self.grade.liberar(antigo_x, antigo_y)

            if self.eh_ambulancia:
                self.handle_ambulancia_sai(antigo_x, antigo_y)

        self.grade.liberar(self.x, self.y)
        self.grade.remover_carro(self)

    def handle_ambulancia_aproxima(self, intersecao, orientacao):
        pass

    def handle_ambulancia_sai(self, antigo_x, antigo_y):
        pass

    def terminar(self):
        self.executando = False

from car import Carro

class Ambulancia(Carro):
    def __init__(self, grade, relogio, gerenciador_semáforo, inicio_x, inicio_y, direcao):
        super().__init__(grade, relogio, gerenciador_semáforo, inicio_x, inicio_y, direcao, 'FAST')
        self.eh_ambulancia = True
        self.intersecao_ativa = None

    def handle_ambulancia_aproxima(self, intersecao, orientacao):
        # Forçar interseção para verde na direção da ambulância
        intersecao.definir_ambulancia(orientacao)
        self.intersecao_ativa = intersecao

    def handle_ambulancia_sai(self, antigo_x, antigo_y):
        # Se acabamos de sair completamente de uma interseção
        intersecao_antiga = self.gerenciador_semaforo.obter_intersecao(antigo_x, antigo_y)
        intersecao_atual = self.gerenciador_semaforo.obter_intersecao(self.x, self.y)

        if intersecao_antiga is not None and intersecao_atual is None:
            intersecao_antiga.limpar_ambulancia()
            self.intersecao_ativa = None

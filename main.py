import pygame
import threading
import sys
import random

from constants import FPS, PONTOS_APARECIMENTO, MAX_CARS
from clock import GlobalClock
from map import Grade
from traffic_light import GerenciadorSemaforos
from car import Carro
from ambulance import Ambulancia
from renderer import Renderizador

def main():
    relogio = GlobalClock()
    grade = Grade()
    gerenciador_semaforo = GerenciadorSemaforos(relogio)

    relogio.start()
    gerenciador_semaforo.start()

    renderizador = Renderizador()
    executando = True
    pygame_clock = pygame.time.Clock()

    threads_carros = []
    ultimo_tick_spawn = 0

    try:
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False

            threads_carros = [c for c in threads_carros if c.is_alive()]

            ticks_atual = relogio.tick
            if ticks_atual - ultimo_tick_spawn >= 3 and len(threads_carros) < MAX_CARS:
                ponto = random.choice(PONTOS_APARECIMENTO)
                sx, sy, sdir = ponto

                if not grade.locks[sy][sx].locked():
                    existe_ambulancia = any(c.eh_ambulancia for c in threads_carros)
                    if not existe_ambulancia and len(threads_carros) > 5:
                        carro = Ambulancia(grade, relogio, gerenciador_semaforo, sx, sy, sdir)
                    else:
                        velocidade = random.choice(['FAST', 'MEDIUM', 'SLOW'])
                        carro = Carro(grade, relogio, gerenciador_semaforo, sx, sy, sdir, velocidade)

                    carro.start()
                    threads_carros.append(carro)
                    ultimo_tick_spawn = ticks_atual

            renderizador.renderizar(grade, gerenciador_semaforo, ticks_atual)
            pygame_clock.tick(FPS)
    except KeyboardInterrupt:
        pass
    finally:
        executando = False
        relogio.stop()
        gerenciador_semaforo.stop()

        for carro in threads_carros:
            carro.terminar()

        relogio.join()
        gerenciador_semaforo.join()
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    main()

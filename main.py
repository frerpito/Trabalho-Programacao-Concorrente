from map import Grade
from clock import GlobalClock
from traffic_light import GerenciadorSemaforos
import time

def main():
    print("Testando semáforos integrados...")
    relogio = GlobalClock()
    grade = Grade()
    semaforos = GerenciadorSemaforos(relogio)
    relogio.start()
    semaforos.start()
    time.sleep(1)
    relogio.stop()
    semaforos.stop()
    relogio.join()
    semaforos.join()

if __name__ == '__main__':
    main()

from map import Grade
from clock import GlobalClock
import time

def main():
    print("Testando relógio e simulação básica...")
    relogio = GlobalClock()
    grade = Grade()
    relogio.start()
    time.sleep(1)
    relogio.stop()
    relogio.join()

if __name__ == '__main__':
    main()

import time
from multiprocessing import Process, Semaphore


class Philosopher(Process):

    def __init__(self, name, leftFork, rightFork):
        Process.__init__(self)
        self.name = name
        self.leftFork = leftFork
        self.rightFork = rightFork

    # Na początku spotkania oraz po każdym posiłku filozofowie odczekują chwilę,
    # a następnie biorą się do pierwszej/kolejnej porcji
    def run(self):
        while True:
            time.sleep(1)
            print('%s want to eat. ' % self.name)
            self.eat()

    # Wybrany filozof próbuje chwycić jednoczeście do ręki lewy oraz prawy widelec.
    # Jeżeli mu się uda to przez chwilę spożywa posiłek, a następnie odkłada sztućce i udaje się na odpoczynek.
    # W innym wypadku odkłada widelec (jeżeli go trzyma) i wykonuje całą operację ponownie
    def eat(self):
        while True:
            self.leftFork.acquire()
            if self.rightFork.acquire(True):
                print('%s is eating now. ' % self.name)
                time.sleep(2)
                print('%s finishes eating and resting now. ' % self.name)
                self.rightFork.release()
                self.leftFork.release()
                return
            else:
                self.leftFork.release()


def main():
    # Stworzenie sztućców
    forks = []
    for i in range(5):
        forks.append(Semaphore())

    # Stworzenie listy gości i przypisanie każdemu pary sztućców
    names = ['Sokrates', 'Platon', 'Arystoteles', 'Heraklit', 'Demokryt']
    guestlist = []
    for i in range(len(names)):
        guestlist.append(Philosopher(names[i], forks[i], forks[i + 1])) if i < len(names) - 1\
            else guestlist.append(Philosopher(names[i], forks[i], forks[0]))

    # Rozpoczęcia posiłku
    for banqueter in guestlist:
        banqueter.start()

    time.sleep(15)

    # Zakończenie posiłku
    print("\nBanquet is finished")
    for philosopher in guestlist:
        philosopher.kill()

if __name__ == '__main__':
    main()
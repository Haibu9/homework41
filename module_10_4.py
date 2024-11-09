
from queue import Queue
from time import sleep
from random import randint
import threading

class Table:

    def __init__(self, number, guest=None):
        self.number, self.guest = number, guest

class Guest(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        sleep(randint(3, 10))

class Cafe:

    def __init__(self, *args):
        self.queue = Queue()
        self.tables = args

    def guest_arrival(self, *guests):
        guests = list(guests)
        for g in guests:
            for table in self.tables:
                if table.guest is None:
                    table.guest = g
                    g.start()
                    print(f"{g.name} сел(-а) за стол номер {table.number}")
                    guests.remove(g)
                    break
        for g in guests:
            self.queue.put(g)
            print(f"{g.name} в очереди")

    def discuss_guests(self):
        cheak = True
        while not self.queue.empty() or cheak:
            x = 0
            for t in self.tables:
                if not self.queue.qsize() and t.guest is None:
                    x += 1
                    if x == len(self.tables):
                        cheak = False
                if t.guest is not None and not t.guest.is_alive():
                    print(f"{t.guest.name} покушал(-а) и ушёл(ушла)и Стол номер {t.number} свободен")
                    t.guest = None
                    if not self.queue.empty():
                        t.guest = self.queue.get()
                        print(f"{t.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {t.number}")
                        print(f"{self.queue.qsize()} чееловек осталось в очереди")
                        t.guest.start()
        print("Рабочий день закончен!")




# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()

import threading
import time
import random
import datetime
from enum import Enum

terminate = False

class Valor:
    def __init__(self, item_id, name, transação):
        self.name = name
        self.item_id = item_id
        self.transação = transação
    name = ""
    item_id = 0
    transação = ""
    fila = []
    valor_lock = False

class Color(Enum):
    CYAN = 36
    RED = 31
    GREEN = 32
    BLUE = 34
    YELLOW = 33
    MAGENTA = 35

def assignColor(color : Color, message : str):
    return "\033[" + str(color.value) + "m" + message + "\033[0m"

x = Valor(1, "X", "")
y = Valor(2, "Y", "")
threads = []

def acessar():
    def value_lock(valor : Valor):
        if (valor.valor_lock == True):
            currentTime = datetime.datetime.now()
            valor.fila.append(threading.current_thread().name)
            print(assignColor(Color.CYAN, "Thread " + threading.current_thread().name + " travada, esperando por " + valor.name))
            while valor.valor_lock == True or valor.fila[0] != threading.current_thread().name:
                if currentTime + datetime.timedelta(seconds=50) < datetime.datetime.now():
                    print(assignColor(Color.RED, "Thread " + threading.current_thread().name + " espirou."))
                    valor.fila.remove(threading.current_thread().name)
                    return False
                time.sleep(1)
            valor.fila.remove(threading.current_thread().name)        
        
        valor.valor_lock = True
        print(assignColor(Color.YELLOW, valor.name + " bloqueado por " + threading.current_thread().name))
        time.sleep(random.randint(1,5))
        return True

    print(assignColor(Color.GREEN, "\n" + threading.current_thread().name + " começa sua execução."))

    time.sleep(random.randint(1,5))
    if not value_lock(x):
        acessar()
        return
    if not value_lock(y):
        x.valor_lock = False
        acessar()
        return

    x.valor_lock = False
    print(assignColor(Color.BLUE, "X desbloqueado por " + threading.current_thread().name))
    time.sleep(random.randint(1,5))
    y.valor_lock = False
    print(assignColor(Color.BLUE, "Y desbloqueado por " + threading.current_thread().name))
    time.sleep(random.randint(1,5))

    threads.remove(threading.current_thread())

    print(assignColor(Color.MAGENTA, threading.current_thread().name + " termina sua execução."))

def threadsBuild():
    while not terminate:
        newThread = threading.Thread(target=acessar, args=(), kwargs={})
        threads.append(newThread)
        newThread.start()
        time.sleep(random.randint(10,20))

print("Envie qualquer valor para sair.")

threadBuilder = threading.Thread(target=threadsBuild, args=(), kwargs={})
threadBuilder2 = threading.Thread(target=threadsBuild, args=(), kwargs={})
threadBuilder.start()
threadBuilder2.start()

input()
terminate = True

for t in threads:
    t.join()
threadBuilder.join()
threadBuilder2.join()

exit()
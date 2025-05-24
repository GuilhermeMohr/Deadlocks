import threading
import time
import random
import datetime

terminate = False

# outputList = []
# def terminal():
#     while not terminate:
#         time.sleep(random.randint(0.5))
#         if any(outputList):
#             for output in outputList:
#                 print(" | " + output)
#             print(" |")   

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

x = Valor(1, "X", "")
y = Valor(2, "Y", "")
threads = []

def acessar():
    def value_lock(valor : Valor):
        if (valor.valor_lock == True):
            currentTime = datetime.datetime.now()
            valor.fila.append(threading.current_thread().name)
            print("Thread " + threading.current_thread().name + " bloqueada, esperando por " + valor.name)
            while valor.valor_lock == True or valor.fila[0] != threading.current_thread().name:
                if currentTime + datetime.timedelta(seconds=50) < datetime.datetime.now():
                    print("Thread " + threading.current_thread().name + " espirou.")
                    valor.fila.remove(threading.current_thread().name)
                    return False
                time.sleep(1)
            valor.fila.remove(threading.current_thread().name)        
        
        valor.valor_lock = True
        print(valor.name + " bloqueado por " + threading.current_thread().name)
        time.sleep(random.randint(1,5))
        return True

    print("\n" + threading.current_thread().name + " começa sua execução.")

    time.sleep(random.randint(1,5))
    if not value_lock(x):
        acessar()
        return
    if not value_lock(y):
        x.valor_lock = False
        acessar()
        return

    x.valor_lock = False
    print("X desbloqueado por " + threading.current_thread().name)
    time.sleep(random.randint(1,5))
    y.valor_lock = False
    print("Y desbloqueado por " + threading.current_thread().name)
    time.sleep(random.randint(1,5))

    threads.remove(threading.current_thread())

    print(threading.current_thread().name + " termina sua execução.")

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
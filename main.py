import threading
import time
import random
import datetime
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt

terminate = False
waitForDeletionOfNode = threading.Event()

class Valor:
    def __init__(self, item_id, name, transacao):
        self.name = name
        self.item_id = item_id
        self.transacao = transacao
    name = ""
    item_id = 0
    transacao = ""
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

G = nx.DiGraph()
G.add_node("X", type="resource")
G.add_node("Y", type="resource")

def draw_graph():
    """
    Desenha o grafo de alocação de recursos em uma janela matplotlib.
    """
    plt.clf()
    pos = nx.spring_layout(G, seed=42)
    node_colors = []
    for node in G.nodes:
        if G.nodes[node].get("type") == "thread":
            node_colors.append("lightblue")
        else:
            node_colors.append("lightgreen")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        arrowsize=20,
        arrowstyle="->"
    )
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    plt.title("Resource Allocation Graph")
    plt.axis("off")
    plt.pause(0.1)

def acessar(waitForDeletionOfNode : threading.Event):
    def value_lock(valor : Valor):
        thread_name = threading.current_thread().name

        if not G.has_node(thread_name):
            G.add_node(thread_name, type="thread")
        G.add_edge(thread_name, valor.name, label="requests")
        #draw_graph()

        if (valor.valor_lock == True):
            currentTime = datetime.datetime.now()
            valor.fila.append(thread_name)
            print(assignColor(Color.CYAN, "Thread " + thread_name + " travada, aguardando por " + valor.name))
            while valor.valor_lock == True or valor.fila[0] != thread_name:
                if currentTime + datetime.timedelta(seconds=50) < datetime.datetime.now():
                    print(assignColor(Color.RED, "Thread " + thread_name + " expirou."))
                    valor.fila.remove(thread_name)
                    if G.has_edge(thread_name, valor.name):
                        G.remove_edge(thread_name, valor.name)
                        #draw_graph()
                    return False
                time.sleep(1)
            valor.fila.remove(thread_name)        
        
        valor.valor_lock = True
        valor.transacao = threading.current_thread().name

        if G.has_edge(thread_name, valor.name):
            G.remove_edge(thread_name, valor.name)
        G.add_edge(valor.name, thread_name, label="holds")
        #draw_graph()

        print(assignColor(Color.YELLOW, valor.name + " bloqueado por " + thread_name))
        time.sleep(random.randint(1,5))
        return True

    print(assignColor(Color.GREEN, "\n" + threading.current_thread().name + " inicializa sua execução."))

    rand = random.randint(0,1)
    time.sleep(random.randint(5,10))
    if (rand == 1):
        if not value_lock(x):
            acessar(waitForDeletionOfNode)
            return
        if not value_lock(y):
            if G.has_edge(x.name, threading.current_thread().name):
                G.remove_edge(x.name, threading.current_thread().name)
            if x.transacao == threading.current_thread().name:
                x.valor_lock = False
            acessar(waitForDeletionOfNode)
            return
    else:
        if not value_lock(y):
            acessar(waitForDeletionOfNode)
            return
        if not value_lock(x):
            if G.has_edge(y.name, threading.current_thread().name):
                G.remove_edge(y.name, threading.current_thread().name)
            if y.transacao == threading.current_thread().name:
                y.valor_lock = False
            acessar(waitForDeletionOfNode)
            return

    if G.has_edge(x.name, threading.current_thread().name):
        G.remove_edge(x.name, threading.current_thread().name)
        #draw_graph()
    x.valor_lock = False
    print(assignColor(Color.BLUE, "X desbloqueado por " + threading.current_thread().name))
    time.sleep(random.randint(5,10))

    if G.has_edge(y.name, threading.current_thread().name):
        G.remove_edge(y.name, threading.current_thread().name)
        #draw_graph()
    y.valor_lock = False
    print(assignColor(Color.BLUE, "Y desbloqueado por " + threading.current_thread().name))
    time.sleep(random.randint(5,10))

    #threads.remove(threading.current_thread())
    waitForDeletionOfNode.set()
    time.sleep(1)
    G.remove_node(threading.current_thread().name)
    time.sleep(1)
    waitForDeletionOfNode.clear()
    print(assignColor(Color.MAGENTA, threading.current_thread().name + " finaliza sua execução."))

def threadsBuild():
    while not terminate:
        newThread = threading.Thread(target=acessar, args=(waitForDeletionOfNode,))
        threads.append(newThread)
        newThread.start()
        time.sleep(random.randint(20,35))

print("ESC para terminar a execucao.")

plt.ion()
plt.figure(figsize=(8, 6))

threadBuilder = threading.Thread(target=threadsBuild)
threadBuilder2 = threading.Thread(target=threadsBuild)
threadBuilder.start()
threadBuilder2.start()

import keyboard
while True:
    if not waitForDeletionOfNode.is_set():
        try:
            draw_graph()
        except:
            pass
    if keyboard.is_pressed('esc'):
        print("Finalizando!")
        break

terminate = True

for t in threads:
    t.join()
threadBuilder.join()
threadBuilder2.join()
draw_graph()
plt.ioff()
plt.show()

exit()


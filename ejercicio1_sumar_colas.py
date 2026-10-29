"""Ejercicio 1: suma elemento a elemento de dos colas (con interfaz gráfica azul)."""
import tkinter as tk
from tkinter import messagebox

from tarea.cola import Cola

AZUL_OSCURO = "#0D47A1"
AZUL = "#1976D2"
AZUL_CLARO = "#BBDEFB"
AZUL_FONDO = "#E3F2FD"
BLANCO = "#FFFFFF"


def sumar_colas(cola_a, cola_b):
    """Recibe 2 colas de enteros y devuelve una nueva cola con sus elementos sumados
    uno a uno. Las colas originales no se modifican. Si una es más larga, los
    elementos sobrantes se suman con 0."""
    resultado = Cola()
    a, b = Cola(), Cola()
    for x in cola_a.a_lista():
        a.encolar(x)
    for x in cola_b.a_lista():
        b.encolar(x)

    while not a.esta_vacia() or not b.esta_vacia():
        va = a.desencolar() if not a.esta_vacia() else 0
        vb = b.desencolar() if not b.esta_vacia() else 0
        resultado.encolar(va + vb)
    return resultado


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 1 - Suma de Colas")
        self.configure(bg=AZUL_FONDO)
        self.geometry("720x520")
        self.minsize(640, 480)

        self.cola_a = Cola()
        self.cola_b = Cola()

        tk.Label(self, text="Suma de Colas", bg=AZUL_OSCURO, fg=BLANCO,
                 font=("Segoe UI", 20, "bold"), pady=12).pack(fill="x")

        marco = tk.Frame(self, bg=AZUL_FONDO)
        marco.pack(fill="both", expand=True, padx=15, pady=10)
        for i in range(3):
            marco.columnconfigure(i, weight=1, uniform="col")
        marco.rowconfigure(2, weight=1)

        self.lista_a = self._crear_columna(marco, 0, "Cola A", self.cola_a)
        self.lista_b = self._crear_columna(marco, 1, "Cola B", self.cola_b)

        tk.Label(marco, text="Cola Resultado", bg=AZUL_FONDO, fg=AZUL_OSCURO,
                 font=("Segoe UI", 12, "bold")).grid(row=0, column=2)
        tk.Label(marco, text="(A + B)", bg=AZUL_FONDO, fg=AZUL,
                 font=("Segoe UI", 10)).grid(row=1, column=2)
        self.lista_r = self._listbox(marco, 2, 2)

        botones = tk.Frame(self, bg=AZUL_FONDO)
        botones.pack(pady=(0, 15))
        self._boton(botones, "Sumar colas", self.sumar).pack(side="left", padx=5)
        self._boton(botones, "Cargar ejemplo", self.cargar_ejemplo).pack(side="left", padx=5)
        self._boton(botones, "Limpiar todo", self.limpiar).pack(side="left", padx=5)

    # ---------- utilidades de interfaz ----------
    def _boton(self, padre, texto, comando):
        return tk.Button(padre, text=texto, command=comando, bg=AZUL, fg=BLANCO,
                         activebackground=AZUL_OSCURO, activeforeground=BLANCO,
                         font=("Segoe UI", 11, "bold"), relief="flat",
                         padx=14, pady=6, cursor="hand2")

    def _listbox(self, padre, fila, columna):
        lb = tk.Listbox(padre, bg=BLANCO, fg=AZUL_OSCURO, font=("Consolas", 14),
                        justify="center", selectbackground=AZUL, relief="flat",
                        highlightthickness=2, highlightbackground=AZUL,
                        highlightcolor=AZUL_OSCURO)
        lb.grid(row=fila, column=columna, sticky="nsew", padx=8, pady=5)
        return lb

    def _crear_columna(self, padre, col, titulo, cola):
        tk.Label(padre, text=titulo, bg=AZUL_FONDO, fg=AZUL_OSCURO,
                 font=("Segoe UI", 12, "bold")).grid(row=0, column=col)
        fila_entrada = tk.Frame(padre, bg=AZUL_FONDO)
        fila_entrada.grid(row=1, column=col, pady=4)
        entry = tk.Entry(fila_entrada, width=8, font=("Segoe UI", 12), justify="center",
                         relief="solid", bd=1)
        entry.pack(side="left", padx=3)
        entry.bind("<Return>", lambda e: self.agregar(cola, entry, lb))
        lb = self._listbox(padre, 2, col)
        self._boton(fila_entrada, "Encolar",
                    lambda: self.agregar(cola, entry, lb)).pack(side="left")
        return lb

    # ---------- lógica ----------
    def agregar(self, cola, entry, listbox):
        try:
            valor = int(entry.get().strip())
        except ValueError:
            messagebox.showwarning("Dato inválido", "Ingresa un número entero.")
            return
        cola.encolar(valor)
        listbox.insert("end", valor)
        entry.delete(0, "end")
        entry.focus()

    def sumar(self):
        resultado = sumar_colas(self.cola_a, self.cola_b)
        self.lista_r.delete(0, "end")
        for x in resultado.a_lista():
            self.lista_r.insert("end", x)

    def cargar_ejemplo(self):
        self.limpiar()
        for x in (3, 4, 2, 8, 12):
            self.cola_a.encolar(x)
        for x in (6, 2, 9, 11, 3):
            self.cola_b.encolar(x)
        self._mostrar_colas()
        self.sumar()

    def _mostrar_colas(self):
        for lb, cola in ((self.lista_a, self.cola_a), (self.lista_b, self.cola_b)):
            lb.delete(0, "end")
            for x in cola.a_lista():
                lb.insert("end", x)

    def limpiar(self):
        # Se vacían las mismas colas (los botones ya apuntan a ellas)
        while not self.cola_a.esta_vacia():
            self.cola_a.desencolar()
        while not self.cola_b.esta_vacia():
            self.cola_b.desencolar()
        self.lista_r.delete(0, "end")
        self._mostrar_colas()


if __name__ == "__main__":
    App().mainloop()

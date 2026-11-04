import tkinter as tk
from tkinter import messagebox


# ==========================================
# 1. Estructura de Datos (Listas Enlazadas)
# ==========================================
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ColaEnlazada:
    def __init__(self):
        self.frente = None
        self.final = None
        self._tamanio = 0

    def esta_vacia(self) -> bool:
        return self.frente is None

    def encolar(self, elemento):
        nuevo_nodo = Nodo(elemento)
        if self.esta_vacia():
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self._tamanio += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("Error: la cola está vacía.")
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        self._tamanio -= 1
        if self.frente is None:
            self.final = None
        return dato

    def primero(self):
        if self.esta_vacia():
            raise IndexError("Error: la cola está vacía.")
        return self.frente.dato

    def __len__(self):
        return self._tamanio


# ==========================================
# 2. Interfaz Gráfica (Tkinter)
# ==========================================
class ColaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Cola con Lista Enlazada")
        self.root.geometry("820x450")
        self.root.resizable(False, False)
        self.root.config(bg="#f4f6f9")

        self.cola = ColaEnlazada()

        # Panel de controles superior
        frame_control = tk.Frame(self.root, bg="#ffffff", pady=15, padx=20, relief=tk.RIDGE, bd=1)
        frame_control.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)

        tk.Label(frame_control, text="Valor a encolar:", font=("Arial", 11, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=5)

        self.entrada_dato = tk.Entry(frame_control, font=("Arial", 11), width=12)
        self.entrada_dato.pack(side=tk.LEFT, padx=5)
        self.entrada_dato.focus()
        self.entrada_dato.bind("<Return>", lambda event: self.encolar_accion())

        btn_encolar = tk.Button(frame_control, text="Encolar (enqueue)", bg="#28a745", fg="white",
                                font=("Arial", 10, "bold"), padx=10, command=self.encolar_accion)
        btn_encolar.pack(side=tk.LEFT, padx=6)

        btn_desencolar = tk.Button(frame_control, text="Desencolar (dequeue)", bg="#dc3545", fg="white",
                                   font=("Arial", 10, "bold"), padx=10, command=self.desencolar_accion)
        btn_desencolar.pack(side=tk.LEFT, padx=6)

        btn_frente = tk.Button(frame_control, text="Ver Frente", bg="#17a2b8", fg="white",
                               font=("Arial", 10, "bold"), padx=10, command=self.ver_frente_accion)
        btn_frente.pack(side=tk.LEFT, padx=6)

        # Lienzo para graficar la cola y los nodos
        self.canvas = tk.Canvas(self.root, bg="#ffffff", height=240, relief=tk.SOLID, bd=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Barra de estado inferior
        self.lbl_estado = tk.Label(self.root, text="Cola vacía. Ingrese un elemento y presione 'Encolar'.",
                                   font=("Arial", 10), bg="#f4f6f9", fg="#333333", anchor="w")
        self.lbl_estado.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=8)

        self.actualizar_vista()

    def encolar_accion(self):
        valor = self.entrada_dato.get().strip()
        if not valor:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un dato para encolar.")
            return

        self.cola.encolar(valor)
        self.entrada_dato.delete(0, tk.END)
        self.lbl_estado.config(text=f"Se encoló '{valor}'. Total elementos: {len(self.cola)}", fg="#28a745")
        self.actualizar_vista()

    def desencolar_accion(self):
        try:
            elemento = self.cola.desencolar()
            self.lbl_estado.config(text=f"Se desencoló '{elemento}'. Total elementos: {len(self.cola)}", fg="#dc3545")
            self.actualizar_vista()
        except IndexError as err:
            messagebox.showerror("Error", str(err))

    def ver_frente_accion(self):
        try:
            primer_elem = self.cola.primero()
            messagebox.showinfo("Frente de la Cola", f"El primer elemento a salir es: {primer_elem}")
        except IndexError as err:
            messagebox.showinfo("Cola vacía", str(err))

    def actualizar_vista(self):
        self.canvas.delete("all")

        if self.cola.esta_vacia():
            self.canvas.create_text(400, 120, text="[ La cola está vacía ]", font=("Arial", 14, "italic"), fill="#888888")
            return

        x = 50
        y = 90
        ancho = 80
        alto = 50
        separacion = 50

        actual = self.cola.frente
        indice = 0

        while actual is not None:
            # Dibujo de la caja del nodo
            color_fondo = "#d1ecf1" if indice == 0 else "#e2e3e5"
            borde = "#0c5460" if indice == 0 else "#383d41"

            self.canvas.create_rectangle(x, y, x + ancho, y + alto, fill=color_fondo, outline=borde, width=2)
            self.canvas.create_text(x + (ancho / 2), y + (alto / 2), text=str(actual.dato), font=("Arial", 12, "bold"))

            # Etiquetas para el Frente y el Final
            if indice == 0:
                self.canvas.create_text(x + (ancho / 2), y - 20, text="FRENTE\n(head)", font=("Arial", 9, "bold"), fill="#0056b3", justify=tk.CENTER)

            if actual.siguiente is None:
                self.canvas.create_text(x + (ancho / 2), y + alto + 20, text="FINAL\n(tail)", font=("Arial", 9, "bold"), fill="#b02a37", justify=tk.CENTER)

            # Flecha apuntando al siguiente nodo o a 'None'
            if actual.siguiente is not None:
                self.canvas.create_line(x + ancho, y + (alto / 2), x + ancho + separacion, y + (alto / 2),
                                        arrow=tk.LAST, width=2, fill="#333333")
            else:
                self.canvas.create_line(x + ancho, y + (alto / 2), x + ancho + 35, y + (alto / 2),
                                        arrow=tk.LAST, width=2, fill="#6c757d")
                self.canvas.create_text(x + ancho + 55, y + (alto / 2), text="null", font=("Arial", 10, "italic"), fill="#6c757d")

            x += ancho + separacion
            actual = actual.siguiente
            indice += 1


if __name__ == "__main__":
    ventana = tk.Tk()
    app = ColaApp(ventana)
    ventana.mainloop()
"""Ejercicio 2: colas de servicios para una compañía de seguros (GUI azul).

Comandos (igual que por consola):
    C<n>  -> llega un cliente al servicio n y recibe su número de atención.
    A<n>  -> se atiende al siguiente cliente del servicio n.
Ejemplos: C1, C3, A1
"""
import tkinter as tk
from tkinter import messagebox

from tarea.cola import Cola

AZUL_OSCURO = "#0D47A1"
AZUL = "#1976D2"
AZUL_CLARO = "#BBDEFB"
AZUL_FONDO = "#E3F2FD"
BLANCO = "#FFFFFF"

# Servicios disponibles: número -> (nombre, prefijo del ticket)
SERVICIOS = {
    1: ("Siniestros", "S"),
    2: ("Pólizas nuevas", "P"),
    3: ("Pagos", "G"),
    4: ("Cancelaciones", "X"),
}


class SistemaAtencion:
    """Lógica del sistema: una Cola por servicio y un contador de tickets."""

    def __init__(self, servicios):
        self.servicios = servicios
        self.colas = {n: Cola() for n in servicios}
        self.contadores = {n: 0 for n in servicios}

    def _ticket(self, servicio, numero):
        prefijo = self.servicios[servicio][1]
        return f"{prefijo}-{numero:03d}"

    def llegada(self, servicio):
        """Un cliente llega: se le asigna el siguiente número del servicio."""
        self.contadores[servicio] += 1
        ticket = self._ticket(servicio, self.contadores[servicio])
        self.colas[servicio].encolar(ticket)
        return ticket

    def atender(self, servicio):
        """Llama al siguiente cliente. Devuelve el ticket o None si no hay nadie."""
        cola = self.colas[servicio]
        if cola.esta_vacia():
            return None
        return cola.desencolar()

    def procesar(self, comando):
        """Interpreta 'C<n>' o 'A<n>' y devuelve el mensaje a mostrar."""
        comando = comando.strip().upper()
        if len(comando) < 2 or comando[0] not in "CA" or not comando[1:].isdigit():
            raise ValueError("Comando inválido. Usa C<n> (llegada) o A<n> (atender). Ej: C1, A2")
        servicio = int(comando[1:])
        if servicio not in self.servicios:
            raise ValueError(f"El servicio {servicio} no existe (1 a {len(self.servicios)}).")
        nombre = self.servicios[servicio][0]
        if comando[0] == "C":
            ticket = self.llegada(servicio)
            return f"Cliente nuevo en «{nombre}». Su número de atención es {ticket}."
        ticket = self.atender(servicio)
        if ticket is None:
            return f"No hay clientes en espera en «{nombre}»."
        return f"Llamando al número {ticket} en «{nombre}»."


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 2 - Colas de Servicios (Seguros)")
        self.configure(bg=AZUL_FONDO)
        self.geometry("860x620")
        self.minsize(760, 560)

        self.sistema = SistemaAtencion(SERVICIOS)

        tk.Label(self, text="Compañía de Seguros · Turnos", bg=AZUL_OSCURO, fg=BLANCO,
                 font=("Segoe UI", 20, "bold"), pady=12).pack(fill="x")

        # Entrada de comandos
        barra = tk.Frame(self, bg=AZUL_FONDO)
        barra.pack(pady=(12, 4))
        tk.Label(barra, text="Comando (C1, A1...):", bg=AZUL_FONDO, fg=AZUL_OSCURO,
                 font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        self.entry = tk.Entry(barra, width=10, font=("Segoe UI", 14), justify="center",
                              relief="solid", bd=1)
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<Return>", lambda e: self.ejecutar())
        self.entry.focus()
        self._boton(barra, "Ejecutar", self.ejecutar).pack(side="left", padx=5)

        # Mensaje principal (lo que se "llama" o asigna)
        self.mensaje = tk.Label(self, text="Ingresa un comando para comenzar.",
                                bg=AZUL, fg=BLANCO, font=("Segoe UI", 14, "bold"),
                                wraplength=800, pady=14)
        self.mensaje.pack(fill="x", padx=15, pady=8)

        # Columnas por servicio
        marco = tk.Frame(self, bg=AZUL_FONDO)
        marco.pack(fill="both", expand=True, padx=15)
        self.listas = {}
        for i, (n, (nombre, _)) in enumerate(SERVICIOS.items()):
            marco.columnconfigure(i, weight=1, uniform="col")
            tk.Label(marco, text=f"{n}. {nombre}", bg=AZUL_OSCURO, fg=BLANCO,
                     font=("Segoe UI", 11, "bold"), pady=6).grid(row=0, column=i, sticky="ew", padx=4)
            lb = tk.Listbox(marco, bg=BLANCO, fg=AZUL_OSCURO, font=("Consolas", 14),
                            justify="center", relief="flat", selectbackground=AZUL,
                            highlightthickness=2, highlightbackground=AZUL,
                            highlightcolor=AZUL_OSCURO)
            lb.grid(row=1, column=i, sticky="nsew", padx=4, pady=(2, 4))
            fila = tk.Frame(marco, bg=AZUL_FONDO)
            fila.grid(row=2, column=i, pady=(0, 6))
            self._boton(fila, "Llegada", lambda s=n: self.ejecutar(f"C{s}"), chico=True).pack(side="left", padx=2)
            self._boton(fila, "Atender", lambda s=n: self.ejecutar(f"A{s}"), chico=True).pack(side="left", padx=2)
            self.listas[n] = lb
        marco.rowconfigure(1, weight=1)

        # Historial
        tk.Label(self, text="Historial", bg=AZUL_FONDO, fg=AZUL_OSCURO,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=18)
        self.historial = tk.Listbox(self, height=5, bg=AZUL_CLARO, fg=AZUL_OSCURO,
                                    font=("Segoe UI", 10), relief="flat")
        self.historial.pack(fill="x", padx=15, pady=(0, 12))

    def _boton(self, padre, texto, comando, chico=False):
        return tk.Button(padre, text=texto, command=comando, bg=AZUL, fg=BLANCO,
                         activebackground=AZUL_OSCURO, activeforeground=BLANCO,
                         font=("Segoe UI", 9 if chico else 11, "bold"), relief="flat",
                         padx=8 if chico else 14, pady=4 if chico else 6, cursor="hand2")

    def ejecutar(self, comando=None):
        if comando is None:
            comando = self.entry.get()
            self.entry.delete(0, "end")
        try:
            texto = self.sistema.procesar(comando)
        except ValueError as error:
            messagebox.showwarning("Comando inválido", str(error))
            return
        self.mensaje.config(text=texto)
        self.historial.insert(0, f"{comando.strip().upper()}: {texto}")
        self.refrescar()

    def refrescar(self):
        for n, lb in self.listas.items():
            lb.delete(0, "end")
            for ticket in self.sistema.colas[n].a_lista():
                lb.insert("end", ticket)


if __name__ == "__main__":
    App().mainloop()

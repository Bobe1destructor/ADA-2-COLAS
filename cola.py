"""Clase Cola (FIFO) usada por los dos ejercicios."""
from collections import deque


class Cola:
    def __init__(self):
        self._items = deque()

    def encolar(self, elemento):
        """Agrega un elemento al final de la cola."""
        self._items.append(elemento)

    def desencolar(self):
        """Quita y devuelve el elemento del frente. Lanza IndexError si está vacía."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._items.popleft()

    def frente(self):
        """Devuelve el elemento del frente sin quitarlo."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._items[0]

    def esta_vacia(self):
        return len(self._items) == 0

    def tamanio(self):
        return len(self._items)

    def a_lista(self):
        """Devuelve una copia de los elementos (frente primero), sin modificar la cola."""
        return list(self._items)

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Cola({self.a_lista()})"

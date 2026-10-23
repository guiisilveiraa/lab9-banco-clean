from abc import ABC, abstractmethod

from dominio import Conta


class IContaRepository(ABC):
    @abstractmethod
    def salvar(self, conta: Conta):
        pass

    @abstractmethod
    def buscar(self, numero: int):
        pass

    @abstractmethod
    def proximo_numero(self):
        pass
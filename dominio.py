from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Cliente:
    nome: str
    cpf: str


@dataclass
class Conta:
    numero: int
    cliente: Cliente
    saldo: Decimal
    historico: list = field(default_factory=list)

    def validar_movimentacao(self, valor):
        if not valor.is_finite() or valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        if valor != valor.quantize(Decimal("0.01")):
            raise ValueError("Use até duas casas decimais.")

    def depositar(self, valor):
        self.validar_movimentacao(valor)

        self.saldo += valor
        self.historico.append(f"Depósito: +R$ {valor:.2f}")

    def sacar(self, valor):
        self.validar_movimentacao(valor)

        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")

        self.saldo -= valor
        self.historico.append(f"Saque: -R$ {valor:.2f}")
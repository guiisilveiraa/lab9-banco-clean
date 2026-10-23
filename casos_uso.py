from decimal import Decimal, InvalidOperation

from dominio import Cliente, Conta
from repositorio import IContaRepository


class RealizarSaqueUseCase:
    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio

    def executar(self, numero, valor):
        conta = self.repositorio.buscar(numero)

        if conta is None:
            raise ValueError("Conta não encontrada.")

        conta.sacar(valor)
        self.repositorio.salvar(conta)

        return conta


class BancoService:
    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio
        self.realizar_saque = RealizarSaqueUseCase(repositorio)

    def converter_valor(self, texto):
        try:
            valor = Decimal(str(texto).replace(",", "."))

            if not valor.is_finite():
                raise ValueError

            if valor != valor.quantize(Decimal("0.01")):
                raise ValueError

            return valor

        except (InvalidOperation, ValueError):
            raise ValueError(
                "Informe um valor válido com até duas casas decimais."
            )

    def converter_numero(self, texto):
        try:
            numero = int(texto)
        except (ValueError, TypeError):
            raise ValueError("Informe um número de conta válido.")

        if numero <= 0:
            raise ValueError("Informe um número de conta válido.")

        return numero

    def criar_conta(self, nome, cpf, saldo_texto):
        nome = nome.strip()
        cpf = cpf.strip()

        if not nome or not cpf:
            raise ValueError("Preencha nome e CPF.")

        saldo = self.converter_valor(saldo_texto)

        if saldo < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")

        cliente = Cliente(nome, cpf)

        conta = Conta(
            numero=self.repositorio.proximo_numero(),
            cliente=cliente,
            saldo=saldo,
        )

        conta.historico.append(
            f"Abertura da conta: R$ {saldo:.2f}"
        )

        self.repositorio.salvar(conta)
        return conta

    def consultar_conta(self, numero_texto):
        numero = self.converter_numero(numero_texto)
        conta = self.repositorio.buscar(numero)

        if conta is None:
            raise ValueError("Conta não encontrada.")

        return conta

    def depositar(self, numero_texto, valor_texto):
        conta = self.consultar_conta(numero_texto)
        valor = self.converter_valor(valor_texto)

        conta.depositar(valor)
        self.repositorio.salvar(conta)

        return conta

    def sacar(self, numero_texto, valor_texto):
        numero = self.converter_numero(numero_texto)
        valor = self.converter_valor(valor_texto)

        return self.realizar_saque.executar(numero, valor)

    def consultar_historico(self, numero_texto):
        conta = self.consultar_conta(numero_texto)
        return list(conta.historico)
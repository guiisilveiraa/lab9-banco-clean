import json
from decimal import Decimal
from pathlib import Path

from dominio import Cliente, Conta
from repositorio import IContaRepository


class ArquivoContaRepository(IContaRepository):
    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def carregar(self):
        if not self.caminho.exists():
            return []

        try:
            texto = self.caminho.read_text(encoding="utf-8")
            return json.loads(texto)
        except (OSError, json.JSONDecodeError) as erro:
            raise ValueError(
                "Não foi possível ler o arquivo de contas."
            ) from erro

    def salvar(self, conta):
        registros = self.carregar()

        registro = {
            "numero": conta.numero,
            "nome": conta.cliente.nome,
            "cpf": conta.cliente.cpf,
            "saldo": str(conta.saldo),
            "historico": conta.historico,
        }

        for indice, existente in enumerate(registros):
            if existente["numero"] == conta.numero:
                registros[indice] = registro
                break
        else:
            registros.append(registro)

        temporario = self.caminho.with_suffix(".tmp")

        try:
            temporario.write_text(
                json.dumps(
                    registros,
                    ensure_ascii=False,
                    indent=4,
                ),
                encoding="utf-8",
            )

            temporario.replace(self.caminho)

        except OSError as erro:
            raise ValueError(
                "Não foi possível salvar o arquivo de contas."
            ) from erro

    def buscar(self, numero):
        for registro in self.carregar():
            if registro["numero"] == numero:
                cliente = Cliente(
                    nome=registro["nome"],
                    cpf=registro["cpf"],
                )

                return Conta(
                    numero=registro["numero"],
                    cliente=cliente,
                    saldo=Decimal(registro["saldo"]),
                    historico=list(registro["historico"]),
                )

        return None

    def proximo_numero(self):
        registros = self.carregar()

        return max(
            (registro["numero"] for registro in registros),
            default=0,
        ) + 1
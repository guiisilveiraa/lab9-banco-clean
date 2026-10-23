import tkinter as tk
from pathlib import Path

from casos_uso import BancoService
from infraestrutura import ArquivoContaRepository
from view import BancoView


def main():
    caminho = Path(__file__).resolve().parent / "contas.txt"

    repositorio = ArquivoContaRepository(caminho)
    servico = BancoService(repositorio)

    janela = tk.Tk()
    view = BancoView(janela, servico)

    janela.mainloop()


if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox


class BancoView:
    def __init__(self, janela, servico):
        self.servico = servico

        janela.title("Banco — Arquitetura Multicamadas")
        janela.geometry("560x700")

        tk.Label(
            janela,
            text="Gerenciamento bancário",
            font=("Arial", 16),
        ).pack(pady=10)

        self.nome = self.criar_campo(janela, "Nome")
        self.cpf = self.criar_campo(janela, "CPF")
        self.saldo = self.criar_campo(janela, "Saldo inicial")

        tk.Button(
            janela,
            text="Criar conta",
            command=self.criar_conta,
        ).pack(pady=8)

        self.numero = self.criar_campo(janela, "Número da conta")

        tk.Button(
            janela,
            text="Exibir dados da conta",
            command=self.consultar_conta,
        ).pack(pady=5)

        self.valor = self.criar_campo(
            janela,
            "Valor do depósito ou saque",
        )

        botoes = tk.Frame(janela)
        botoes.pack(pady=8)

        tk.Button(
            botoes,
            text="Depositar",
            command=self.depositar,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            botoes,
            text="Sacar",
            command=self.sacar,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            botoes,
            text="Exibir histórico",
            command=self.exibir_historico,
        ).pack(side=tk.LEFT, padx=5)

        self.resultado = tk.Text(
            janela,
            width=60,
            height=14,
            state=tk.DISABLED,
        )
        self.resultado.pack(pady=10)

    def criar_campo(self, janela, titulo):
        tk.Label(janela, text=titulo).pack()
        campo = tk.Entry(janela, width=45)
        campo.pack(pady=3)
        return campo

    def mostrar_texto(self, texto):
        self.resultado.config(state=tk.NORMAL)
        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(tk.END, texto)
        self.resultado.config(state=tk.DISABLED)

    def mostrar_conta(self, conta):
        saldo = f"{conta.saldo:.2f}".replace(".", ",")

        self.mostrar_texto(
            f"Conta: {conta.numero}\n"
            f"Nome: {conta.cliente.nome}\n"
            f"CPF: {conta.cliente.cpf}\n"
            f"Saldo: R$ {saldo}"
        )

        self.numero.delete(0, tk.END)
        self.numero.insert(0, str(conta.numero))

    def criar_conta(self):
        try:
            conta = self.servico.criar_conta(
                self.nome.get(),
                self.cpf.get(),
                self.saldo.get(),
            )
            self.mostrar_conta(conta)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def consultar_conta(self):
        try:
            conta = self.servico.consultar_conta(
                self.numero.get()
            )
            self.mostrar_conta(conta)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def depositar(self):
        try:
            conta = self.servico.depositar(
                self.numero.get(),
                self.valor.get(),
            )
            self.mostrar_conta(conta)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def sacar(self):
        try:
            conta = self.servico.sacar(
                self.numero.get(),
                self.valor.get(),
            )
            self.mostrar_conta(conta)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def exibir_historico(self):
        try:
            historico = self.servico.consultar_historico(
                self.numero.get()
            )

            self.mostrar_texto(
                "Histórico da conta\n\n" + "\n".join(historico)
            )
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))
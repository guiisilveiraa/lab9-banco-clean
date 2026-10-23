# Laboratório 9.3 — Arquitetura Clean

Sistema bancário em Python com interface gráfica Tkinter
e persistência em arquivo TXT.

## Funcionalidades

- Criar conta.
- Consultar dados da conta.
- Realizar depósitos.
- Realizar saques.
- Consultar histórico.
- Preservar os dados após fechar o programa.

## Organização

- dominio.py: entidades Cliente e Conta e regras de movimentação.
- repositorio.py: interface IContaRepository.
- casos_uso.py: operações da aplicação e RealizarSaqueUseCase.
- infraestrutura.py: implementação ArquivoContaRepository.
- view.py: interface gráfica.
- main.py: criação e conexão dos componentes.

## Inversão de dependência

O RealizarSaqueUseCase recebe um IContaRepository.

Ele não importa ArquivoContaRepository e não acessa arquivos.
A infraestrutura implementa a interface definida no núcleo.

O main.py injeta a implementação concreta na aplicação.

## Persistência

Os dados são armazenados em contas.txt, em formato textual JSON.
O arquivo é criado automaticamente ao salvar a primeira conta.

## Execução

Execute main.py usando Python com Tkinter disponível.

Não é necessário instalar bibliotecas externas.
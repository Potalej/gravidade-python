import matplotlib.animation as animation
import matplotlib.pyplot as plt
from pandas import read_csv
from numpy import arange
from auxiliares.hamiltoniano import H
from auxiliares.auxiliares import centro_massas, momentoAngular
from statistics import mean
from tabulate import tabulate
from time import time

DIM = 3
DIRBASE = "./fortran/simulacoes/"

def ler_csv (dir):
  tempo = time()
  print("Lendo o arquivo...")

  # captura com header para saber o tamanho
  df = read_csv(DIRBASE + dir, nrows=1)

  # quantidade de corpos
  massas = df.values.tolist()[0]
  N = len(massas)
  # a quantidade de posicoes sera 2 * N * dim
  qntdCols = 2 * N * DIM

  # agora le sem o cabecalho
  df = read_csv(DIRBASE + dir, header=None, skiprows=[0])
  valores = df.values.tolist()
  

  # converte o que foi lido em posicoes e momentos
  posicoes, momentos = [[] for i in range(N)], [[] for i in range(N)]
  print("Convertendo os dados...")
  for v in valores:
    for corpo in range(N):
      R = [v[corpo], v[corpo+DIM], v[corpo+2*DIM]]
      P = [v[N*DIM+corpo], v[N*DIM+corpo+DIM], v[N*DIM+corpo+2*DIM]]
      posicoes[corpo].append(R)
      momentos[corpo].append(P)

  tempo = round((time() - tempo)/10, 2)
  print(f"Dados capturados! ({tempo} ms)")

  return massas, posicoes, momentos

def visualizar (R:list):
  fig = plt.figure(figsize=(12,6), dpi=100)
  ax = fig.gca(projection='3d')
  for Ri in R:
    ax.scatter(*Ri[0])
    Ri = list(zip(*Ri))
    ax.plot(Ri[0], Ri[1], Ri[2])
  ax.set_xlim3d(*[-1000,1000])
  ax.set_ylim3d(*[-1000,1000])
  plt.show()

def visualizar_tempo_real (R:list):

  posicoes = list(zip(*R))

  fig = plt.figure(figsize=(12,6), dpi=100)
  ax = fig.gca(projection = '3d')

  def atualizar (t):
    ax.clear()
    Rs = posicoes[:t] if t > 0 else [posicoes[t]]
    Rs = list(zip(*Rs))
    for r in Rs:
      X, Y, Z = list(zip(*r))
      ax.plot(X, Y, Z)

  ani = animation.FuncAnimation(fig, atualizar, arange(len(posicoes)), interval=10, repeat=False)
  plt.show()

def estatisticas (m:list, R:list, P:list):
  """
    Exibe as estatísticas
  """
  infos = {
    "Jx": [], # momento angular
    "Jy": [], # momento angular
    "Jz": [], # momento angular
    "H": [], # energia
    "Rcmx": [], # centro de massas
    "Rcmy": [], # centro de massas
    "Rcmz": [], # centro de massas
    "Px": [],  # momento linear total
    "Py": [], # momento linear total
    "Pz": [] # momento linear total
  }
  R = list(zip(*R))
  P = list(zip(*P))

  for t in range(len(R)):

    Rt, Pt = R[t], P[t]

    J = momentoAngular(Rt, Pt)
    infos["Jx"] += [J[0]]
    infos["Jy"] += [J[1]]
    infos["Jz"] += [J[2]]

    Ptotal = [sum(list(zip(*Pt))[0]), sum(list(zip(*Pt))[1]), sum(list(zip(*Pt))[2])]
    infos["Px"] += [Ptotal[0]]
    infos["Py"] += [Ptotal[1]]
    infos["Pz"] += [Ptotal[2]]

    Rcm = centro_massas(m, Rt)
    infos["Rcmx"] += [Rcm[0]]
    infos["Rcmy"] += [Rcm[1]]
    infos["Rcmz"] += [Rcm[2]]

    energia = H(Rt, Pt, m)
    infos["H"] += [energia]
  
  # agora calcula as estatísticas
  H_info =  ["H",  infos["H"][0],  min(infos["H"]),  max(infos["H"]),  mean(infos["H"])]
  
  Jx_info = ["Jx", infos["Jx"][0], min(infos["Jx"]), max(infos["Jx"]), mean(infos["Jx"])]
  Jy_info = ["Jy", infos["Jy"][0], min(infos["Jy"]), max(infos["Jy"]), mean(infos["Jy"])]
  Jz_info = ["Jz", infos["Jz"][0], min(infos["Jz"]), max(infos["Jz"]), mean(infos["Jz"])]

  Px_info = ["Px", infos["Px"][0], min(infos["Px"]), max(infos["Px"]), mean(infos["Px"])]
  Py_info = ["Py", infos["Py"][0], min(infos["Py"]), max(infos["Py"]), mean(infos["Py"])]
  Pz_info = ["Pz", infos["Pz"][0], min(infos["Pz"]), max(infos["Pz"]), mean(infos["Pz"])]

  Rcmx_info = ["Rcmx", infos["Rcmx"][0], min(infos["Rcmx"]), max(infos["Rcmx"]), mean(infos["Rcmx"])]
  Rcmy_info = ["Rcmx", infos["Rcmy"][0], min(infos["Rcmy"]), max(infos["Rcmy"]), mean(infos["Rcmy"])]
  Rcmz_info = ["Rcmx", infos["Rcmz"][0], min(infos["Rcmz"]), max(infos["Rcmz"]), mean(infos["Rcmz"])]

  tabela = [H_info, Jx_info, Jy_info, Jz_info, Px_info, Py_info, Rcmx_info, Pz_info, Rcmy_info, Rcmz_info]
  tabela = tabulate(tabela, headers=["Integral", "Inicial", "Min", "Max", "Média"])
  print()
  print(tabela, end="\n\n")

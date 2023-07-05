import matplotlib.animation as animation
import matplotlib.pyplot as plt
from pandas import read_csv
from numpy import arange
from auxiliares.hamiltoniano import H
from auxiliares.auxiliares import centro_massas, momentoAngular
from statistics import mean
from tabulate import tabulate
from time import time
from os import mkdir
from moviepy.editor import *

DIM = 3
DIRBASE = "./fortran/simulacoes/"

def ler_csv (dir):
  tempo = time()
  print("Lendo o arquivo...")

  # captura com header para saber o tamanho
  df = read_csv(DIRBASE + dir, nrows=1, header=None)

  # quantidade de corpos
  massas = df.values.tolist()[0]
  N = len(massas)
  # a quantidade de posicoes sera 2 * N * dim
  qntdCols = 2 * N * DIM

  # agora le sem o cabecalho
  df = read_csv(DIRBASE + dir, header=None, skiprows=[0], dtype=float)
  # df = read_csv(DIRBASE + dir, header=None, skiprows=[0], dtype=float)
  valores = df.values.tolist()
  

  # converte o que foi lido em posicoes e momentos
  posicoes, momentos = [[] for i in range(N)], [[] for i in range(N)]
  print("Convertendo os dados...")
  # fator = 40
  fator = 1
  for v in valores:
    for corpo in range(N):
      # R = [v[corpo]/fator, v[corpo+DIM]/fator, v[corpo+2*DIM]/fator]
      R = [v[corpo]/fator, v[corpo+N]/fator, v[corpo+2*N]/fator]
      P = [v[N*DIM+corpo], v[N*DIM+corpo+N], v[N*DIM+corpo+2*N]] # arrumar esse tambem
      posicoes[corpo].append(R)
      momentos[corpo].append(P)

  print(momentos[0][0])
  print(momentos[1][0])
  print(momentos[2][0])
  print(momentos[3][0])

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
  ax.set_zlim3d(*[-1000,1000])
  plt.show()

def salvar_animacao (R:list):
  posicoes = list(zip(*R))

  pasta = str(round(time())) 
  mkdir(f'pontos/{pasta}')

  def atualizar (t):
    ax.clear()
    ax.set_xlim3d(*[-500,500])
    ax.set_ylim3d(*[-500,500])
    ax.set_zlim3d(*[-500,500])
    # plota as partículas
    Rs = posicoes[t]
    Rs = list(zip(*Rs))
    X, Y, Z = Rs
    ax.scatter(X, Y, Z, c="black")
  qntd = 100
  for i in range(int(len(posicoes)/qntd)):
    print('gerando frame ', i)
    funcao = lambda t: atualizar(qntd*i+t)
    fig = plt.figure(figsize=(12,6), dpi=100)
    ax = fig.gca(projection = '3d')
    ax.set_xlim3d(*[-500,500])
    ax.set_ylim3d(*[-500,500])
    ax.set_zlim3d(*[-500,500])
    ani = animation.FuncAnimation(fig, funcao, arange(qntd), interval=10, repeat=False)
    writervideo = animation.PillowWriter(fps=30)
    ani.save(f'pontos/{pasta}/frame{i}.gif', writer=writervideo)
    plt.close()
  
  # agora gera um arquivo de vídeo
  arquivos = []
  dir = lambda i: f'pontos/{pasta}/frame{i}.gif'
  for i in range(int(len(posicoes)/qntd)):
    clip = VideoFileClip(dir(i))
    # clip.fx(vfx.speedx,2)
    arquivos.append(clip)
  # concatena e salva
  final = concatenate_videoclips(arquivos)
  final.write_videofile(f'pontos/{pasta}/video_{pasta}.mp4')
  
def gerar_video (pasta, inicio, fim):
  dir = lambda i: f'pontos/{pasta}/frame{i}.gif'
  # gera um video a partir do range 
  arquivos = []
  for i in range(inicio, fim):
    clip = VideoFileClip(dir(i))
    arquivos.append(clip)
  #concatena e salva
  final = concatenate_videoclips(arquivos)
  final.write_videofile(f'pontos/{pasta}/video_{pasta}_{inicio}_{fim}.mp4')

def visualizar_tempo_real (R:list):

  posicoes = list(zip(*R))

  fig = plt.figure(figsize=(12,6), dpi=100)
  ax = fig.gca(projection = '3d')

  def atualizar (t):
    ax.clear()
    ax.set_xlim3d(*[-1000,1000])
    ax.set_ylim3d(*[-1000,1000])
    ax.set_zlim3d(*[-1000,1000])
    # plota as partículas
    Rs = posicoes[t]
    for r in Rs:
      X, Y, Z = r
      ax.scatter(X, Y, Z, c="black")

  ax.set_xlim3d(*[-1000,1000])
  ax.set_ylim3d(*[-1000,1000])
  ax.set_zlim3d(*[-1000,1000])
  ani = animation.FuncAnimation(fig, atualizar, arange(len(posicoes)), interval=100, repeat=False)
  plt.show()

def estatisticas (m:list, R:list, P:list, G:float):
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

    energia = H(Rt, Pt, m, G)
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

  tabela = [H_info, Jx_info, Jy_info, Jz_info, Px_info, Py_info, Pz_info, Rcmx_info, Rcmy_info, Rcmz_info]
  tabela = tabulate(tabela, headers=["Integral", "Inicial", "Min", "Max", "Média"])
  print()
  print(tabela, end="\n\n")

  fig, ax = plt.subplots(1, 4, figsize=(16,8))
  
  ax[0].plot(infos["H"], label="H")
  ax[0].set_ylabel("H")
  ax[0].legend()
  
  ax[1].plot(infos["Jx"], label="Jx")
  ax[1].plot(infos["Jy"], label="Jy")
  ax[1].plot(infos["Jz"], label="Jz")
  ax[1].legend()

  ax[2].plot(infos["Px"], label="Px")
  ax[2].plot(infos["Py"], label="Py")
  ax[2].plot(infos["Pz"], label="Pz")
  ax[2].legend()

  ax[3].plot(infos["Rcmx"], label="Rcmx")
  ax[3].plot(infos["Rcmy"], label="Rcmy")
  ax[3].plot(infos["Rcmz"], label="Rcmz")
  ax[3].legend()
  
  plt.show()
  

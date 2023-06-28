import matplotlib.animation as animation
import matplotlib.pyplot as plt
from numpy import arange
from moviepy.editor import *

from simulacao.simular import Simulacao
from auxiliares.auxiliares import centro_massas, momento_inercia_cm, momentoAngular
from auxiliares.hamiltoniano import H, U, EC
from time import time
import os

from tabulate import tabulate

class Simulacao3D (Simulacao):

  def __init__ (self, massas:list, R0: list, P0: list, h:float=0.05, G:float=1):
    super().__init__(massas=massas, R0=R0, P0=P0, h=h, G=G)
    self.G = G
    self.exibir_centro_massas = False
    self.xlim = [-1000,1000]
    self.ylim = [-1000,1000]
    self.zlim = [-1000,1000]

  def passo_integracao (self, infosImediatas=False, centroMassas=False):
    self.R, self.P, self.posicoes, self.momentos_lineares = self.metodo.aplicarNVezes(self.R, self.P, n=self.n)
    # se quiser usar somente as informacoes imediatas
    if infosImediatas:
      # energia
      self.E = H(self.R, self.P, self.massas, self.G)
      # momento angular
      self.J = momentoAngular(self.R, self.P)
      # centro de massas
      self.rcm = centro_massas(self.massas, self.R)
      # momento linear total
      self.Ptot = [sum(p) for p in list(zip(*self.P))]
    # ou se quiser somente o centro de massas tambem
    elif centroMassas:
      self.rcm = centro_massas(self.massas, self.R)
    return self.R, self.P

  def integracao (self, infosImediatas=False, centroMassas=False):
    for _ in range(self.qntdFrames+1):
      self.passo_integracao(infosImediatas=infosImediatas, centroMassas=centroMassas)
      yield self.R, self.P
  
  def simular_salvar (self):
    self.nomeArquivo = f"pontos_{time()}.txt"
    YK = []
    self.abrirArquivo(self.massas, self.nomeArquivo)
    for frame in self.integracao(infosImediatas=False):
      R, P = frame
      yk = []
      for i in range(self.quantidade_corpos):
        for j in range(self.dimensao):
          yk += [R[i][j], P[i][j]]
      YK.append(yk)

      if len(YK) == self.QUANTIDADE_ANTES_SALVAR:
        self.salvarPontos(YK, self.nomeArquivo)
        YK = []

    if len(YK) >= 0:
      self.salvarPontos(YK, self.nomeArquivo)

  def simular_exibir (self):
    self.fig = plt.figure(figsize=(12,6), dpi=100)
    self.ax = self.fig.add_subplot(projection = '3d')
    ani = animation.FuncAnimation(self.fig, self.atualizar, arange(self.qntdFrames), interval=10, repeat=False)
    plt.show()

  def simular (self, qntdFrames:int=0, exibir:bool=True, salvar:bool=False)->str:
    """
      Faz uma simulação 3d usando as condições iniciais informadas.
    """
    self.qntdFrames = qntdFrames

    if salvar: self.simular_salvar()

    elif exibir: self.simular_exibir()

    # se nao for salvar nem exibir, apenas apresentar dados
    else:
      Rs, Ps = [], []
      t0 = time()
      for frame in self.integracao():
        # resultado do metodo
        R, P = frame
        # salva trajetorias
        Rs.append(R)
        # salva momentos linears totais
        Ps.append([sum(pi) for pi in list(zip(*P))])

      print('TEMPO:', time() - t0, end='\n\n')

      ###########################
      #       informacoes       #
      ###########################
      # Es, Js, Ps_tot, Rcms = self.informacoes(Rs, Ps)

      ###########################
      #         graficos        #
      ###########################
      # self.info_graficos(Es, Js, Ps_tot, Rcms)      

      # visualizacao 
      self.visualizacao(Rs)
    
  def visualizar (self, R:list, salvar:bool=True):
    """
      Para somente visualizar uma lista já em mãos.
    """
    if salvar:
      pasta = str(round(time())) 
      os.mkdir(f'pontos/{pasta}')
    # vai de 1000 em 1000
    for i in range(int(len(R)/100)):
      self.funcao = lambda t: (R[100*i+t], 0, 0)
      self.fig = plt.figure(figsize=(12,6), dpi=100)
      self.ax = self.fig.add_subplot(projection = '3d')
      ani = animation.FuncAnimation(self.fig, self.atualizar, arange(100), interval=10,  repeat=False)
      if not salvar:
        plt.show()
      else:
        writervideo = animation.PillowWriter(fps=60)
        ani.save(f'pontos/{pasta}/frame{i}.gif', writer=writervideo)
        plt.close()
    if salvar:
      # agora gera um arquivo de vídeo
      arquivos = []
      dir = lambda i: f'pontos/{pasta}/frame{i}.gif'
      for i in range(int(len(R)/100)):
        clip = VideoFileClip(dir(i))
        clip.fx(vfx.speedx, 2)
        arquivos.append(clip)
      # concatena e salva
      final = concatenate_videoclips(arquivos)
      final.write_videofile(f'pontos/{pasta}/video.mp4')

  def atualizar (self, t):
    """
      Função auxiliar para visualizações 3d.
    """
    R, P = self.passo_integracao(infosImediatas=False, centroMassas=True)
    print('energia: ', H(R, P, self.massas, self.G))
    print('momento angular: ', momentoAngular(R, P))
    print()
    # salva
    try: self.Rs.append(R)
    except: self.Rs = [R]
    Ra = list(zip(*self.Rs))
    # limpa o desenho
    self.ax.clear()
    # plota as trajetórias
    for i in range(len(self.massas)):
      X, Y, Z = list(zip(*Ra[i]))
      self.ax.plot(X, Y, Z, c="black") # era 3
    # plota o centro de massas se quiser
    if self.exibir_centro_massas:
      self.ax.scatter(self.rcm[0], self.rcm[1], self.rcm[2], color="red")

  def informacoes (self, Rs, Ps):
    # energia
    Es = self.Es
    E_info = ["H", self.E0, min(Es), max(Es), sum(Es)/len(Es)]
    
    # momento angular
    Js = list(zip(*self.Js))
    Js[0] = [self.J0[0]] + list(Js[0])
    Js[1] = [self.J0[1]] + list(Js[1])
    Js[2] = [self.J0[2]] + list(Js[2])
    
    Jx_info = ["Jx", self.J0[0], min(Js[0]), max(Js[0]), sum(Js[0])/len(Js[0])]
    Jy_info = ["Jy", self.J0[1], min(Js[1]), max(Js[1]), sum(Js[1])/len(Js[1])]
    Jz_info = ["Jz", self.J0[2], min(Js[2]), max(Js[2]), sum(Js[2])/len(Js[2])]

    # momento linear
    Ps_tot = list(zip(*Ps))
    Ps_tot[0] = [self.P0_tot[0]] + list(Ps_tot[0])
    Ps_tot[1] = [self.P0_tot[1]] + list(Ps_tot[1])
    Ps_tot[2] = [self.P0_tot[2]] + list(Ps_tot[2])
    
    Px_info = ["Px", self.P0_tot[0], min(Ps_tot[0]), max(Ps_tot[0]), sum(Ps_tot[0])/len(Ps_tot[0])]
    Py_info = ["Py", self.P0_tot[1], min(Ps_tot[1]), max(Ps_tot[1]), sum(Ps_tot[1])/len(Ps_tot[1])]
    Pz_info = ["Pz", self.P0_tot[2], min(Ps_tot[2]), max(Ps_tot[2]), sum(Ps_tot[2])/len(Ps_tot[2])]

    # centro de massas
    Rcms = list(zip(*[centro_massas(self.massas, Rsa) for Rsa in Rs]))
    Rcmx = ["Rcmx"] + list(Rcms[0])
    Rcmy = ["Rcmy"] + list(Rcms[1])
    Rcmz = ["Rcmz"] + list(Rcms[2])

    tabela = [E_info, Jx_info, Jy_info, Jz_info, Px_info, Py_info, Pz_info, Rcmx, Rcmy, Rcmz]
    tabela = tabulate(tabela, headers=["Integral", "Inicial", "Min", "Max", "Média"])
    print(f'\n{tabela}\n')

    return Es, Js, Ps_tot, Rcms

  def info_graficos (self, Es, Js, Ps_tot, Rcms):
    fig, ax = plt.subplots(1, 4, figsize=(16,8))

    ax[0].plot(Es, label="H")
    ax[0].set_ylabel("H")
    ax[0].legend()
    
    ax[1].plot(Js[0], label="Jx")
    ax[1].plot(Js[1], label="Jy")
    ax[1].plot(Js[2], label="Jz")
    ax[1].legend()

    ax[2].plot(Ps_tot[0], label="Px")
    ax[2].plot(Ps_tot[1], label="Py")
    ax[2].plot(Ps_tot[2], label="Pz")
    ax[2].legend()

    ax[3].plot(Rcms[0], label="Rcmx")
    ax[3].plot(Rcms[0], label="Rcmy")
    ax[3].plot(Rcms[0], label="Rcmz")
    ax[3].legend()
    
    plt.show()

  def visualizacao (self, Rs):
    self.fig = plt.figure(figsize=(12,6), dpi=100)
    self.ax = self.fig.add_subplot(projection='3d')
    Rs = list(zip(*Rs))
    for i in range(self.quantidade_corpos):
      Ri = list(zip(*Rs[i]))
      self.ax.plot(Ri[0],Ri[1],Ri[2])
      self.ax.scatter(*Rs[i][0])
    self.ax.set_xlim3d(*[-1000, 1000])
    self.ax.set_ylim3d(*[-1000, 1000])
    plt.show()

  def desigualdade_sundman (self, Rs, Ps):
    # quadrado da norma do momento angular
    indice_maximo = 0
    norma2_J = []
    for i, J in enumerate(self.JsPasso):
      c2 = sum(ji**2 for ji in J)
      if i > 0:
        if c2 >= max(norma2_J):
          indice_maximo = i
      norma2_J.append(c2)

    # 2 I T
    limitante_J = [
      2 * momento_inercia_cm(self.massas, Rs[i]) * EC(Ps[i], self.massas) for i in range(len(Rs))
    ]

    foi_falso = 0
    for i in range(len(norma2_J)):
      if norma2_J[i] > limitante_J[i]:
        foi_falso += 1

    print()
    print('DESIGUALDADE DE SUNDMAN: ||J||2 <= 2IT ?')
    print('Maximo: ', norma2_J[indice_maximo], limitante_J[indice_maximo])
    print('Foi falso', foi_falso, 'vezes')
    print()
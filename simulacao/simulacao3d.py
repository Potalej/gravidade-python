import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
from moviepy.editor import *
from math import sqrt

from auxiliares.shapedynamics import mudar_somente_posicao, momento_dilatacao
from simulacao.simular import Simulacao
from auxiliares.auxiliares import centro_massas, momento_inercia_cm, momentoAngular, norma2
from auxiliares.hamiltoniano import H, U, EC
from time import time
import os

from tabulate import tabulate

import config.configs as config

class Simulacao3D (Simulacao):
  """
    Para fazer simulacoes tridimensionais bem legais.

    Parametros
    ----------
    massas : list
      Lista de massas das particulas.
    R0 : list
      Lista de posicoes iniciais.
    P0 : list
      Lista de momentos lineares iniciais.
    h : float = 0.05
      Tamanho do passo de integracao.
    G : float = 1
      Constante de gravitacao universal.
    integrador : str = 'rk4'
      Integrador da simulacao. Por padrao eh o RK4
    corrigir : bool = False
      Aplicar ou nao a correcao via KKT 1a ordem
    colidir : bool = False
      Aplicar ou nao as colisoes
    visualizar_2d : bool = False
      Se quiser visualizar em 2 dimensoes apenas
  """
  
  def __init__ (
      self,
      massas        : list,
      R0            : list,
      P0            : list,
      h             : float = 0.05,
      G             : float = 1,
      integrador    : str   = 'rk4',
      corrigir      : bool  = False,
      colidir       : bool  = False,
    ):
    super().__init__(massas=massas, R0=R0, P0=P0, h=h, G=G, integrador=integrador, corrigir=corrigir, colidir=colidir)
    self.G = G
    self.exibir_centro_massas = False

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

  def simular_exibir_2d (self):
    self.visualizar_sd = False
    self.visualizar_2d = True
    self.fig = plt.figure(figsize=(12,6), dpi=config.ANIMACAO_DPI)
    self.ax = self.fig.add_subplot()
    ani = animation.FuncAnimation(self.fig, self.atualizar, arange(self.qntdFrames), interval=config.ANIMACAO_INTERVALO, repeat=False)
    plt.show()

  def simular_exibir (self):
    self.exibir_sd = False
    self.visualizar_2d = False
    self.fig = plt.figure(figsize=(12,6), dpi=config.ANIMACAO_DPI)
    self.ax = self.fig.add_subplot(projection = '3d')
    ani = animation.FuncAnimation(self.fig, self.atualizar, arange(self.qntdFrames), interval=config.ANIMACAO_INTERVALO, repeat=False)
    plt.show()

  def simular_exibir_sd (self):
    self.exibir_sd = True
    self.visualizar_2d = False
    self.fig = plt.figure(figsize=(12,6), dpi=config.ANIMACAO_DPI)
    self.ax = self.fig.add_subplot(projection = '3d')
    ani = animation.FuncAnimation(self.fig, self.atualizar, arange(self.qntdFrames), interval=config.ANIMACAO_INTERVALO, repeat=False)
    plt.show()

  def simular (self, qntdFrames:int=0, visualizacao:str='3d', salvar:bool=False, expandir:bool=True)->str:
    """
      Faz uma simulação 3d usando as condições iniciais informadas.
    """
    self.qntdFrames = qntdFrames
    self.expandir = expandir

    if salvar: self.simular_salvar()

    elif visualizacao == '2d': 
      self.visualizacao_2d = True
      self.simular_exibir_2d()

    elif visualizacao == '3d': 
      self.simular_exibir()

    elif visualizacao == 'sd':
      self.simular_exibir_sd()

    # se nao for salvar nem exibir, apenas apresentar dados
    else:
      Rs, Ps = [], []
      t0 = time()
      qntd = 0
      for frame in self.integracao():
        # resultado do metodo
        R, P = frame
        # Salva as trajetorias
        try: self.Rs.append(R)
        except: self.Rs = [R]
        try: self.Ps.append(P)
        except: self.Ps = [P]
        qntd += 1
        if qntd % 100 == 0: print(qntd)
      
      print('TEMPO:', time() - t0, end='\n\n')

  def visualizar (self, R:list, salvar:bool=True):
    """
      Para somente visualizar uma lista ja em maos.
    """
    if salvar:
      pasta = str(round(time())) 
      os.mkdir(f'pontos/{pasta}')

    for i in range(len(R)):
      self.funcao = lambda t: (R[i+t], 0, 0)
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
    Atualiza os frames.
    """
    # integra
    R, P = self.passo_integracao(infosImediatas=False, centroMassas=True)
    # salva
    try: self.Rs.append(R)
    except: self.Rs = [R]
    try: self.Ps.append(P)
    except: self.Ps = [P]

    # limpa o desenho
    self.ax.clear()

    # verifica se quer exibir o normal ou o SD
    if self.visualizar_2d:
      self.atualizar_2d(t, R, P)
    elif self.exibir_sd:
      self.atualizar_sd(t, R, P)
    else:
      self.atualizar_coord(t)

  def atualizar_2d (self, t, R, P):
    """
      Atualiza a animacao na visao 2d.
    """
    self.ax.set_xlim(config.RANGE_PLOT_X)
    self.ax.set_ylim(config.RANGE_PLOT_Y)

    # Separa as coordenadas
    Rs = list(zip(*self.Rs))
    for i in range(len(self.massas)):
      X, Y, Z = list(zip(*Rs[i]))

      if self.expandir:
        # Verifica se precisa aumentar o tamanho do plot
        if X[-1] < config.RANGE_PLOT_X[0] or X[-1] > config.RANGE_PLOT_X[1]:
          config.RANGE_PLOT_X = [2*x for x in config.RANGE_PLOT_X]
        if Y[-1] < config.RANGE_PLOT_Y[0] or Y[-1] > config.RANGE_PLOT_Y[1]:
          config.RANGE_PLOT_Y = [2*y for y in config.RANGE_PLOT_Y]

      self.ax.scatter(X[-1], Y[-1])
      
      if config.TAMANHO_RASTRO_ANIMACOES > 0:
        tamanho_rastro = min([config.TAMANHO_RASTRO_ANIMACOES, len(X)-1])      
        self.ax.plot(X[-tamanho_rastro:-1], Y[-tamanho_rastro:-1], c='black')
    
  def atualizar_sd (self, t, R, P, plotar_circulo:bool=True):
    """
      Atualiza a animacao na visao da SD.
    """
    # aplica as transformacoes de coordenada da SD
    R_sp = mudar_somente_posicao(self.massas, R)
    # salva o Rsp
    try: self.Rs_sp.append(R_sp)
    except: self.Rs_sp = [R_sp]
    # separa as coordenadas
    Ra = list(zip(*self.Rs_sp))
    
    # plota o circulo
    if plotar_circulo:
      theta = np.linspace(0, 2 * np.pi, 201)
      y = np.cos(theta)
      z = np.sin(theta)
      self.ax.plot(y,z,z, c='black')

    # plota as trajetorias
    for i in range(len(self.massas)):
      self.ax.set_xlim([-1,1])
      self.ax.set_ylim([-1,1])
      self.ax.set_zlim([-1,1])
      
      X, Y, Z = list(zip(*Ra[i]))
      self.ax.scatter(X[-1],Y[-1],Z[-1])

      if config.TAMANHO_RASTRO_ANIMACOES > 0:
        tamanho_rastro = min([config.TAMANHO_RASTRO_ANIMACOES, len(X)-1])      
        self.ax.plot(X[-tamanho_rastro:-1], Y[-tamanho_rastro:-1], Z[-tamanho_rastro:-1], c='black')

  def atualizar_coord (self, t):
    """
      Função auxiliar para visualizações 3d.
    """
    # separa as coordenadas
    Ra = list(zip(*self.Rs))
    # plota as trajetórias
    for i in range(len(self.massas)):
      
      self.ax.set_xlim(config.RANGE_PLOT_X)
      self.ax.set_ylim(config.RANGE_PLOT_Y)
      self.ax.set_zlim(config.RANGE_PLOT_Z)

      X, Y, Z = list(zip(*Ra[i]))

      if self.expandir:
        # Verifica se precisa aumentar o tamanho do plot
        if X[-1] < config.RANGE_PLOT_X[0] or X[-1] > config.RANGE_PLOT_X[1]:
          config.RANGE_PLOT_X = [2*x for x in config.RANGE_PLOT_X]
        if Y[-1] < config.RANGE_PLOT_Y[0] or Y[-1] > config.RANGE_PLOT_Y[1]:
          config.RANGE_PLOT_Y = [2*y for y in config.RANGE_PLOT_Y]
        if Z[-1] < config.RANGE_PLOT_Z[0] or Z[-1] > config.RANGE_PLOT_Z[1]:
          config.RANGE_PLOT_Z = [2*z for z in config.RANGE_PLOT_Z]

      self.ax.scatter(X[-1], Y[-1], Z[-1])

      if config.TAMANHO_RASTRO_ANIMACOES > 0:
        tamanho_rastro = min([config.TAMANHO_RASTRO_ANIMACOES, len(X)-1])      
        self.ax.plot(X[-tamanho_rastro:-1], Y[-tamanho_rastro:-1], Z[-tamanho_rastro:-1], c='black')

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
    self.fig = plt.figure(figsize=(12,6), dpi=config.ANIMACAO_DPI)
    self.ax = self.fig.add_subplot(projection='3d')
    Rs = list(zip(*Rs))
    
    for i in range(self.quantidade_corpos):
      Ri = list(zip(*Rs[i]))
      self.ax.plot(Ri[0],Ri[1],Ri[2])
      self.ax.scatter(*Rs[i][0])

    self.ax.set_xlim3d(*config.RANGE_PLOT_X)
    self.ax.set_ylim3d(*config.RANGE_PLOT_Y)
    plt.show()
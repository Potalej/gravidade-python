import matplotlib.animation as animation
import matplotlib.pyplot as plt
from numpy import arange

from simulacao.simular import Simulacao
from auxiliares.auxiliares import centro_massas
from auxiliares.hamiltoniano import H, U
from time import time

class Simulacao3D (Simulacao):

  def __init__ (self, massas:list, R0: list, P0: list, h:float=0.05, G:float=1):
    super().__init__(massas, R0, P0, h, G)
    self.exibir_centro_massas = False
    self.xlim = [-1000,1000]
    self.ylim = [-1000,1000]
    self.zlim = [-1000,1000]
  
  def funcao (self):
    for _ in range(self.qntdFrames):
      self.R, self.P, self.F = self.metodo.aplicarNVezes(self.R,self.P,n=self.n,E=self.E0)
      self.E = H(self.R,self.P,self.massas)
      self.V = U(self.R,self.massas)
      yield self.R, self.P, self.E

  def simular (self, qntdFrames:int=0, exibir:bool=True, salvar:bool=False)->str:
    """
      Faz uma simulação 3d usando as condições iniciais informadas.
    """
    self.qntdFrames = qntdFrames
    self.nomeArquivo = f"pontos_{time()}.txt"

    YK = []
    self.abrirArquivo(self.massas, self.nomeArquivo)
    for frame in self.funcao():
      R, P, E = frame

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


    
  def visualizar (self, R:list):
    """
      Para somente visualizar uma lista já em mãos.
    """
    self.funcao = lambda t: (R[t], 0, 0)
    self.fig = plt.figure(figsize=(12,6), dpi=100)
    self.ax = self.fig.gca(projection = '3d')
    ani = animation.FuncAnimation(self.fig, self.atualizar, arange(len(R)), interval=10,  repeat=False)
    plt.show()

  def atualizar (self, t):
    """
      Função auxiliar para visualizações 3d.
    """
    R, P, E = self.funcao(t)
    X, Y, Z = list(zip(*R))
    X, Y, Z = list(X), list(Y), list(Z)
    self.ax.clear()
    self.ax.set_xlim3d(*self.xlim)
    self.ax.set_ylim3d(*self.ylim)
    self.ax.set_zlim3d(*self.zlim)
    self.ax.scatter(X, Y, Z)
    if self.exibir_centro_massas:
      Rcm = centro_massas(self.massas, R)
      self.ax.scatter(Rcm[0], Rcm[1], Rcm[2], color="red")
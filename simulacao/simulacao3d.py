import matplotlib.animation as animation
import matplotlib.pyplot as plt
from numpy import arange
from moviepy.editor import *

from simulacao.simular import Simulacao
from auxiliares.auxiliares import centro_massas, momento_inercia_cm
from auxiliares.hamiltoniano import H, U, EC
from time import time
import os

from tabulate import tabulate

class Simulacao3D (Simulacao):

  def __init__ (self, massas:list, R0: list, P0: list, h:float=0.05, G:float=1):
    super().__init__(massas, R0, P0, h, G)
    self.G = G
    self.exibir_centro_massas = False
    self.xlim = [-1000,1000]
    self.ylim = [-1000,1000]
    self.zlim = [-1000,1000]
  
  def funcaoLimitada (self, t=0):
    for _ in range(self.qntdFrames):
      self.R, self.P, self.F, Es, Js = self.metodo.aplicarNVezes(self.R,self.P,n=self.n,E=self.E0,J0=self.J0)
      self.E = H(self.R,self.P,self.massas,self.G)
      self.V = U(self.R,self.massas,self.G)
      yield self.R, self.P, self.E
  
  def funcaoLimitada1 (self, t=0):
    for _ in range(self.qntdFrames):
      self.R, self.P, self.F, Es, Js, Ps = self.metodo.aplicarNVezes(self.R,self.P,n=self.n,E=self.E0,J0=self.J0,P0=self.P0_tot, rcm0_int=self.rcm_int)
      self.E = H(self.R,self.P,self.massas,self.G)
      self.V = U(self.R,self.massas,self.G)
      
      try: self.Es += Es
      except: self.Es = Es

      try: 
        self.Js += Js
        self.JsPasso += [Js[-1]]
      except: 
        self.Js = Js
        self.JsPasso  = [Js[-1]]

      try: 
        self.Ps[0] += Ps[0]
        self.Ps[1] += Ps[1]
        self.Ps[2] += Ps[2]
      except: 
        self.Ps = [[],[],[]]
        self.Ps[0] = Ps[0]
        self.Ps[1] = Ps[1]
        self.Ps[2] = Ps[2]

      yield self.R, self.P, self.E
  
  def funcao (self, t=0):
    self.R, self.P, self.F, Es, Js, Ps = self.metodo.aplicarNVezes(self.R,self.P,n=self.n,E=self.E0,J0=self.J0,P0=self.P0_tot, rcm0_int=self.rcm_int)
    self.E = H(self.R,self.P,self.massas,self.G)
    self.V = U(self.R,self.massas,self.G)
    return self.R, self.P, self.E

  def simular (self, qntdFrames:int=0, exibir:bool=True, salvar:bool=False)->str:
    """
      Faz uma simulação 3d usando as condições iniciais informadas.
    """
    self.qntdFrames = qntdFrames

    if salvar:
      self.nomeArquivo = f"pontos_{time()}.txt"
      YK = []
      self.abrirArquivo(self.massas, self.nomeArquivo)
      for frame in self.funcaoLimitada():
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

    elif exibir:
      self.fig = plt.figure(figsize=(12,6), dpi=100)
      self.ax = self.fig.gca(projection = '3d')
      ani = animation.FuncAnimation(self.fig, self.atualizar, arange(self.qntdFrames), interval=10,  repeat=False)
      plt.show()

    else:
      Rs, Ps, Pa = [], [], []
      Pas = []
      t0 = time()
      for frame in self.funcaoLimitada1():
        R, P, E = frame
        Rs.append(R)
        Pa = list(zip(*P))
        Pas.append(P)
        Ps.append([sum(Pa[0]), sum(Pa[1]), sum(Pa[2])])

      print('TEMPO:', time() - t0)
      print('Rs[-1]: ', Rs[-1])
      print()
      print('Pa: ', Pa)
      print()

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
      Ps = list(zip(*Ps))
      Ps[0] = [self.P0_tot[0]] + list(Ps[0])
      Ps[1] = [self.P0_tot[1]] + list(Ps[1])
      Ps[2] = [self.P0_tot[2]] + list(Ps[2])
      
      Px_info = ["Px", self.P0_tot[0], min(Ps[0]), max(Ps[0]), sum(Ps[0])/len(Ps[0])]
      Py_info = ["Py", self.P0_tot[1], min(Ps[1]), max(Ps[1]), sum(Ps[1])/len(Ps[1])]
      Pz_info = ["Pz", self.P0_tot[2], min(Ps[2]), max(Ps[2]), sum(Ps[2])/len(Ps[2])]

      # centro de massas
      def centrom(m, Rs):
        mtot = sum(m)
        Rcm = [[
          r[0]*m[a],
          r[1]*m[a],
          r[2]*m[a]
        ] for a,r in enumerate(Rs)]
        return [sum(a)/mtot for a in list(zip(*Rcm))] 

      Rcms = list(zip(*[centrom(self.massas, Rsa) for Rsa in Rs]))
      Rcmx = ["Rcmx"] + list(Rcms[0])
      Rcmy = ["Rcmy"] + list(Rcms[1])
      Rcmz = ["Rcmz"] + list(Rcms[2])

      tabela = [E_info, Jx_info, Jy_info, Jz_info, Px_info, Py_info, Pz_info, Rcmx, Rcmy, Rcmz]
      tabela = tabulate(tabela, headers=["Integral", "Inicial", "Min", "Max", "Média"])
      print()
      print(tabela)
      print()

      ###########################
      # desigualdade de sundman #
      ###########################
      
      # quadrado da norma do momento angular
      # indice_maximo = 0
      # norma2_J = []
      # for i, J in enumerate(self.JsPasso):
      #   c2 = sum(ji**2 for ji in J)
      #   if i > 0:
      #     if c2 >= max(norma2_J):
      #       indice_maximo = i
      #   norma2_J.append(c2)

      # # 2 I T
      # limitante_J = [
      #   2 * momento_inercia_cm(self.massas, Rs[i]) * EC(Pas[i], self.massas) for i in range(len(Rs))
      # ]

      # foi_falso = 0
      # for i in range(len(norma2_J)):
      #   if norma2_J[i] > limitante_J[i]:
      #     foi_falso += 1

      # print()
      # print('DESIGUALDADE DE SUNDMAN: ||J||2 <= 2IT ?')
      # print('Maximo: ', norma2_J[indice_maximo], limitante_J[indice_maximo])
      # print('Foi falso', foi_falso, 'vezes')
      # print()

      # ##########################
      # #  separacoes max e min  #
      # ##########################
      
      # # energia potencial
      # lista_U = [U(R, self.massas, self.G) for R in Rs]

      # dist = lambda x, y: sum((x[i]-y[i])**2 for i in range(len(x)))**.5

      # distancias_minimas = []
      # for R in Rs:
      #   distancias = []
      #   for a in range(len(R)):
      #     Ra = R[a]
      #     for b in range(len(R)):
      #       if a == b: continue
      #       Rb = R[b]
      #       distancias.append(dist(Ra, Rb))
  
      #   distancias_minimas.append(min(distancias))
      
      # m0 = min(self.massas)
      # m1 = max(self.massas)
      # sucessos = 0
      # for i in range(len(lista_U)):
      #   lado_esquerdo = - self.G*m1*m1/(2*distancias_minimas[i])
      #   lado_direito = - self.G*m0*m0/distancias_minimas[i]
      #   if lado_esquerdo <= lista_U[i] and lista_U[i] <= lado_direito:
      #     print(f'SUCESSO: r = {distancias_minimas[i]} e H = {H(Rs[i], Pas[i], self.massas, self.G)} \t {lado_esquerdo} < {lista_U[i]} < {lado_direito}')
      #     sucessos += 1
      #   else:
      #     print(f'Falhou: r = {distancias_minimas[i]} e H = {H(Rs[i], Pas[i], self.massas, self.G)} \t {lado_esquerdo} < {lista_U[i]} < {lado_direito}')

      # print(f'\nTivemos {100*sucessos/len(lista_U)}% de sucesso.')


      ###########################
      #         graficos        #
      ###########################

      fig, ax = plt.subplots(1, 4, figsize=(16,8))

      ax[0].plot(Es, label="H")
      ax[0].set_ylabel("H")
      ax[0].legend()
      
      ax[1].plot(Js[0], label="Jx")
      ax[1].plot(Js[1], label="Jy")
      ax[1].plot(Js[2], label="Jz")
      ax[1].legend()

      ax[2].plot(Ps[0], label="Px")
      ax[2].plot(Ps[1], label="Py")
      ax[2].plot(Ps[2], label="Pz")
      ax[2].legend()

      ax[3].plot(Rcms[0], label="Rcmx")
      ax[3].plot(Rcms[0], label="Rcmy")
      ax[3].plot(Rcms[0], label="Rcmz")
      ax[3].legend()
      
      plt.show()
      


      self.fig = plt.figure(figsize=(12,6), dpi=100)
      self.ax = self.fig.gca(projection='3d')
      Rs = list(zip(*Rs))
      for i in range(self.quantidade_corpos):
        Ri = list(zip(*Rs[i]))
        self.ax.plot(Ri[0],Ri[1],Ri[2])
        self.ax.scatter(*Rs[i][0])
      self.ax.set_xlim3d(*[-1000, 1000])
      self.ax.set_ylim3d(*[-1000, 1000])
      # self.ax.set_zlim3d(*[0, 5000])
      plt.show()
    
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
      self.ax = self.fig.gca(projection = '3d')
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
    R, P, E = self.funcao(t)
    try: self.Rs.append(R)
    except: self.Rs = [R]
    # X, Y, Z = list(zip(*R))
    Ra = list(zip(*self.Rs))
    # X, Y, Z = list(X), list(Y), list(Z)
    self.ax.clear()
    # self.ax.set_xlim3d(*self.xlim)
    # self.ax.set_ylim3d(*self.ylim)
    # self.ax.set_zlim3d(*self.zlim)
    for i in range(len(R)):
      X, Y, Z = list(zip(*Ra[i]))
      self.ax.plot(X, Y, Z, c="black") # era 3
    # self.ax.scatter(X, Y, Z, s=10, c="black") # era 3
    if self.exibir_centro_massas:
      Rcm = centro_massas(self.massas, R)
      self.ax.scatter(Rcm[0], Rcm[1], Rcm[2], color="red")
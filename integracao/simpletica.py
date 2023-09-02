"""
  Integrador simpletico de Verlet
"""

from auxiliares.auxiliares import distancia
from auxiliares.colisao import colisao
from auxiliares.correcao import correcao

class Verlet:

  def __init__ (self, massas:list, G:float, h:float=0.05, dimensao:int=3, corrigir:bool=True, colidir:bool=True):

    # Dimensao
    self.dimensao = dimensao

    # Quantidade de particulas
    self.qntd = len(massas)

    # Passo de integracao
    self.h = h

    # Constante de gravitacao universal
    self.G = G

    # Monta os vetores de massas
    self.massas = massas

    # Configuracoes
    self.corrigir = corrigir
    self.colidir = colidir

  def forcas (self, R):
    Fsomas = [[0,0,0] for i in range(self.qntd)]
    for a in range(self.qntd):
      ma = self.massas[a]
      ra = R[a]
      for b in range(a):
        if a != b:
          mb = self.massas[b]
          rb = R[b]
          rab = distancia(rb, ra)
          for i in range(self.dimensao):
            Fabi = self.G * ma * mb * (rb[i] - ra[i])/(rab**3)
            Fsomas[a][i] += Fabi
            Fsomas[b][i] -= Fabi
    return Fsomas


  def integrar (self, R0, P0):
    # Gera matriz de forcas
    Fsomas = self.forcas(R0)

    # Velocity Verlet
    R, P = [],[]

    for a in range(self.qntd):
      R.append([])
      
      for i in range(self.dimensao):
        # Calcula x (t+h) = x(t) + p(t) h/m + 0.5 h² Fa(t)/m
        ra = R0[a][i] + self.h*P0[a][i]/self.massas[a] + 0.5 * (self.h**2) * Fsomas[a][i]/self.massas[a]
        R[-1].append(ra)

    # Calcula as novas forcas
    Fsomas_apos = self.forcas(R)
    for a in range(self.qntd):
      P.append([])  
      for i in range(self.dimensao):
        # Calcula p(t+h)=p(t)+0.5*h (Fa(t) + Fa(t+h))
        pa = P0[a][i] + 0.5 * self.h * (Fsomas[a][i] + Fsomas_apos[a][i])
        P[-1].append(pa)
    
    return R, P

  def aplicarNVezes (self, R0, P0, n=1):
    posicoes = []
    momentos_lineares = []
    R, P = R0, P0
    for _ in range(n):
      # integra
      R, P = self.integrar(R, P)

      if self.corrigir:
        R, P, corrigiu = correcao(self.massas, R, P, self.G)
      
      if self.colidir:
        P = colisao(self.massas, R, P)
      
      # Salva as posicoes e os momentos lineares
      posicoes.append(R)
      momentos_lineares.append(P)
    return R, P, posicoes, momentos_lineares
  
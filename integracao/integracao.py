"""
  Integração numérica via Runge-Kutta de 4ª ordem (RK4)

  A integração é feita matricialmente e adaptada especialmente
  para o sistema de N-corpos.
"""
from numpy import array, transpose, identity, ones, einsum, true_divide, zeros
from auxiliares.hamiltoniano import *
from time import time

class RK4:

  """
    Integração numérica via Runge-Kutta de 4ª ordem (RK4)

    A integração é feita matricialmente e adaptada especialmente
    para o sistema de N-corpos.

    Parâmetros
    ----------
    massas : list
      Lista de massas das partículas.
    h : float = 0.05
      Tamanho do passo de integração.
    G : float = 1
      Constante de gravitação universal.
    dim : int = 1
      Dimensão dos problemas.
  """

  def __init__ (self, massas:list, h:float=0.05, G:float=1, dimensao:int=3):

    # dimensão
    self.dimensao = dimensao

    # quantidade de partículas
    self.qntd = len(massas)

    # passo de integração
    self.h = h

    # constante de gravitação universal
    self.G = G

    # monta os vetores de massas
    self.guardar_massas(massas)

    self.vetorUm = ones((self.qntd, self.qntd))
    self.identidade = identity(self.qntd)

  def guardar_massas (self, massas:list)->None:
    """
      Guarda a lista de massas informada nas formas de matriz 
      e vetor de massas inversas.

      Parâmetros
      ----------
      massas : list
        Lista de massas das partículas.
    """
    # vetor de massas
    self.massas = array(massas)

    # vetor de massas invertidas
    self.massasDuplicadasInvertidas = array([
      [1/mi for i in range(self.dimensao)] 
      for mi in massas
    ])

    # matriz de produto de massas (facilita o cálculo das forças)
    MA = array([
      [0 if j == i else self.massas[j] for j in range(self.qntd)]
      for i in range(self.qntd)
    ])
    self.prodM = MA * transpose(MA)

  def forcas (self, R)->tuple:
    """
      Monta a matriz de forças entre cada partícula e a matriz 
      de soma das forças para cada partícula.

      Parâmetros
      ----------
      R : np.array
        Vetor de posições das partículas.
    """
    # coordenadas
    X = [[Ri] for Ri in R]
    
    # matriz X cheia
    X = einsum('ij,ijk->ijk', self.vetorUm, X)
    # diferença rb - ra
    difX = X.transpose(1,0,2) - X
    # norma
    norma = einsum('ijk,ijk->ij', difX, difX)**(3/2) + self.identidade
    # matriz de forças
    F = true_divide(self.prodM, norma)
    F = -self.G*einsum('ij,ijk->ijk', F, difX)
    
    # matriz de soma das forças
    FSomas = sum(F)
    return F, FSomas

  def runge_kutta4 (self, R, P, FSomas):
    """
      Método RK4 adaptado para os sistemas em questão.
    """
    # faz a integração sobre as equações x'
    k1_vet = P*self.massasDuplicadasInvertidas
    k1_1m = k1_vet*self.massasDuplicadasInvertidas
    k1_2m = k1_1m*self.massasDuplicadasInvertidas
    k1_3m = k1_2m*self.massasDuplicadasInvertidas

    fator = (self.h/6) * (6*k1_vet + 3*self.h*k1_1m + self.h**2 * k1_2m + 0.25*self.h**3 * k1_3m)
    novas_posicoes = R + fator

    # integração sobre as equações p'
    novos_momentos = P + self.h*FSomas

    return novas_posicoes, novos_momentos

  def aplicarNVezes (self, R, P, n=1, E=0, J0=[0,0,0], P0=[0,0,0], rcm0_int=[0,0,0]):
    Es = []
    Js = []
    Ps = [[],[],[]]
    for _ in range(n):
      # forças no instante atual
      F, FSomas = self.forcas(R)
      
      # integração numérica
      R, P = self.runge_kutta4(R,P,FSomas)
      
      # R, P, e = ajustarH(R, P, self.massas, E, FSomas, R0, P0)
      # F, FSomas = self.forcas(R)
      # R, P, e = ajustarH(R, P, self.massas, E, FSomas)
      R, P = ajusteJ(R, P, J0)
      P = ajustePTotal(P, P0)
      R = ajusteCentroMassas(self.massas, R, rcm0_int)
      # ajuste da energia

      # R, P = juntos(R, P, self.massas, E, FSomas, J0)

      # PARECE QUE CORRIGIR A ENERGIA PRIMEIRO E DEPOIS O MOMENTO ANGULAR DÁ MELHOR PRO MOMENTO ANGULAR. VER ISSO!

      # níveis de energia e momento angular atuais
      e = H(R, P, self.massas)
      J = momentoAngular(R,P)
      
      p = [sum(p[0] for p in P),sum(p[1] for p in P),sum(p[2] for p in P)]
      Ps[0].append(p[0])
      Ps[1].append(p[1])
      Ps[2].append(p[2])
      Es.append(e)
      Js.append(J)
    return R, P, F, Es, Js, Ps
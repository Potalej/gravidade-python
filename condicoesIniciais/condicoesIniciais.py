"""
    Classe especial de geração de condições iniciais.
"""

import random

class condicoesIniciais:
  """
      Classe básica para gerar condições iniciais.
      Contém funções voltadas para a geração aleatória de 
      posições, velocidades e momentos dados os limites e
      os intervalos de passo.
  """

  def __init__ (self, massas:list=[], dimensao=3):
    self.adicionar_massas(massas)
    self.dimensao = dimensao
    # par (1) ou ímpar (0)
    self.qntd_tipo = 1 if self.qntdCorpos % 2 == 0 else 0

  def gerar_posicoes (self, qntd:int, int_x:list, int_y:list, int_z:list=[], dist_min_x:float=10, dist_min_y:float=10, dist_min_z:float=0):
    """
      Gerar uma lista de pares de coordenadas de posiçao.
    """
    if len(int_z) == 0:
      self.r = [
        random.sample(range(int_x[0], int_x[1], dist_min_x), qntd),
        random.sample(range(int_y[0], int_y[1], dist_min_y), qntd)
      ]
    else:
      self.r = [
        random.sample(range(int_x[0], int_x[1], dist_min_x), qntd),
        random.sample(range(int_y[0], int_y[1], dist_min_y), qntd),
        random.sample(range(int_z[0], int_z[1], dist_min_z), qntd)
      ]

    self.r = list(zip(*self.r))
    return self.r

  def gerar_momentos (self, qntd:int, int_x:list, int_y:list, int_z:list=[], int_min_x:float=.1, int_min_y:float=.1, int_min_z:float=0):
    """
      Gerar uma lista de pares de coordenadas de momento.
    """
    if len(int_z) == 0:
      self.p = [
        [random.randrange(int_x[0], int_x[1], int_min_x),random.randrange(int_y[0], int_y[1], int_min_y)] for i in range(qntd)
      ]
    else:
      self.p = [
        [random.randrange(int_x[0], int_x[1], int_min_x),random.randrange(int_y[0], int_y[1], int_min_y),random.randrange(int_z[0], int_z[1], int_min_z)] 
        for i in range(qntd)
      ]

    return self.p

  def gerar_velocidades (self, qntd:int, int_x:list, int_y:list, int_z:list=[], int_min_x:float=.1, int_min_y:float=.1, int_min_z:float=0):
    """
      Gerar uma lista de pares de coordenadas de velocidade.
    """
    if len(int_z) == 0:
      self.v = [
        [random.randrange(int_x[0], int_x[1], int_min_x),random.randrange(int_y[0], int_y[1], int_min_y)] for i in range(qntd)
      ]
    else:
      self.v = [
        [random.randrange(int_x[0], int_x[1], int_min_x),random.randrange(int_y[0], int_y[1], int_min_y),random.randrange(int_z[0], int_z[1], int_min_z)] 
        for i in range(qntd)
      ]

    return self.v

  def juntar_ps (self, v=True):
    """
      Junta os pontos em uma lista intercalando coordenada 
      de posição com cada respectiva coordenada de momento.

      Se estiver utilizando a velocidade em cálculos anteriores,
      passar `v=True` para criar o vetor de momentos.
    """
    if v:
      if len(self.v[0]) == 2:
        self.p = [[
          self.v[i][0]*self.massas[i], self.v[i][1]*self.massas[i]
        ] for i in range(self.qntdCorpos)]
      else:
        self.p = [[
          self.v[i][0]*self.massas[i], self.v[i][1]*self.massas[i],self.v[i][2]*self.massas[i]
        ] for i in range(self.qntdCorpos)]

    self.ps = []
    if len(self.r[0]) == 2:
      for i in range(self.qntdCorpos):
          self.ps += [self.r[i][0], self.p[i][0], self.r[i][1], self.p[i][1]]
    else:
      for i in range(self.qntdCorpos):
        self.ps += [self.r[i][0], self.p[i][0], 
        self.r[i][1], self.p[i][1],
        self.r[i][2], self.p[i][2]]

    return self.ps

  def gerar_massas (self, m_min: float, m_max:float, qntd:float, inteiras:bool=True):
    """
        Gera massas aleatórias num intervalo dado.
    """
    if inteiras: self.massas = [random.randint(m_min, m_max) for i in range(qntd)]
    else: self.massas = [random.randrange(m_min, m_max) for i in range(qntd)]
    self.adicionar_massas(self.massas)
    return self.massas

  def adicionar_massas (self, m:list):
    """
        Adiciona as massas passadas às propriedades
        da classe:
        
        `massas`: lista de massas.
        
        `qntdCorpos`: quantidade de corpos no sistema.

        `mtot`: soma total das massas.
    """
    self.massas = m
    self.qntdCorpos = len(self.massas)
    self.mtot = sum(self.massas)
import random

class condicoesIniciais:
  """
    Classe básica para gerar condições iniciais.
    Contém funções voltadas para a geração aleatória de 
    posições, velocidades e momentos dados os limites e
    os intervalos de passo.
  """
  def __init__ (self, N:int=2, dimensao:int=3):
    self.N = N
    self.dimensao = dimensao
  
  def gerar_massas (self, configs_massas:dict)->list:
    """Gera massas aleatórias num intervalo dado."""
    m_min, m_max = configs_massas['min'], configs_massas['max']
    if configs_massas['inteiras']:
      self.massas = [random.randint(m_min, m_max) for i in range(self.N)]
    else:
      self.massas = [random.randrange(m_min, m_max) for i in range(self.N)]
    self.mtot = sum(self.massas)
    return self.massas

  def gerar_valores(self, configs_valores:dict, repete:bool=True)->list:
    """Gerar uma lista"""
    int_x = configs_valores['x']['intervalo']
    int_y = configs_valores['y']['intervalo']

    # gera para as duas primeiras coordenadas
    if self.dimensao == 2:
      if repete:
        vals = [[
          random.randrange(*int_x, configs_valores['x']['dist_min']),
          random.randrange(*int_y, configs_valores['y']['dist_min'])
        ] for a in range(self.N)]
      else:
        vals = [
          random.sample(range(*int_x, configs_valores['x']['dist_min']), self.N),
          random.sample(range(*int_y, configs_valores['y']['dist_min']), self.N)
        ]
        vals = list(zip(*vals))

    # se for no R3, precisa adicionar mais uma dimensão
    if self.dimensao == 3:
      int_z = configs_valores['z']['intervalo']
      if repete:
        vals = [[
          random.randrange(*int_x, configs_valores['x']['dist_min']),
          random.randrange(*int_y, configs_valores['y']['dist_min']),
          random.randrange(*int_z, configs_valores['z']['dist_min']),
        ] for a in range(self.N)]
      else:
        vals = [
          random.sample(range(*int_x, configs_valores['x']['dist_min']), self.N),
          random.sample(range(*int_y, configs_valores['y']['dist_min']), self.N),
          random.sample(range(*int_z, configs_valores['z']['dist_min']), self.N)
        ]
        vals = list(zip(*vals))

    return vals
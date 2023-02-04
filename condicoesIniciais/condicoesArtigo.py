import random
from numpy import matrix
from numpy.linalg import solve
from auxiliares.auxiliares import centro_massas, momento_linear_total_velocidade, momentos_angulares, momento_inercia_cm, tensor_inercia_geral, prodvetR3
from auxiliares.hamiltoniano import EC, U, H

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



class condicoesArtigo (condicoesIniciais):
  
  def __init__ (self, configs:dict):
    """
      Gera as coordenadas básicas.
    """
    # quantidade de corpos
    self.N = configs['qntdCorpos']
    super().__init__(self.N, configs['dimensao'])

    # gera o básico
    self.basico(configs)

    # aplicando as condições sobre os valores gerados
    self.condicionar()
    

  def basico (self, configs:dict)->None:
    """
      Gera os valores básicos.
    """
    # gerando as massas
    self.gerar_massas(configs['massas'])

    # gerando as posições
    self.r = self.gerar_valores(configs['posicoes'], repete=False)

    # gerando as velocidades
    self.v = self.gerar_valores(configs['velocidades'], repete=True)

  
  def condicionar (self)->None:
    """
      Aplica as condições sobre os valores já gerados.
    """
    self.rcm = centro_massas(self.massas, self.r)

    # 1) zerar rcm
    self.zerar_centro_massas()

    # 2) zerar vcm = r'cm
    self.zerar_velocidade_centro_massas()

    # 3) zerar o momento angular
    self.zerar_momento_angular()

    # 2) zerar o centro de massas novamente
    self.zerar_centro_massas()

    # 2) zerar vcm = r'cm
    self.zerar_velocidade_centro_massas()
    
    # 4) zerar a energia total
    self.zerar_energia_total()

    self.rcm = centro_massas(self.massas, self.r)
    self.P = momento_linear_total_velocidade(self.massas, self.v)
    # calcula todos os momentos angulares
    Ja = momentos_angulares(self.massas, self.r, self.v)
    # momento angular total
    self.J = [ sum(Jax[i] for Jax in Ja) for i in range(3) ]

    print('centro de massas: ', self.rcm)
    print('momento linear total: ', self.P)
    print('momento angular total: ', self.J)
    print('energia total: ', H(self.r, self.p, self.massas))


  def zerar_centro_massas (self)->None:
    """
      Posiciona o centro de massas na origem.
    """
    # arruma as posições
    self.r = [
      [ self.r[a][i] - self.rcm[i] for i in range(self.dimensao) ]
      for a in range(self.N)
    ]  
    # define o novo centro de massas
    self.rcm = centro_massas(self.massas, self.r)

  
  def zerar_velocidade_centro_massas (self)->None:
    """
      Zera a velocidade do centro de massas, i. é, 
      do momento linear total.
    """
    # calcula o momento
    self.P = momento_linear_total_velocidade(self.massas, self.v)
    # arruma as velocidades
    self.v = [
      [ self.v[a][i] - self.P[i]/self.mtot for i in range(self.dimensao) ]
      for a in range(self.N)
    ]
    self.p = [
      [ self.v[a][i]*self.massas[a] for i in range(self.dimensao) ]
      for a in range(self.N)
    ]
    # define os novos momentos
    self.P = momento_linear_total_velocidade(self.massas, self.v)

  
  def zerar_momento_angular (self)->None:
    """
      Zera o momento angular do sistema.
    """
    # calcula todos os momentos angulares
    Ja = momentos_angulares(self.massas, self.r, self.v)
    # momento angular total
    J = [ sum(Jax[i] for Jax in Ja) for i in range(3) ]
    # momento de inércia
    self.Icm = momento_inercia_cm(self.massas, self.r)

    # se for em 3 dimensões
    if self.dimensao == 3:
      # tensor de inércia
      I = tensor_inercia_geral(self.massas, self.r)
      # vetor de rotação
      omega = - solve(I, J)
      # percorre os corpos
      for a in range(self.N):
        # produto vetorial de ra por omega
        ra_omega = list(prodvetR3(self.r[a], omega))
        
        self.v[a] = [
          self.v[a][i] + ra_omega[i]
          for i in range(self.dimensao)
        ]
      
      self.p[a] = [
        self.massas[a] * self.v[a][i] for i in range(self.dimensao)
      ]
      # calcula o novo momento angular total
      self.J = matrix(J) + (matrix(I) * matrix(omega).T).T

  def zerar_energia_total (self)->None:
    """
      Zera a energia total.
    """
    # calcula a energia cinética atual
    energia_cinetica = EC(self.p, self.massas)
    # calcula a energia potencial atual
    energia_potencial = U(self.r, self.massas)

    # fator de razão
    fator = (-energia_potencial/energia_cinetica)**.5

    for a in range(self.N):
      for i in range(self.dimensao):
        self.p[a][i] *= fator
        self.v[a][i] = self.p[a][i]/self.massas[a]
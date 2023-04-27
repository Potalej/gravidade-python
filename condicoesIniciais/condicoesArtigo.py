from numpy import matrix
from numpy.linalg import solve
from auxiliares.auxiliares import centro_massas, momento_linear_total_velocidade, momentos_angulares, momentoAngular, momento_inercia_cm, tensor_inercia_geral, prodvetR3
from auxiliares.hamiltoniano import EC, U, H
from condicoesIniciais.condicoesIniciais import condicoesIniciais

class condicoesArtigo (condicoesIniciais):
  
  def __init__ (self, configs:dict={}, valoresIniciais:dict={}):
    """
      Gera as coordenadas básicas.
    """
    # se quiser gerar
    if bool(configs):
    # quantidade de corpos
      self.N = configs['qntdCorpos']
      super().__init__(self.N, configs['dimensao'])

      # gera o básico
      self.basico(configs)

    elif bool(valoresIniciais):
      self.N = valoresIniciais["qntdCorpos"]
      super().__init__(self.N, valoresIniciais['dimensao'])
      self.G = valoresIniciais['G']
      self.massas = valoresIniciais['massas']
      self.mtot = sum(self.massas)
      self.r = valoresIniciais['posicoes']
      self.v = [
        [p/self.massas[i] for p in valoresIniciais['momentos'][i]]
        for i in range(self.N)]
      
    else:
      raise ValueError("Nenhum valor informado!")

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
    self.J = momentoAngular(self.r, self.p)

    print('centro de massas: ', self.rcm)
    print('momento linear total: ', self.P)
    print('momento angular total: ', self.J)
    print('energia total: ', H(self.r, self.p, self.massas, self.G))


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
    energia_potencial = U(self.r, self.massas, self.G)

    # fator de razão
    fator = (-energia_potencial/energia_cinetica)**.5

    for a in range(self.N):
      for i in range(self.dimensao):
        self.p[a][i] *= fator
        self.v[a][i] = self.p[a][i]/self.massas[a]
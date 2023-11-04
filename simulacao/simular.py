import config.configs as config
from auxiliares.auxiliares import momento_inercia_cm, centro_massas, momentoAngular
from auxiliares.hamiltoniano import H, U
from auxiliares.shapedynamics import complexidade
from integracao.rk4 import RK4
from integracao.simpletica import Verlet

from time import time
from numpy import true_divide

class Simulacao:
  """
    Para fazer simulacoes no geral.

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
  """
  QUANTIDADE_ANTES_SALVAR = config.SIMULACAO_QNTD_SALVAR
  INTEGRADORES = {
    'rk4': RK4,
    'verlet': Verlet
  }

  def __init__ (
      self, 
      massas     : list, 
      R0         : list, 
      P0         : list, 
      h          : float = 0.05, 
      G          : float = 1,
      integrador : str   = 'rk4',
      corrigir   : bool  = False,
      colidir    : bool  = False
    ):
    # Guarda as informacoes basicas
    self.massas = massas
    self.quantidade_corpos = len(self.massas)
    self.dimensao = len(R0[0])
    self.mtot = sum(self.massas)

    self.R, self.P = R0, P0
    self.G = G

    # Captura o metodo escolhido
    try:
      metodo_integracao = self.INTEGRADORES[integrador.lower()]
    except:
      raise ValueError('O integrador informado eh desconhecido.')
    # Inicializa o metodo
    self.h = h
    self.metodo = metodo_integracao(massas=self.massas, h=self.h, G=G, dimensao=self.dimensao, corrigir=corrigir, colidir=colidir)

    # energia inicial
    self.E0 = H(self.R, self.P, self.massas, self.G)
    self.E = self.E0

    # momento angular inicial
    self.J0 = momentoAngular(R0, P0)

    # momento linear total inicial
    self.P0_tot = [sum(x) for x in list(zip(*P0))]

    # quantidade de integrações por passo
    self.n = config.SIMULACAO_QNTD_INTEGRACOES_PASSO

    # centro de massas inicial (sem o total de massas)
    self.rcm_int = [
      sum(self.massas[a]*self.R[a][0] for a in range(self.quantidade_corpos)),
      sum(self.massas[a]*self.R[a][1] for a in range(self.quantidade_corpos)),
      sum(self.massas[a]*self.R[a][2] for a in range(self.quantidade_corpos))
    ]

  def salvarPontos (self, pontos:list, nome='pontos.txt'):
    coords = [[str(ponto) for ponto in lista] for lista in pontos]
    coords = '\n'.join([','.join(ponto) for ponto in coords])
    with open('pontos/' + nome, 'a') as arq:
      arq.write('\n' + coords)

  def abrirArquivo (self, massas:list, nome='pontos.txt'):
    with open('pontos/' + nome, 'w') as arq:
      m = ','.join(str(m) for m in massas)
      arq.write(m + config.SEPARADOR_ARQUIVOS)

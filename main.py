from condicoesIniciais.exemplos import CondicoesIniciaisExemplos
from condicoesIniciais.condicoesArtigo import condicoesArtigo
from simulacao.ler import ler_arquivo
from simulacao.simulacao3d import Simulacao3D
from outros.ajudador import informacoes_basicas


##################################################################
# 1º CASO: EXEMPLO PRE-DEFINIDO
##################################################################
# Roda um exemplo de lemniscata
# massas, posicoes, momentos, G = CondicoesIniciaisExemplos().gerar('lemniscata')
# S = Simulacao3D(massas, posicoes, momentos, G=G, h=0.001, integrador='verlet')
# S.simular(500, visualizacao='2d')

##################################################################
# 2º CASO: FORNECE VALORES E VISUALIZA 
##################################################################
# m = [100, 100, 80]
# R0 = [[100, 100, 100],[-100, -100, 0], [-200, 200,0]]
# P0 = [[70, 0,0],[0, 30,10],[0,-5,-10]]
# S = Simulacao3D(m, R0, P0, G=3, h=0.05, integrador='verlet')
# S.simular(500, visualizacao='2d')

##################################################################
# 3º CASO: GERA VALORES ALEATORIOS CONDICIONADOS
##################################################################
configs = {
  'dimensao': 3,
  'G': 5,
  'qntdCorpos': 10, # qntd de corpos
  'massas': {
    'min': 100,
    'max': 300,
    'inteiras': True
  },
  'posicoes': {
    'x': {
      'intervalo': [-800, 800],
      'dist_min': 50
    },
    'y': {
      'intervalo': [-800, 800],
      'dist_min': 50
    },
    'z': {
      'intervalo': [-800, 800],
      'dist_min': 50
    }
  },
  'velocidades': {
    'x': {
      'intervalo': [-1,1],
      'dist_min': 1
    },
    'y': {
      'intervalo': [-1,1],
      'dist_min': 1
    },
    'z': {
      'intervalo': [-1,1],
      'dist_min': 1
    }
  }
}
condicoes = condicoesArtigo(configs, energia=-20.0)
S = Simulacao3D(
  massas=condicoes.massas,
  R0 = condicoes.r,
  P0 = condicoes.p,
  h = 0.05,
  G = configs['G'],
  integrador = 'verlet',
  corrigir = False,
  colidir = False,
)
S.simular(300, visualizacao='', salvar=False, expandir=False)
informacoes_basicas(
  m                 = condicoes.massas, 
  Rs                = S.Rs, 
  Ps                = S.Ps, 
  G                 = configs['G'],
  energia           = [0,0],
  angular           = [0,1],
  linear            = [],
  centro_de_massas  = [],
  dilatacao         = [1,0],
  inercia           = [],
  complexidade      = [1,1],
  formato           = [2,2]
)
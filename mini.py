from simulacao.simulacao3d import Simulacao3D
from condicoesIniciais.condicoesArtigo import condicoesArtigo

### EXEMPLO GERAL COM E=0, P=0, J=0 E RCM=0 CONFORME O ARTIGO
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
      'intervalo': [-1300, 1300],
      'dist_min': 50
    },
    'y': {
      'intervalo': [-1300, 1300],
      'dist_min': 50
    },
    'z': {
      'intervalo': [-1300, 1300],
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

condicoes = condicoesArtigo(configs)

S = Simulacao3D(
  massas=condicoes.massas,
  R0 = condicoes.r,
  P0 = condicoes.p,
  h = 0.01,
  G = configs['G'],
  integrador = 'verlet',
  corrigir = False,
  colidir = False,
  visualizar_2d = False
)
S.simular(3000, exibir=False, salvar=True)

from ajudador import informacoes_basicas

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
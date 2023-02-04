from simulacao.simulacao3d import Simulacao3D
from condicoesIniciais.condicoesArtigo import condicoesArtigo

### EXEMPLO GERAL COM E=0, P=0, J=0 E RCM=0 CONFORME O ARTIGO
configs = {
  'dimensao': 3,
  'qntdCorpos': 10, # qntd de corpos
  'massas': {
    'min': 100,
    'max': 100,
    'inteiras': True
  },
  'posicoes': {
    'x': {
      'intervalo': [-5000, 5000],
      'dist_min': 100
    },
    'y': {
      'intervalo': [-5000, 5000],
      'dist_min': 100
    },
    'z': {
      'intervalo': [-5000, 5000],
      'dist_min': 100
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
from auxiliares.hamiltoniano import H

S = Simulacao3D(condicoes.massas, condicoes.r, condicoes.p, G=150)
S.xlim = [-5000,5000]
S.ylim = [-5000,5000]
S.zlim = [-5000,5000]
S.simular(500, True, False)
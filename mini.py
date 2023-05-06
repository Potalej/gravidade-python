from simulacao.simulacao3d import Simulacao3D
from condicoesIniciais.condicoesArtigo import condicoesArtigo

### EXEMPLO GERAL COM E=0, P=0, J=0 E RCM=0 CONFORME O ARTIGO
configs = {
  'dimensao': 3,
  'G': 15,
  'qntdCorpos': 50, # qntd de corpos
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
from auxiliares.hamiltoniano import H

S = Simulacao3D(condicoes.massas, condicoes.r, condicoes.p, G=15)
S.simular(30000, False, True)
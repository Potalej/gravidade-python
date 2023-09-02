from condicoesIniciais.condicoesArtigo import condicoesArtigo


# Um bom exemplo de solucao cagada eh usar 4 corpos com Verlet e colisao ligada, sem correcao
# Forma um negocio esquisito que desestabiliza a energia e consequentemenete a evolucao do sistema

# EXEMPLO DE 4 CORPOS ABAIXO
massas = [100, 100, 100, 100]
posicoes = [
  [-10, -10, 0],
  [10, 10, 0], 
  [10, -10, 0], 
  [-10, 10, 0], 
]
momentos = [
  [50,30,0],
  [-30,90,0],
  [-10,10,-90],
  [-10,100,100],
]

# EXEMPLO DE 3 CORPOS ABAIXO
# massas = [10,11,12]

# posicoes = [
#   [-30, 0, 0],
#   [ 0, 0, 10],
#   [ 0, 0, 0]
# ]

# momentos = [
#   [1000, 1000, 0],
#   [-1000, -10, 0],
#   [0, 0, 0]
# ]

# posicoes = [
#   [-30, 0, 0],
#   [ 0, 30, 0],
#   [ 0, 0, 30]
# ]

# momentos = [
#   [1, 1, 0],
#   [1, 1, 0],
#   [0, 0, 0]
# ]

# massas = [100, 100]
# posicoes = [
#   [-5, -10, 1],
#   [10, 15, 2]
# ]
# momentos = [
#   [10, 1, 3],
#   [2, 5, 5]
# ]

# G = 0.3
G = 5

valoresIniciais = {
  'qntdCorpos': len(massas),
  'dimensao': len(posicoes[0]),
  'posicoes': posicoes,
  'momentos': momentos,
  'massas': massas,
  'G': G
}

C = condicoesArtigo(valoresIniciais=valoresIniciais)

from simulacao.simulacao3d import Simulacao3D

# S = Simulacao3D(
#   massas=massas, 
#   R0=C.r, 
#   P0=C.p, 
#   h=0.005, 
#   G=G, 
#   integrador = 'verlet',
#   corrigir = False,
#   colidir = False,
#   visualizar_2d = False
# )

# Lemniscata
R = [
  [-0.97000436, 0.24308753, 0],
  [0, 0, 0],
  [0.97000436, -0.24308753, 0]
]
P = [
  [ 0.4662036850, 0.4323657300, 0],
  [-0.93240737, -0.86473146, 0],
  [ 0.4662036850, 0.4323657300, 0]
]
massas = [1,1,1]
G = 1
S = Simulacao3D(
  massas=massas, 
  R0=R, 
  P0=P, 
  h=0.0005, 
  G=G, 
  integrador = 'verlet',
  corrigir = False,
  colidir = False,
  visualizar_2d = True
)

# S = Simulacao3D(massas=massas, R0=posicoes, P0=momentos, h=0.05, G=G)
from time import time
print()
t0 = time()
# print('CORREÇÃO MOMENTO ANGULAR')
S.simular(20000, exibir=True, salvar=False)
print()
print(S.R)
print('tempo: ', time() - t0)

# from ajudador import informacoes_basicas

# informacoes_basicas(
#   m                 = massas, 
#   Rs                = S.Rs, 
#   Ps                = S.Ps, 
#   G                 = G,
#   energia           = [0,0],
#   angular           = [0,1],
#   linear            = [],
#   centro_de_massas  = [],
#   dilatacao         = [1,0],
#   inercia           = [],
#   complexidade      = [1,1],
#   formato           = [2,2]
# )
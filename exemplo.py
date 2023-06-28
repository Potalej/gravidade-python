from condicoesIniciais.condicoesArtigo import condicoesArtigo

massas = [100, 100, 80]
posicoes = [
  [100, 100, 100],
  [-100, -100, 0], 
  [-200, 200,0]
]
momentos = [
  [-70, 0,0],
  [0, 30,10],
  [0,-5,-10]
]

G = 10

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

S = Simulacao3D(massas=massas, R0=C.r, P0=C.p, h=0.1, G=G)
from time import time
print()
t0 = time()
# print('CORREÇÃO MOMENTO ANGULAR')
S.simular(1500, exibir=True, salvar=False)
print()
print(S.R)
print('tempo: ', time() - t0)
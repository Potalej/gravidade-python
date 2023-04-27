from auxiliares.auxiliares import momentos_angulares, tensor_inercia_geral, prodvetR3, momentoAngular
from auxiliares.hamiltoniano import EC, U, H
from numpy import matrix
from numpy.linalg import solve
from condicoesIniciais.condicoesArtigo import condicoesArtigo

massas = [100, 100, 80]
posicoes = [
  [100, 100, 100],
  [-100, -100, 0], 
  [-200, 200,0]
]
momentos = [
  [70, 0,0],
  [0, 30,10],
  [0,-5,-10]
]

G = 3

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

S = Simulacao3D(massas, C.r, C.p, G=G)
# S.xlim = [-200,200]
# S.ylim = [-200,200]
# S.zlim = [-200,200]
from time import time
print()
t0 = time()
# print('CORREÇÃO MOMENTO ANGULAR')
S.simular(200, False, False)
print()
print('tempo: ', time() - t0)
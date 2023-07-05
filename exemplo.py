from condicoesIniciais.condicoesArtigo import condicoesArtigo

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

# G = 0.3
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

S = Simulacao3D(massas=massas, R0=C.r, P0=C.p, h=0.001, G=G)
# S = Simulacao3D(massas=massas, R0=posicoes, P0=momentos, h=0.05, G=G)
from time import time
print()
t0 = time()
# print('CORREÇÃO MOMENTO ANGULAR')
S.simular(5000, exibir=True, salvar=False)
print()
print(S.R)
print('tempo: ', time() - t0)

# exibe as infos de momento linear transformados
import matplotlib.pyplot as plt

P_sp = S.Ps_sp
P_sp = list(zip(*P_sp))
cores = ["black", "blue", "red", "green"]
print(len(P_sp), len(P_sp[0]), len(P_sp[0][0]))
plt.title('Momento linear total de cada corpo')
for i,corpo in enumerate(P_sp):
  # calcula os momentos lineares totais
  Ps_a = [sum(k) for k in corpo]
  plt.plot(Ps_a, c=cores[i])
  
plt.show()

plt.title('Momento de dilatação')
plt.plot(S.Ds_sp)
plt.show()

plt.title('Momento de inércia')
plt.plot(S.Icms_sp)
plt.show()
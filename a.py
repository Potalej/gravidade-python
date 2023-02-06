"""
  Leitura de informações de dados.
"""

from simulacao.ler import ler_arquivo
from simulacao.simulacao3d import Simulacao3D
from auxiliares.informacoes import informacoes

m, Rs, Ps = ler_arquivo('./pontos/pontos_1675611148.6727002.txt', 3)
# m, Rs, Ps = ler_arquivo('./pontos/pontos_1675546797.6079152.txt', 3)
print('lido')
# infos = informacoes(m, Rs, Ps, exibir=True)
S = Simulacao3D(m, Rs[0], [[0,0,0] for i in range(len(m))])
S.xlim = [-50000,50000]
S.ylim = [-50000,50000]
S.zlim = [-50000,50000]
S.visualizar(Rs)
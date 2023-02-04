"""
  Leitura de informações de dados.
"""

from simulacao.ler import ler_arquivo
from simulacao.simulacao3d import Simulacao3D
from auxiliares.informacoes import informacoes

# m, Rs, Ps = ler_arquivo('./pontos/pontos_1675483175.8847883.txt', 3)
m, Rs, Ps = ler_arquivo('./pontos/pontos_1675546797.6079152.txt', 3)

# infos = informacoes(m, Rs, Ps, exibir=True)
S = Simulacao3D(m, Rs[0], Ps[0])
S.visualizar(Rs)
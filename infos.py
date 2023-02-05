"""
  Leitura de informações de dados.
"""

from simulacao.ler import ler_arquivo
from simulacao.simulacao3d import Simulacao3D
from auxiliares.informacoes import informacoes

m, Rs, Ps = ler_arquivo('./pontos/pontos_1675609348.0346444.txt', 3)

# infos = informacoes(m, Rs, Ps, exibir=True)
S = Simulacao3D(m, Rs[0], Ps[0])
S.xlim = [-5000,5000]
S.ylim = [-5000,5000]
S.zlim = [-5000,5000]
S.visualizar(Rs)
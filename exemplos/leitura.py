"""
  Exemplo de leitura e visualização de dados em um arquivo.
"""

from simulacao.ler import ler_arquivo
from simulacao.simulacao3d import Simulacao3D

m, Rs, Ps = ler_arquivo('./pontos/pontos_1675483175.8847883.txt', 3)
S = Simulacao3D(m, Rs[0], Ps[0])
S.visualizar(Rs)

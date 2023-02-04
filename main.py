from simulacao.ler import ler_arquivo
from simulacao.simulacao3d import Simulacao3D

m = [100, 100, 80]
R0 = [[100, 100, 100],[-100, -100, 0], [-200, 200,0]]
P0 = [[70, 0,0],[0, 30,10],[0,-5,-10]]
S = Simulacao3D(m, R0, P0, G=3)
S.simular(500, salvar=True)

# m, Rs, Ps = ler_arquivo('./pontos/pontos_1675483175.8847883.txt', 3)
# S = Simulacao3D(m, Rs[0], Ps[0])
# S.visualizar(Rs)

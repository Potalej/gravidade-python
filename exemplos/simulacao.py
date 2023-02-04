from simulacao.simulacao3d import Simulacao3D

m = [100, 100, 80]
R0 = [[100, 100, 100],[-100, -100, 0], [-200, 200,0]]
P0 = [[70, 0,0],[0, 30,10],[0,-5,-10]]
S = Simulacao3D(m, R0, P0, G=3)
S.simular(500, salvar=True)
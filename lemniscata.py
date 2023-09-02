from fortran.ler import ler_csv
import matplotlib.pyplot as plt
from auxiliares.shapedynamics import mudar_somente_posicao

dir_verlet = '20230828_10.csv'
dir_rk4 = '20230828_11.csv'

m, posicoes, momentos = ler_csv(dir_rk4)
R = list(zip(*posicoes))
coords = [[] for corpo in range(len(m))]
for Ri in R:
  novas_coords = Ri
  novas_coords = mudar_somente_posicao(m, novas_coords)
  for i, coord in enumerate(novas_coords):
    coords[i].append(coord)
Ri = coords[0]
R = list(zip(*Ri))
X, Y, Z = R
plt.plot(X, Y, linestyle="solid", c='black', linewidth=0.3, label="RK4")

m, posicoes, momentos = ler_csv(dir_verlet)
R = list(zip(*posicoes))
coords = [[] for corpo in range(len(m))]
for Ri in R:
  novas_coords = Ri
  novas_coords = mudar_somente_posicao(m, novas_coords)
  for i, coord in enumerate(novas_coords):
    coords[i].append(coord)
Ri = coords[0]
R = list(zip(*Ri))
X, Y, Z = R
plt.plot(X, Y, linestyle="solid", c='red', linewidth=3, label="Verlet")

plt.xticks([])
plt.yticks([])
plt.legend(fontsize=20)
plt.show()
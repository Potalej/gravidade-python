"""
  Aqui eh feita a correcao numerica utilizando a matriz jacobiana.
"""

from auxiliares.hamiltoniano import H
from auxiliares.auxiliares import momentoAngular, centro_massas, distancia, produto_interno
from numpy.linalg import solve

# CALCULAR OS GRADIENTES

# gradiente da energia
def gradiente_energia (G, m, Rs, Ps, N):
  grad = []
  for a in range(N):
    grad_a = [0, 0, 0, Ps[a][0]/m[a], Ps[a][1]/m[a], Ps[a][2]/m[a]]
    for b in range(N):
      if b != a:
        rab = distancia(Rs[a], Rs[b])
        grad_a[0] += m[b]*(Rs[b][0]-Rs[a][0])* (1/rab**3)
        grad_a[1] += m[b]*(Rs[b][1]-Rs[a][1])* (1/rab**3)
        grad_a[2] += m[b]*(Rs[b][2]-Rs[a][2])* (1/rab**3)
    grad_a[0] *= -G*m[a]
    grad_a[1] *= -G*m[a]
    grad_a[2] *= -G*m[a]
    grad += grad_a
  return grad

# gradiente do momento angular
def gradiente_momentoAngular (Rs, Ps, N):
  grad = [[],[],[]]
  for a in range(N):
    grad[0] += [0, Ps[a][2], -Ps[a][1], 0, -Rs[a][2], Rs[a][1]]
    grad[1] += [-Ps[a][2], 0, Ps[a][0], Rs[a][2], 0, -Rs[a][0]]
    grad[2] += [Ps[a][1], -Ps[a][0], 0, -Rs[a][1], Rs[a][0], 0]
  return grad

# gradiente do momento linear
def gradiente_momentoLinear (N):
  grad = [[],[],[]]
  grad_pxa = [0,0,0,1,0,0]
  grad_pya = [0,0,0,0,1,0]
  grad_pza = [0,0,0,0,0,1]
  for _ in range(N):
    grad[0] += grad_pxa
    grad[1] += grad_pya
    grad[2] += grad_pza
  return grad

# gradiente do centro de massas
def gradiente_centroMassas (m, M, N):
  grad = [[],[],[]]
  for a in range(N):
    grad[0] += [m[a]/M, 0, 0, 0, 0, 0]
    grad[1] += [0, m[a]/M, 0, 0, 0, 0]
    grad[2] += [0, 0, m[a]/M, 0, 0, 0]
  return grad

# calcular J*Jt
def matriz_normal (G, m, M, Rs, Ps, N):
  # gradientes
  gradH = gradiente_energia(G, m, Rs, Ps, N)
  gradJx, gradJy, gradJz = gradiente_momentoAngular(Rs, Ps, N)
  gradPx, gradPy, gradPz = gradiente_momentoLinear(N)
  gradRcmx, gradRcmy, gradRcmz = gradiente_centroMassas(m, M, N)

  grad = [gradH, gradJx, gradJy, gradJz, gradPx, gradPy, gradPz, gradRcmx, gradRcmy, gradRcmz]

  JJt = []
  for gi in grad:
    JJt.append([])
    for gj in grad:
      JJt[-1].append(produto_interno(gj, gi))
  
  return grad, JJt

# calcular o lado direito
def Gx (G, m, M, Rs, Ps, N):
  vetG = []
  
  # energia total
  vetG.append(-H(Rs, Ps, m, G))

  # momento angular total
  Js = momentoAngular(Rs, Ps)
  vetG.append(-Js[0])
  vetG.append(-Js[1])
  vetG.append(-Js[2])

  # momento linear total
  PsG = list(zip(*Ps))
  vetG.append(-sum(PsG[0]))
  vetG.append(-sum(PsG[1]))
  vetG.append(-sum(PsG[2]))

  # centro de massas
  Rcm = centro_massas(m, Rs)
  vetG.append(-Rcm[0])
  vetG.append(-Rcm[1])
  vetG.append(-Rcm[2])

  return vetG

# resolver o sistema 10x10
def resolverSistema (A, b):
  return solve(A, b)

def correcao (m, Rs, Ps, G):
  N = len(m)
  M = sum(m)
  grads, JJt = matriz_normal(G, m, M, Rs, Ps, N)
  vetG = Gx(G, m, M, Rs, Ps, N)
  alphas = list(resolverSistema(JJt, vetG))

  u = [[alphas[i]*g for g in grads[i]] for i in range(10)]
  u = [sum(list(i)) for i in list(zip(*u))]
  
  R, P = [], []
  for a in range(0, N):
    R.append([Rs[a][0] + u[6*a],   Rs[a][1] + u[6*a+1], Rs[a][2] + u[6*a+2]])
    P.append([Ps[a][0] + u[6*a+3], Ps[a][1] + u[6*a+4], Ps[a][2] + u[6*a+5]])

  return R, P
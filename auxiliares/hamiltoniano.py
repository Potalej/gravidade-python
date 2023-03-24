"""
  Cálculos ligados ao hamiltoniano do sistema.
"""

from math import sqrt
from numpy import true_divide
from auxiliares.auxiliares import momentoAngular

def EC (P, m:list)->float:
  soma = 0
  for a in range(len(m)):
    pa = P[a]
    pi_pa = sum(pa_i**2 for pa_i in pa)
    soma += pi_pa/(2*m[a])
  return soma

def U (R, m:list)->float:
  soma = 0
  for b in range(1, len(m)):
    for a in range(b):
      ra = R[a]
      rb = R[b]
      dist = sqrt(sum((ra[i] - rb[i])**2 for i in range(len(ra))))
      soma += m[a]*m[b] / dist
  return -soma

def H (R, P, m:list)->float:
  """Energia total"""
  return EC(P, m) + U(R, m)

def derH_derR (R, m, a):
  ma = m[a]
  Ra = R[a]
  der = [0,0,0]
  for b in range(len(m)):
    if a == b: continue
    Rb = R[b]
    rab3 = sum((Ra[i]-Rb[i])**2 for i in range(3))**(3/2)
    for i in range(3):
      der[i] += m[b]*(Rb[i]-Ra[i])/rab3
  der = [-3*ma*i for i in der]
  return der

def gradH (R, P, m):
  grad = []
  for i in range(len(m)):
    der = derH_derR(R, m, i)
    grad += [
      der[0],
      P[i][0]/m[i],
      der[1],
      P[i][1]/m[i],
      der[2],
      P[i][2]/m[i],
    ]
  return grad

def ajustarH (R:list, P:list, m:list, e0:float, Fsomas:list)->tuple:
  e = H(R, P, m)
  grad = gradH(R, P, m)
  
  norma_grad2 = sum(g*g for g in grad)
  fator = true_divide(e-e0, norma_grad2)
  dif = [fator*gradi for gradi in grad]

  k = max(abs(i) for i in dif)

  if k <= 1:
    for i in range(len(R)):        
      R[i][0] -= dif[6*i]
      P[i][0] -= dif[6*i+1]

      R[i][1] -= dif[6*i+2]
      P[i][1] -= dif[6*i+3]

      R[i][2] -= dif[6*i+4]
      P[i][2] -= dif[6*i+5]

  return R, P, e

# ajuste no momento angular
def ajusteJ (R, P, J0):
  """
    Ajuste no momento angular via método do gradiente.
  """
  # gradientes
  gradx, grady, gradz = [], [], []
  norma_gradx, norma_grady, norma_gradz = 0, 0, 0

  for a in range(len(R)): # N
    # separa para facilitar
    Ra, Pa = R[a], P[a]
    Rax, Ray, Raz = Ra
    Pax, Pay, Paz = Pa
    # adiciona nos arrays
    gradx += [0, 0, Paz, -Raz, -Pay, Ray]
    grady += [-Paz, Raz, 0, 0, Pax, -Rax]
    gradz += [Pay, -Ray, -Pax, Rax, 0, 0]
    # calcula as normas
    norma_gradx += Paz*Paz + Raz*Raz + Pay*Pay + Ray*Ray
    norma_grady += Paz*Paz + Raz*Raz + Pax*Pax + Rax*Rax
    norma_gradz += Pay*Pay + Ray*Ray + Pax*Pax + Rax*Rax

  # momento angular
  J = momentoAngular(R, P) # N

  # fatores de distância
  fatorx = true_divide(J[0]-J0[0], norma_gradx)
  fatory = true_divide(J[1]-J0[1], norma_grady)
  fatorz = true_divide(J[2]-J0[2], norma_gradz)

  # soma os valores para adicionar de uma vez
  # dif = [fatorx*gradx[i] + fatory*grady[i] + fatorz*gradz[i] for i in range(len(gradx))] # 6N # backup
  # a vantagem de usar a dif acima eh poder filtrar pelo maximo, mas talvez nao seja necessario nesse caso...

  for a in range(len(R)): # N       

    # R[a][0] -= dif[6*a+0] # backup
    # P[a][0] -= dif[6*a+1] # backup

    # R[a][1] -= dif[6*a+2] # backup
    # P[a][1] -= dif[6*a+3] # backup

    # R[a][2] -= dif[6*a+4] # backup
    # P[a][2] -= dif[6*a+5] # backup

    R[a][0] -= fatorx*gradx[6*a+0] + fatory*grady[6*a+0] + fatorz*gradz[6*a+0]
    P[a][0] -= fatorx*gradx[6*a+1] + fatory*grady[6*a+1] + fatorz*gradz[6*a+1]

    R[a][1] -= fatorx*gradx[6*a+2] + fatory*grady[6*a+2] + fatorz*gradz[6*a+2]
    P[a][1] -= fatorx*gradx[6*a+3] + fatory*grady[6*a+3] + fatorz*gradz[6*a+3]

    R[a][2] -= fatorx*gradx[6*a+4] + fatory*grady[6*a+4] + fatorz*gradz[6*a+4]
    P[a][2] -= fatorx*gradx[6*a+5] + fatory*grady[6*a+5] + fatorz*gradz[6*a+5]

  return R, P



def juntos (R, P, m, e0, Fsomas, J0):
  e = H(R, P, m)
  grad = gradH(P, m, Fsomas)
  norma_grad2 = sum(g*g for g in grad)
  fatorH = true_divide(e-e0, norma_grad2)

  # gradientes
  gradx, grady, gradz = [], [], []
  norma_gradx, norma_grady, norma_gradz = 0, 0, 0

  for a in range(len(R)): # N
    # separa para facilitar
    Ra, Pa = R[a], P[a]
    Rax, Ray, Raz = Ra
    Pax, Pay, Paz = Pa
    # adiciona nos arrays
    gradx += [0, 0, Paz, -Raz, -Pay, Ray]
    grady += [-Paz, Raz, 0, 0, Pax, -Rax]
    gradz += [Pay, -Ray, -Pax, Rax, 0, 0]
    # calcula as normas
    norma_gradx += Paz*Paz + Raz*Raz + Pay*Pay + Ray*Ray
    norma_grady += Paz*Paz + Raz*Raz + Pax*Pax + Rax*Rax
    norma_gradz += Pay*Pay + Ray*Ray + Pax*Pax + Rax*Rax

  # momento angualr
  J = momentoAngular(R, P) # N

  # fatores de distância
  fatorx = true_divide(J[0]-J0[0], norma_gradx)
  fatory = true_divide(J[1]-J0[1], norma_grady)
  fatorz = true_divide(J[2]-J0[2], norma_gradz)

  for a in range(len(R)): # N       

    R[a][0] -= fatorH*grad[6*a+0] + fatorx*gradx[6*a+0] + fatory*grady[6*a+0] + fatorz*gradz[6*a+0]
    P[a][0] -= fatorH*grad[6*a+1] + fatorx*gradx[6*a+1] + fatory*grady[6*a+1] + fatorz*gradz[6*a+1]

    R[a][1] -= fatorH*grad[6*a+2] + fatorx*gradx[6*a+2] + fatory*grady[6*a+2] + fatorz*gradz[6*a+2]
    P[a][1] -= fatorH*grad[6*a+3] + fatorx*gradx[6*a+3] + fatory*grady[6*a+3] + fatorz*gradz[6*a+3]

    R[a][2] -= fatorH*grad[6*a+4] + fatorx*gradx[6*a+4] + fatory*grady[6*a+4] + fatorz*gradz[6*a+4]
    P[a][2] -= fatorH*grad[6*a+5] + fatorx*gradx[6*a+5] + fatory*grady[6*a+5] + fatorz*gradz[6*a+5]

  return R, P










# ajuste no momento angular
def ajusteJ1 (R, P, J0):
  """
    Ajuste no momento angular via método do gradiente.
  """
  # X
  gradx = []
  norma_gradx = 0
  for a in range(len(R)):
    Ra, Pa = R[a], P[a]
    Rax, Ray, Raz = Ra
    Pax, Pay, Paz = Pa
    gradx += [0, 0, Paz, -Raz, -Pay, Ray]
    norma_gradx += Paz*Paz + Raz*Raz + Pay*Pay + Ray*Ray

  J = momentoAngular(R, P)
  fatorx = true_divide(J[0]-J0[0], norma_gradx)

  for a in range(len(R)):
    R[a][0] -= fatorx*gradx[6*a+0]
    P[a][0] -= fatorx*gradx[6*a+1]

  # Y
  grady = []
  norma_grady = 0
  for a in range(len(R)):
    Ra, Pa = R[a], P[a]
    Rax, Ray, Raz = Ra
    Pax, Pay, Paz = Pa
    grady += [-Paz, Raz, 0, 0, Pax, -Rax]
    norma_grady += Paz*Paz + Raz*Raz + Pax*Pax + Rax*Rax

  J = momentoAngular(R, P)
  fatory = true_divide(J[1]-J0[1], norma_grady)

  for a in range(len(R)):
    R[a][1] -= fatory*grady[6*a+2]
    P[a][1] -= fatory*grady[6*a+3]

  # Z
  gradz = []
  norma_gradz = 0
  for a in range(len(R)):
    Ra, Pa = R[a], P[a]
    Rax, Ray, Raz = Ra
    Pax, Pay, Paz = Pa
    gradz += [Pay, -Ray, -Pax, Rax, 0, 0]
    norma_gradz += Pay*Pay + Ray*Ray + Pax*Pax + Rax*Rax

  J = momentoAngular(R, P)
  fatorz = true_divide(J[2]-J0[2], norma_gradz)

  for a in range(len(R)):
    R[a][2] -= fatorz*gradz[6*a+4]
    P[a][2] -= fatorz*gradz[6*a+5]

  return R, P



# 03/03/2023
def ajustePTotal (P, P0):
  """Recebe a lista de vetores de momento linear."""
  N = len(P)
  den = 1/(3*N)
  res = [0,0,0]
  for a in range(N):
    res[0] += P[a][0] - P0[0]
    res[1] += P[a][1] - P0[1]
    res[2] += P[a][2] - P0[2]
  res = [r*den for r in res]
  P = [[
    p[0]-res[0],
    p[1]-res[1],
    p[2]-res[2],
  ] for p in P]
  return P

def rcm(massas, Rs):
  mtot = sum(massas)
  Rcm = [[
    r[0]*massas[a],
    r[1]*massas[a],
    r[2]*massas[a]
  ] for a,r in enumerate(Rs)]
  return [sum(a)/mtot for a in list(zip(*Rcm))]

def ajusteCentroMassas (massas, Rs, rcm0_int):
  """Recebe as massas e a lista de vetores de posição."""

  num = [[
    massas[a]*Rs[a][0] - rcm0_int[0],
    massas[a]*Rs[a][1] - rcm0_int[1],
    massas[a]*Rs[a][2] - rcm0_int[1],
  ] for a in range(len(massas))]

  mtot2 = sum(mi**2 for mi in massas)

  num = [sum(n)/(3*mtot2) for n in list(zip(*num))]

  Rs = [[
    R[0] - massas[a]*num[0],
    R[1] - massas[a]*num[1],
    R[2] - massas[a]*num[2]
  ] for a,R in enumerate(Rs)]  

  return Rs
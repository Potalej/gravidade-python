"""
    Cálculos ligados ao hamiltoniano do sistema.
"""

from math import sqrt
from numpy import true_divide

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
      soma += m[a]*m[b]/dist
  return -soma

def H (R, P, m:list)->float:
    """Energia total"""
    return EC(P, m) + U(R, m)
            
def gradH (P, m, Fsomas):
  grad = []
  for i in range(len(m)):
    grad += [
      -Fsomas[i][0],
      P[i][0]/m[i],
      -Fsomas[i][1],
      P[i][1]/m[i],
    ]
  return grad

def p1_n (R1, R2, m1, m2):
  N = [R2[0]-R1[0],R2[1]-R1[1]]
  normaN = sqrt(sum(ni**2 for ni in N))
  N_hat = [ni/normaN for ni in N]

  T = [-N_hat[1],N_hat[0]]

  v1n = sum(ni for ni in N_hat)*(m1-m2)/(m1+m2)
  v1t = sum(t for t in T)

  v1n_ = [v1n * ni for ni in N_hat]
  v1t_ = [v1t * ti for ti in T]
  
  return [v1n_[0]+v1t_[0],v1n_[1]+v1t_[1]]


def ajustar (R:list, P:list, m:list, e0:float, Fsomas:list, colisoes=[])->tuple:
  e = H(R, P, m)
  # grad = gradH1(R, P, m)
  grad = gradH(P, m, Fsomas)
  if len(colisoes) > 0:
    for i in range(len(R)):
      if i in colisoes['colidiu']:
        p_ = [0,0]
        for j in colisoes['colisoes'][i]:
          pk = p1_n(R[i], R[j], m[i], m[j])
          p_[0] += pk[0]
          p_[1] += pk[1]
        grad[4*i] += m[i]*p_[0]
        grad[4*i+2] += m[i]*p_[1]

  norma_grad2 = sum(g*g for g in grad)
  fator = true_divide(e-e0, norma_grad2)
  dif = [fator*gradi for gradi in grad]

  for i in range(len(R)):        
      R[i][0] -= dif[4*i]
      R[i][1] -= dif[4*i+2]
      P[i][0] -= dif[4*i+1]
      P[i][1] -= dif[4*i+3]

  return R, P, e
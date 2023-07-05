"""
  Algumas coisas da Shape Dynamics
"""

from math import sqrt
from auxiliares.auxiliares import centro_massas, momento_inercia_cm

def momento_linear_medio (P):
  return [sum(p)/len(P) for p in list(zip(*P))]

def momento_linear_relativo (Pcm, P_a):
  return [P_a[i] - Pcm[i] for i in range(3)]

def centro_massas_relativo (Rcm, R_a):
  return [R_a[i] - Rcm[i] for i in range(3)]

def momento_dilatacao (Rcms, Pcms):
  return sum(
    sum(Rcms[a][i]*Pcms[a][i] for i in range(3))
    for a in range(len(Rcms))
  )

def mudanca_coordenadas (massas, R, P):
  """
    Aplica a mudanca de coordenadas:

    s_a = r_a^cm sqrt(m_a / Icm)

    p_a = p_a sqrt(Icm / m_a) - D s_a
  """
  # centro de massas
  rcm = centro_massas(massas, R)
  rcms = [centro_massas_relativo(rcm, ra) for ra in R]

  # momento de inercia
  Icm = momento_inercia_cm(massas, R)

  # aplica a transformacao de posicao
  sigmas = [
    [sqrt(massas[a]/Icm) * rcms[a][i] for i in range(3)]
    for a in range(len(massas))
  ]

  # momentos lineares relativos
  pcm = momento_linear_medio(P)
  pcms = [momento_linear_relativo(pcm, pa) for pa in P]

  # momento de dilatacao
  D = momento_dilatacao(rcms, pcms)

  # print('ICM: ', Icm)

  # aplica a transformacao de momento linear
  pis = [
    [sqrt(Icm/massas[a]) * pcms[a][i] - D * sigmas[a][i] for i in range(3)]
    for a in range(len(massas))
  ]

  return sigmas, pis, momento_dilatacao(R, P), Icm
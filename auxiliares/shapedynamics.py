"""
  Funcoes relacionadas a Shape Dynamics.
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

def mudar_posicao (massas, Rcms, Icm):
  return [
    [sqrt(massas[a]/Icm)*Rcms[a][i] for i in range(3)]
    for a in range(len(massas))
  ]

def mudar_somente_posicao (massas, Rs):
   # centro de massas
  rcm = centro_massas(massas, Rs)
  rcms = [centro_massas_relativo(rcm, ra) for ra in Rs]

  # momento de inercia
  Icm = momento_inercia_cm(massas, Rs)
  return mudar_posicao(massas, rcms, Icm)

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
  sigmas = mudar_posicao(massas, Rcms, Icm)

  # momentos lineares relativos
  pcm = momento_linear_medio(P)
  pcms = [momento_linear_relativo(pcm, pa) for pa in P]

  # momento de dilatacao
  D = momento_dilatacao(rcms, pcms)

  # aplica a transformacao de momento linear
  pis = [
    [sqrt(Icm/massas[a]) * pcms[a][i] - D * sigmas[a][i] for i in range(3)]
    for a in range(len(massas))
  ]

  return sigmas, pis, momento_dilatacao(R, P), Icm

def complexidade (I, mtot, energia_potencial):
  """Calcula a complexidade a partir do momento de inércia."""
  L_rms = (I**.5)/mtot
  L_mhl = mtot**2 / abs(energia_potencial)
  C = L_rms/L_mhl
  return C
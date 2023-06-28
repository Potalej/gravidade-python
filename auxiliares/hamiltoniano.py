"""
  Cálculos ligados ao hamiltoniano do sistema.
"""

from math import sqrt
from numpy import true_divide
from auxiliares.auxiliares import distancia, norma2

def EC (P, m:list)->float:
  soma = 0
  for a in range(len(m)):
    pa = P[a]
    soma += norma2(pa)/m[a]
  return soma/2

def U (R, m:list, G)->float:
  soma = 0
  for b in range(1, len(m)):
    for a in range(b):
      soma += m[a]*m[b] * (1/distancia(R[a], R[b]))
  return -G*soma

def H (R, P, m:list, G)->float:
  """Energia total"""
  return EC(P, m) + U(R, m, G)

  return R, P
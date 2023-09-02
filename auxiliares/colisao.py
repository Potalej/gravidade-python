from auxiliares.auxiliares import distancia, produto_interno, norma2, prodvetR3
import config.configs as config
from statistics import mean, stdev
import matplotlib.pyplot as plt

def colisao (massas, R, P):
  # verifica se alguma distancia esta menor que o minimo
  for a in range(len(massas)):
    ma, Ra, Pa = massas[a], R[a], P[a]
    Va = [p/ma for p in Pa]
    
    for b in range(a):
      mb, Rb, Pb = massas[b], R[b], P[b]
      Vb = [p/mb for p in Pb]

      if (distancia(Ra, Rb) <= config.DIST_MIN_COLISAO):
        # agora verifica o sinal da derivada da distancia
        # se estiver negativo, eh porque estao se aproximado
        dif_velocidade = [Va[i]-Vb[i] for i in range(3)]
        dif_posicao    = [Ra[i]-Rb[i] for i in range(3)]
        if (produto_interno(dif_velocidade, dif_posicao) < 0):
          # calcula a colisao
          P[a], P[b] = colide(ma, mb, Ra, Rb, Pa, Pb)
  return P


def colide (ma, mb, Ra, Rb, Pa, Pb):
  """
    Funcao que de fato faz a colisao.
    Os parametros sao as massas, posicoes e momentos lineares.
  """

  # Debug
  print('colidiu')

  # separa as velocidades
  ua, ub = [pa_i/ma for pa_i in Pa], [pb_i/mb for pb_i in Pb]

  # vetor normal
  N = [Rb[i]-Ra[i] for i in range(3)]
  norma = norma2(N)**.5
  N_ = [Ni/norma for Ni in N]

  # calcula a componente tangente
  u1, u2 = produto_interno(ua, N_), produto_interno(ub, N_)
  # calcula a componente do plano
  ua_p, ub_p = [ua[i] - u1*N[i] for i in range(3)], [ub[i] - u2*N[i] for i in range(3)]
  norma_a_p = norma2(ua_p)**.5
  norma_b_p = norma2(ub_p)**.5
  ua_p = [ui/norma_a_p for ui in ua_p]
  ub_p = [ui/norma_b_p for ui in ub_p]

  # obtem v1 e v2
  v1 = (u1*(ma-mb)+2*mb*u2)/(ma+mb)
  v2 = (u2*(mb-ma)+2*ma*u1)/(ma+mb)

  # calcula as novas velocidades
  va, vb = [ua_p[i] + v1*N_[i] for i in range(3)], [ub_p[i] + v2*N_[i] for i in range(3)]

  # novos momentos
  Pa, Pb = [va_i*ma for va_i in va], [vb_i*mb for vb_i in vb]

  return Pa, Pb
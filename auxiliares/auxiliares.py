"""
  Funções auxiliares que são usadas com alguma frequência nos scripts.
"""

def prodvetR2 (u:list, v:list)->float:
  """Produto vetorial no R2. Retorna um escalar real."""
  return u[0]*v[1]-u[1]*v[0]

def prodvetR3 (u:list, v:list)->list:
  """Produto vetorial no R3. Retorna um vetor no R3 que é ortogonal a `u` e a `v`."""
  return [u[1]*v[2]-v[1]*u[2], -u[0]*v[2]+v[0]*u[2], u[0]*v[1]-v[0]*u[1]]

def norma2 (u:list)->float:
    """Quadrado da norma euclidiana."""
    return sum(ui**2 for ui in u)

def momento_inercia_cm (m:list, r:list)->float:
    """Momento de inércia relativo ao centro de massas."""
    return sum(m[i] * norma2(r[i]) for i in range(len(m)))

def momentos_angulares (m:list, r:list, v:list)->list:
  """Momento angular de cada partícula do sistema."""
  if len(r[0]) == 2:
    if m != []:
      return [prodvetR3([r[i][0], r[i][1], 0], [v[i][0]*m[i], v[i][1]*m[i], 0]) for i in range(len(m))]
    else:
      return [prodvetR3([r[i][0], r[i][1], 0], [v[i][0], v[i][1], 0]) for i in range(len(v))]
  else:
    if m != []:
      return [prodvetR3([r[i][0], r[i][1], r[i][2]], [v[i][0]*m[i], v[i][1]*m[i], v[i][2]*m[i]]) for i in range(len(m))]
    else:
      return [prodvetR3([r[i][0], r[i][1], r[i][2]], [v[i][0], v[i][1], v[i][2]]) for i in range(len(v))]

def momentoAngular (R, P):
  """Momento angular total."""
  Ja = momentos_angulares([], R, P)
  Js = list(zip(*Ja))
  J = [sum(Ji) for Ji in Js]
  return J

def centro_massas (m:list, r:list)->list:
  """Ponto do centro de massas do sistema."""
  rcm = [0 for i in range(len(r[0]))]
  for i in range(len(m)):
      for j in range(len(r[i])):
          rcm[j] += m[i]*r[i][j]
  mtot = sum(m)
  rcm = [rcm_i/mtot for rcm_i in rcm]
  return rcm

def momento_linear_total_velocidade (m:list, v:list)->list:
    """Momento linear total do sistema a partir das velocidades e massas."""
    P = [0 for i in range(len(v[0]))]
    for i in range(len(m)):
        for j in range(len(v[i])):
            P[j] += m[i]*v[i][j]
    return P

def tensor_inercia (ma, Ra):
  r1, r2, r3 = Ra
  I = [
    [ri*ma for ri in [-(r2**2 + r3**2), r1*r2, r1*r3]],
    [ri*ma for ri in [r1*r2, -(r1**2 + r3**2), r2*r3]],
    [ri*ma for ri in [r1*r3, r2*r3, -(r1**2 + r2**2)]],
  ]
  return I

def tensor_inercia_geral (m, R):
  I = [[0 for i in range(3)] for j in range(3)]
  for a in range(len(m)):
    Ia = tensor_inercia(m[a], R[a])
    for i in range(3):
      for j in range(3):
        I[i][j] += Ia[i][j]
  return I

def distancia (u, v):
  """Distancia euclidiana entre dois pontos no espaco."""
  return norma2([u[i]-v[i] for i in range(len(u))])**0.5

def produto_interno (u, v):
  """Produto interno entre dois vetores."""
  return sum(u[i]*v[i] for i in range(len(u)))
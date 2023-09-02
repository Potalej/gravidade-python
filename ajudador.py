import matplotlib.pyplot as plt
from auxiliares.hamiltoniano import H, U
from auxiliares.auxiliares import momento_inercia_cm, momentoAngular, centro_massas, complexidade as C
from auxiliares.shapedynamics import momento_dilatacao

def informacoes_basicas (
    m                 : list,
    Rs                : list,
    Ps                : list,
    G                 : float,
    energia           : list = [1],
    angular           : list = [0],
    linear            : list = [],
    centro_de_massas  : list = [],
    dilatacao         : list = [2],
    inercia           : list = [3],
    complexidade      : list = [],
    formato           : list = [1,4]
  ):
  # Informacoes
  dados = {
    'energia'      : [energia] if len(energia) != 0                   else False,
    'angular_x'    : [angular] if len(angular) != 0                   else False,
    'angular_y'    : [angular] if len(angular) != 0                   else False,
    'angular_z'    : [angular] if len(angular) != 0                   else False,
    'linear_x'     : [linear] if len(linear) != 0                     else False,
    'linear_y'     : [linear] if len(linear) != 0                     else False,
    'linear_z'     : [linear] if len(linear) != 0                     else False,
    'centro_x'     : [centro_de_massas] if len(centro_de_massas) != 0 else False,
    'centro_y'     : [centro_de_massas] if len(centro_de_massas) != 0 else False,
    'centro_z'     : [centro_de_massas] if len(centro_de_massas) != 0 else False,
    'dilatacao'    : [dilatacao] if len(dilatacao) != 0               else False,
    'inercia'      : [inercia] if len(inercia) != 0                   else False,
    'complexidade' : [complexidade] if len(complexidade) != 0         else False,
  }
  # indices
  indices = ['energia', 'angular_x','angular_y','angular_z','linear_x','linear_y','linear_z','centro_x','centro_y','centro_z','dilatacao','inercia','complexidade']

  for indice in indices:
    if not dados[indice]: del dados[indice]

  # Percorre os passos
  for i in range(len(Rs)):
    # Captura infos atuais
    R, P = Rs[i], Ps[i]

    # Energia
    if 'energia' in dados:
      dados['energia'].append(H(R, P, m, G))

    # Angular
    if 'angular_x' in dados:
      # Calcula o momento angular
      [Jx, Jy, Jz] = momentoAngular(R, P)
      # Salva
      dados['angular_x'].append(Jx)
      dados['angular_y'].append(Jy)
      dados['angular_z'].append(Jz)

    # Linear
    if 'linear_x' in dados:
      # Calcula o momento linear
      Ptot = list(zip(*P))
      [Px, Py, Pz] = [sum(p) for p in Ptot]
      dados['linear_x'].append(Px)
      dados['linear_y'].append(Py)
      dados['linear_z'].append(Pz)

    # Centro de massas
    if 'centro_x' in dados:
      # Calcula o centro de massas
      [rcmx, rcmy, rcmz] = centro_massas(m, R)
      dados['centro_x'].append(rcmx)
      dados['centro_y'].append(rcmy)
      dados['centro_z'].append(rcmz)
    
    # Dilatacao
    if 'dilatacao' in dados:
      # Calcula o momento de dilatacao
      D = momento_dilatacao(R, P)
      dados['dilatacao'].append(D)
    
    # Momento de inercia
    if 'inercia' in dados:
      # Calcula o momento de inercia
      I = momento_inercia_cm(m, R)
      dados['inercia'].append(I)

    # Complexidade
    if 'complexidade' in dados:
      # Calcula momento inercia se necessario
      if 'inercia' not in dados:
        I = momento_inercia_cm(m,R)
      # Calcula energia potencial
      potencial = U(R, m, G)
      # Calcula a complexidade
      c = C(I, sum(m), potencial)
      dados['complexidade'].append(c)

  # Agora precisa plotar
  # Monta a figura e os eixos
  fig, ax = plt.subplots(*formato)
  # Se o eixo for unidimensional, eh so percorrer e plotar
  if formato[0] == 1:
    for indice in dados:
      posicao = dados[indice][0][0]
      ax[posicao].set_title(indice)
      ax[posicao].plot(dados[indice][1:])
    plt.show()
  # Se nao for, precisa verificar antes de plotar
  else:
    for indice in dados:
      posicao = dados[indice][0]

      ax[posicao[0], posicao[1]].set_title(indice)
      ax[posicao[0], posicao[1]].plot(dados[indice][1:])
    plt.show()
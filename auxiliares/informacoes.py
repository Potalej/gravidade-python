from auxiliares.hamiltoniano import H, U
from auxiliares.auxiliares import momentoAngular, centro_massas, momento_inercia_cm, complexidade

def informacoes (m, Rs, Ps):
  """Obtém as informações de um dado conjunto de posições e momentos lineares."""
  infos = {
    "H": [], # energia total
    "U": [], # energia potencial
    "P": [], # momento linear total
    "J": [], # momento angular total
    "Rcm": [], # centor de massas
    "I": [], # momento de inércia
    "C": [], # complexidade
  }

  qntd = len(Rs)
  for i in range(qntd):
    R, P = Rs[i], Ps[i]

    # energia total
    infos["H"] += [H(R, P, m)]
    
    # energia potencial
    infos["U"] += [U(R, m)]

    # momento linear total
    infos["P"] += [[sum(Pi) for Pi in list(zip(*P))]]

    # momento angular total
    infos["J"] += [momentoAngular([], R, P)]
    
    # centro de massas
    infos["Rcm"] += [centro_massas(m, R)]

    # momento de inércia
    infos["I"] += [momento_inercia_cm(m, R)]

    # complexidade
    infos["C"] += [complexidade(m, infos["I"][-1], infos["U"][-1])]
  
  return infos
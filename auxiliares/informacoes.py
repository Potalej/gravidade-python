from auxiliares.hamiltoniano import H, U
from auxiliares.auxiliares import momentoAngular, centro_massas, momento_inercia_cm
from auxiliares.shapedynamics import complexidade
from statistics import mean, stdev

class Info:
  """
    Classe para controle de informações.
  """
  dados = {
    "H"  : [], # energia total
    "U"  : [], # energia potencial
    "P"  : [], # momento linear total
    "J"  : [], # momento angular total
    "Rcm": [], # centor de massas
    "I"  : [], # momento de inércia
    "C"  : [], # complexidade
  }

  eixos = ["x", "y", "z"]

  def __str__ (self)->str:
    string = ""
    for ind in self.dados:
      string += "\n\n" + 25*"-" + "\n" + ind
      # verifica se tem mais de uma dimensão
      if isinstance(self.dados[ind][0], list):
        dimensao = len(self.dados[ind][0])
        # separa as dimensões
        seps = list(zip(*self.dados[ind]))
        # percorre
        for i in range(dimensao):
          # dimensão
          dim = seps[i]
          # para exibir
          eixo = self.eixos[i]
          string += "\n" + eixo + "\n"
          # estatísticas
          media = mean(dim)
          desvio = stdev(dim)
          minimo, maximo = min(dim), max(dim)
          string += f"Média: {media} \nDP: {desvio} \nMínimo: {minimo} \nMáximo: {maximo}"
          string += "\n"

      else:
        # dados
        dados = self.dados[ind]
        # para exibir
        string += "\n"
        # estatísticas
        media = mean(dados)
        desvio = stdev(dados)
        minimo, maximo = min(dados), max(dados)
        string += f"Média: {media} \nDP: {desvio} \nMínimo: {minimo} \nMáximo: {maximo}"
        string += "\n\n"
    return string

def informacoes (m:list, Rs:list, Ps:list, exibir:bool=True)->dict:
  """
    Obtém as informações de um dado conjunto de posições 
    e momentos lineares.
  """
  infos = Info()
  mtot = sum(m)
  qntd = len(Rs)
  for i in range(qntd):
    R, P = Rs[i], Ps[i]

    # energia total
    infos.dados["H"] += [H(R, P, m)]
    
    # energia potencial
    infos.dados["U"] += [U(R, m)]

    # momento linear total
    infos.dados["P"] += [[sum(Pi) for Pi in list(zip(*P))]]

    # momento angular total
    infos.dados["J"] += [momentoAngular(R, P)]
    
    # centro de massas
    infos.dados["Rcm"] += [centro_massas(m, R)]

    # momento de inércia
    infos.dados["I"] += [momento_inercia_cm(m, R)]

    # complexidade
    infos.dados["C"] += [complexidade(infos.dados["I"][-1], mtot, infos.dados["U"][-1])]
  
  if exibir:
    print(infos)  

  return infos
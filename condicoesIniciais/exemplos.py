class CondicoesIniciaisExemplos:
  """
    Classe contendo alguns exemplos de condicoes iniciais para testes.
  """
  def gerar (self, nome:str)->list:
    """
      Parametros
      ----------
      nome : str
        Nome do exemplo o qual quer gerar as condicoes.  
    """
    # Condicoes iniciais de uma lemniscata com 3 corpos
    if nome == 'lemniscata':
      m = [1,1,1]
      R = [
        [-0.97000436, 0.24308753, 0],
        [0, 0, 0],
        [0.97000436, -0.24308753, 0]
      ]
      P = [
        [ 0.4662036850, 0.4323657300, 0],
        [-0.93240737, -0.86473146, 0],
        [ 0.4662036850, 0.4323657300, 0]
      ]
      G = 1
      return m, R, P, G
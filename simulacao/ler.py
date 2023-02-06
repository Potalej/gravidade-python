from config.configs import dados

def ler_arquivo (dir, dim=2):
  """Faz a leitura de um arquivo com as informações"""
  with open(dir, 'r') as arquivo:
    Ps, Rs = [], []
    arquivo = arquivo.read()
    partes = arquivo.split(dados['SEPARADOR'])
    
    massas = [float(massa) for massa in partes[0].split(',')]
    
    passos = partes[1].split('\n')

    # se quiser aumentar a velocidade, só colocar um [::x] aqui embaixo
    for posicao in passos:
      if posicao == '': break
      ps = [float(coord) for coord in posicao.split(',')]
      R = [[ps[i+2*j] for j in range(dim)] for i in range(0, len(ps), int(2*dim))]
      # P = [[ps[i+2*j+1] for j in range(dim)] for i in range(0, len(ps), int(2*dim))]
      Rs.append(R)
      # Ps.append(P)
    return massas, Rs, Ps
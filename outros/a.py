from datetime import datetime
from fortran.ler import *

DIVISOR_GRANDE = 53*'='
DIVISOR_PEQUENO = 26*'='

print(f"{DIVISOR_GRANDE} \n Leitura de arquivos gerados pelo gravidade-fortran \n{DIVISOR_GRANDE}\n")

dir = input('= Arquivo: \n> ')
if dir == "": dir = "20230324_10.csv"

print()

parcial_completo = input('= Quer ler por partes (0) ou completo (1)?')

if int(parcial_completo) == 1:
  massas, posicoes, momentos = ler_csv(dir)

  G = float(input('= Gravidade:\n> '))

  print(f"\n\n{DIVISOR_PEQUENO}\n\t Informações\n{DIVISOR_PEQUENO}\n")

  print("Quantidade de corpos:", len(massas))
  print("Quantidade de passos:", len(posicoes[0]))

  print(f'\n\n{DIVISOR_PEQUENO}\n\tEstatísticas\n{DIVISOR_PEQUENO}')

  estatisticas(massas, posicoes, momentos, G)

  data = datetime.now()
  print(data, '\n\n')

  while True:
    formato_visualizacao = int(input('= Deseja visualizar a simulação?\n1 - Trajetórias;\n2 - Evolução;\n3 - Salvar simulação;\n0 - Sair\n> '))
    if formato_visualizacao == 1:
      visualizar(posicoes)
    elif formato_visualizacao == 2:
      visualizar_tempo_real(posicoes)
    elif formato_visualizacao == 3:
      salvar_animacao(posicoes)
    print('\n\n')

else:
  tamanhoChunk = 5000
  pular = 100
  G = float(input('= Gravidade:\n> '))
  # captura o cabecalho
  massas, N = ler_csv_cabecalho(dir)
  # le os chunks
  chunk = 0
  for posicoes, momentos in ler_csv_chunks(dir, tamanhoChunk, N):
    chunk += 1
    print('chunk ', chunk)
    # calcula as estatisticas sem exibir
    infos = estatisticas(massas, posicoes, momentos, G, False, pular)
    
    for chave in infos:
      if chunk == 1: modo = 'w'
      else: modo = 'a'
      with open(chave + '.txt', modo) as arq:
        arq.write("\n" + '\n'.join(infos[chave]))
  print('ok')
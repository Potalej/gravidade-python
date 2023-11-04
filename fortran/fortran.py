from datetime import datetime
from fortran.ler import *

DIVISOR_GRANDE = 53*'='
DIVISOR_PEQUENO = 26*'='

print(f"{DIVISOR_GRANDE} \n Leitura de arquivos gerados pelo gravidade-fortran \n{DIVISOR_GRANDE}\n")

dir = input('= Arquivo: \n> ')
if dir == "": dir = "20230324_10.csv"

print()
massas, posicoes, momentos = ler_csv(dir)

G = float(input('= Gravidade:\n> '))

print(G)

print(f"\n\n{DIVISOR_PEQUENO}\n\t Informações\n{DIVISOR_PEQUENO}\n")

print("Quantidade de corpos:", len(massas))
print("Quantidade de passos:", len(posicoes[0]))

print(f'\n\n{DIVISOR_PEQUENO}\n\tEstatísticas\n{DIVISOR_PEQUENO}')

estatisticas(massas, posicoes, momentos, G)

data = datetime.now()
print(data, '\n\n')

formato_visualizacao = int(input('= Deseja visualizar a simulação?\n1 - Trajetórias;\n2 - Evolução;\n3 - Salvar simulação;\n0 - Sair\n> '))
if formato_visualizacao == 1:
  visualizar(posicoes)
elif formato_visualizacao == 2:
  visualizar_tempo_real(posicoes)
elif formato_visualizacao == 3:
  salvar_animacao(posicoes)
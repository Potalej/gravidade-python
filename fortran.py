from datetime import datetime
from fortran.ler import *


DIVISOR_GRANDE = 53*'='
DIVISOR_PEQUENO = 26*'='

print(f"{DIVISOR_GRANDE} \n Leitura de arquivos gerados pelo gravidade-fortran \n{DIVISOR_GRANDE}\n")

dir = input('= Arquivo: \n> ')
if dir == "": dir = "20230324_10.csv"

print()
massas, posicoes, momentos = ler_csv(dir)

print(f"\n\n{DIVISOR_PEQUENO}\n\t Informações\n{DIVISOR_PEQUENO}\n")

print("Quantidade de corpos:", len(massas))
print("Quantidade de passos:", len(posicoes[0]))

print(f'\n\n{DIVISOR_PEQUENO}\n\tEstatísticas\n{DIVISOR_PEQUENO}')

estatisticas(massas, posicoes, momentos)

data = datetime.now()
print(data, '\n\n')

visualizar(posicoes)
# visualizar_tempo_real(posicoes)
from auxiliares.auxiliares import momentos_angulares, tensor_inercia_geral, prodvetR3, momentoAngular
from auxiliares.hamiltoniano import EC, U, H
from numpy import matrix
from numpy.linalg import solve
from condicoesIniciais.condicoesArtigo import condicoesArtigo

massas = [100, 100, 80]
posicoes = [
  [100, 100, 100],
  [-100, -100, 0], 
  [-200, 200,0]
]
momentos = [
  [70, 0,0],
  [0, 30,10],
  [0,-5,-10]
]

# print(EC(momentos, massas), U(posicoes, massas))
# raise ValueError()

# def zerar_momento_angular (m, r, p):
#   """
#     Zera o momento angular do sistema.
#   """
#   # calcula todos os momentos angulares
#   Ja = momentos_angulares([], r, p)
#   # momento angular total
#   J = [ sum(Jax[i] for Jax in Ja) for i in range(3) ]
    
#   # tensor de inércia
#   I = tensor_inercia_geral(massas, r)
#   # vetor de rotação
#   omega = - solve(I, J)
#   # percorre os corpos
#   for a in range(len(m)):
#     # produto vetorial de ra por omega
#     ra_omega = list(prodvetR3(r[a], omega))
    
#     p[a] = [
#       p[a][i] + m[a]*ra_omega[i]
#       for i in range(3)
#     ]
  
#   # calcula o novo momento angular total
#   J = matrix(J) + (matrix(I) * matrix(omega).T).T
#   return r, p, J

# def zerar_energia_total (m, r, p, e=0):
#   ec = EC(p, m)
#   u = U(r, m)
#   fator = (-(u+e)/ec)**.5

#   for a in range(len(m)):
#     for i in range(3):
#       p[a][i] *= fator

#   return r, p, EC(p,m)+U(r,m)

# def Ptotal(Ps):
#   return [sum(p[0] for p in Ps),sum(p[1] for p in Ps),sum(p[2] for p in Ps)]

# def zerar_velocidade_centro_massas (massas, Ps):
#   mtot = sum(massas)
#   # calcula o momento
#   P = Ptotal(Ps)
#   # arruma as velocidades
#   Pk = [
#     [ Ps[a][i] - P[i]*massas[a]/mtot for i in range(3) ]
#     for a in range(len(massas))
#   ]
#   return Pk

# def rcm(massas, Rs):
#   mtot = sum(massas)
#   Rcm = [[
#     r[0]*massas[a],
#     r[1]*massas[a],
#     r[2]*massas[a]
#   ] for a,r in enumerate(Rs)]
#   return [sum(a)/mtot for a in list(zip(*Rcm))]


# def zerar_centro_massas(massas, Rs):
#   # calcula centro de massas
#   Rcm = rcm(massas, Rs)
#   # ajusta
#   Rs = [[
#     R[0] - Rcm[0],
#     R[1] - Rcm[1],
#     R[2] - Rcm[2],
#   ] for R in Rs]
#   return Rs


# posicoes, momentos, H_total = zerar_energia_total(massas, posicoes, momentos)
# momentos = zerar_velocidade_centro_massas(massas, momentos)
# print(posicoes)
# posicoes = zerar_centro_massas(massas, posicoes)
# posicoes, momentos, J = zerar_momento_angular(massas, posicoes, momentos)

# print(posicoes)
# print(massas)
# print(momentos) 

valoresIniciais = {
  'qntdCorpos': len(massas),
  'dimensao': len(posicoes[0]),
  'posicoes': posicoes,
  'momentos': momentos,
  'massas': massas
}

C = condicoesArtigo(valoresIniciais=valoresIniciais)

# print('momento angular total: ', J, momentoAngular(posicoes, momentos))
# print('energia total: ', H_total, H(posicoes, momentos, massas))
# print('centro de massas: ', rcm(massas, posicoes))

from simulacao.simulacao3d import Simulacao3D

S = Simulacao3D(massas, C.r, C.p, G=3)
# S.xlim = [-200,200]
# S.ylim = [-200,200]
# S.zlim = [-200,200]
from time import time
print()
t0 = time()
# print('CORREÇÃO MOMENTO ANGULAR')
S.simular(200, False, False)
print()
print('tempo: ', time() - t0)
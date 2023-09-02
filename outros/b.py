import matplotlib.pyplot as plt

arquivos = ['H', 'Jx', 'Jy', 'Jz', 'Px', 'Py', 'Pz', 'Rcmx', 'Rcmy', 'Rcmz']
for dir in arquivos:
  with open(dir + '.txt', 'r') as arq:
    valores = arq.read().split('\n')
    valores = [float(i) for i in valores if i != ""]
    plt.title(dir)
    plt.plot(valores)
    plt.show()
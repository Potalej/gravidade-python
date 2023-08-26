"""
  Configuracoes gerais do sistema

  Em vias de facilitar alteracoes, este arquivo centraliza todas as informacoes que 
  sao constantes pelo codigo.
"""

# QUANTIDADE DE INTEGRACOES POR PASSO
SIMULACAO_QNTD_INTEGRACOES_PASSO = 100

# DISTANCIA MINIMA PARA COLISAO
DIST_MIN_COLISAO = 1

# RANGE DE EXIBICAO DOS GRAFICOS
RANGE_PLOT_X = [-5000, 5000]
RANGE_PLOT_Y = [-5000, 5000]
RANGE_PLOT_Z = [-5000, 5000]

# INTERVALO DE PLOT DAS ANIMACOES
ANIMACAO_INTERVALO = 10

# DPI DAS ANIMACOES
ANIMACAO_DPI = 100

# TAMANHO DE RASTRO NAS ANIMACOES
TAMANHO_RASTRO_ANIMACOES = 0

# QUANTIDADE DE PONTOS GUARDADOS ANTES DE SALVAR
SIMULACAO_QNTD_SALVAR = 100

# SEPARADOR DOS ARQUIVOS
SEPARADOR_ARQUIVOS = "\n##########\n"

### Animação
animacao = {
    # tamanho da tela
    "LARGURA": 800,
    "ALTURA": 800,
    
    # densidade da tela. A tela terá "escala" * "tamanho" de pixels
    "ESCALA": 2,

    # densidade das partículas. As partículas terão raio "massa" / "densidade"
    # "DENSIDADE": particulas["DENSIDADE"],

    # cores das partículas (atualmente, lilás)
    "CORES": lambda qntd: [(150, 150, 255) for i in range(qntd)],

    # cor do fundo
    "FUNDO": (0,0,0),

    ## informações visuais
    # fonte
    "FONTE": "Verdana",
    "TAMANHO_FONTE": 18,
    "COR_FONTE": (255,255,255),
    
    # opções de exibição
    "EXIBIR_FPS": True,
    "EXIBIR_ENERGIA": True,

    # taxa de quadros por segundo (fps)
    "TAXA_ATUALIZACAO": 60,

    # quantidade de pontos guardados antes de salvar
    "QUANTIDADE_ANTES_SALVAR": 100
}

### Arquivo que armazena informações de simulação
dados = {
    # separador entre massa e corpos
    "SEPARADOR": "\n##########\n"
}
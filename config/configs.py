"""
    Configurações gerais do sistema

    Em vias de facilitar alterações, este arquivo centraliza todas as informações que 
    são constantes pelo código.
"""

### Partículas
particulas = {
    # "DENSIDADE": 30,
    # "DENSIDADE": 100000,
    "DENSIDADE": 10,
}

### Animação
animacao = {
    # tamanho da tela
    "LARGURA": 800,
    "ALTURA": 800,
    
    # densidade da tela. A tela terá "escala" * "tamanho" de pixels
    "ESCALA": 2,

    # densidade das partículas. As partículas terão raio "massa" / "densidade"
    "DENSIDADE": particulas["DENSIDADE"],

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
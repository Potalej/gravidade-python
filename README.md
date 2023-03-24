# 🪐gravidade-python🪐
Para simulações (mais ou menos) básicas de gravidade em Python.

Este repositório centraliza uma parte dos scripts que faço para praticar algumas coisas que tenho aprendido. É uma refatoração de uma primeira versão que já não está mais entre nós (ao menos de forma pública).

<img src="https://www.linux.ime.usp.br/~potalej/images/daora.gif" alt="Exemplo">

Meu estudo atualmente está seguindo através de um artigo publicado na _Physical Review Letters_ de autoria de Julian Barbour, Tim Koslowski e Flavio Mercati, chamado [Identification of a Gravitational Arrow of Time](https://physics.aps.org/featured-article-pdf/10.1103/PhysRevLett.113.181101). Este, porém, ainda é uma consequência de um artigo mais completo dos mesmos autores chamado [A Gravitational Origin of the Arrows of Time](https://arxiv.org/abs/1310.5167), que estou adentrando aos poucos.

Os autores se fundamentam na (e fundamentam a) Dinâmica de Formas - tradução provavelmente boco-moco para _Shape Dynamics_ -, "uma nova teoria de gravidade baseada em menos e mais fundamentais princípios que a Relatividade Geral", se baseando em algumas compreensões de Mach e Poincaré. O Mercati fez a gentileza de escrever um "tutorial" para isso, o [A Shape Dynamics Tutorial](https://arxiv.org/abs/1409.0105).

## Integração Numérica
Para resolver as equações diferenciais ordinárias (EDOs) que descrevem o comportamento mais básico dos corpos estou utilizando o [Método de Runge-Kutta](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods) em uma versão explícita e adaptada ao tipo de programa que está sendo feito, de modo a conseguir um desempenho melhor.

O Runge-Kutta pode assumir várias formas. Anteriormente, tinha feito numa forma geral que aceitava qualquer ordem e quaisquer matrizes via _tableau_. Devido a inutilidade dessa generalidade nesse caso, reescrevi de forma que se aplica o RK4. 

## Colisões
Na primeira versão desse sistema as coisas eram bidimensionais, então as singularidades (ou ao menos pseudo-colisões) ocorriam com uma frequência muito grande e desestabilizavam todo o sistema. A solução temporária adotada foi adicionar colisões, considerando corpos perfeitamente rígidos e atômicos dada uma densidade, e para os cálculos disso me baseei num excelente [vídeo do canal Reducible](https://youtu.be/eED4bSkYCB8), que por sua vez é baseado num pequeno [texto de Chad Berchek](https://www.vobarian.com/collisions/2dcollisions2.pdf). 

Ocorre que alterar a densidade de 1 para 1.1, por exemplo, seria o suficiente para diferir totalmente o desenvolvimento dos mais simples sistemas cujas condições iniciais fossem exatamente as mesmas. Ademais, o artigo em estudo não mencionava esse tipo de improvisação e as correções numéricas precisavam de adaptações confusas.

Assim, com o _advento_ das simulações tridimensionais o número de colisões e pseudocolisões reduz bastante, então as colisões elásticas foram apenas removidas e aceitamos, com certa angústia, que algumas coisas são como são (ou não?).

Ou apenas não sabemos corrigí-las ainda. Em breve descobrimos.

## Correções Numéricas
Além das imprecisões inevitáveis devido ao Python ser do jeito que é, há o erro natural cometido pelo método de integração em cada passo. Temos quatro simetrias/grandezas conservativas presentes no sistema: a energia total, o centro de massas, o momento linear (que é a velocidade do centro de massas) e o momento angular.

No antigo sistema bidimensional, antes das colisões, havíamos teorizado e aplicado a correção através da energia total, pois bastava utilizar seu gradiente. Agora são aplicadas as correções nas quatro simetrias, apesar de a correção da energia total ter problemas quando as partículas se aproximam.

## Animação
As animações 2D eram inicialmente feitas como um monte de plots do [Matplotlib](https://matplotlib.org/), o que era bastante ineficiente e pouco prático. Decidi então utilizar o [PyGame](https://www.pygame.org/news), já que por razões bastante óbvias desempenho é uma das preocupações dessa biblioteca.

Para as 3D, no momento tenho utilizado novamente o Matplotlib, já que a visualização é somente por curiosidade, pois o interesse agora é outro. A visualização gráfica das informações obtidas do sistema é feita também através do Matplotlib.

## Fortran
Para avançar nos estudos estou desenvolvendo uma [versão desse simulador em Fortran](https://github.com/Potalej/gravidade-fortran). Já tem funcionalidades básicas e consegue fazer simulações normalmente, mas devido a facilidade do Python em lidar com arquivos e visualizações, aqui foi adicionada, ao menos por ora, a possibilidade de ler os arquivos gerados pelo Fortran.

# Estimação do conteúdo de clorofila
Este repositório é destinado ao compartilhamento dos resultados experimentais obtidos na estimação do conteúdo de clorofila usando fotos de smartphone de folhas de mamão.

## Metodologia
Os passos do sistema desenvolvido podem ser visualizados na figura a seguir.

![methodology](https://github.com/esgario/chlestimator/blob/master/images/methodology.png)


### Métricas

Foram utilizadas um total de 27 métricas. Abaixo estão listadas todas as métricas utilizadas.

1. R
* G
* B
* H
* S
* L
* NR = R/(R+G+B)
* NG = G/(R+G+B)
* NB = B/(R+G+B)
* R-G
* R-B
* G-B
* G/R
* R/B
* G/B
* R-G/R+G
* R-B/R+B
* G-B/G+B
* R-G/R+G+B
* R-B/R+G+B
* G-B/R+G+B
* ExR = 1.4NR−NG
* ExG = 2NG-NR-NB
* ExB = 1.4NB-NG
* ExGR = ExG-ExR
* NGRDI = (NG-NR)/(NG+NR)
* DGCI = (Hue−60)/60 + (1−Sat) + (1−Brig)/3

### Dataset

Este dataset visa estimar o conteúdo de clorofila presente em folhas de mamão, por meio de fotos de smartphone. As medidas de referência apresentadas nesse dataset foram obtidas utilizando o dispostivo SPAD-502. Uma vez que o SPAD-502 é um equipamento confiável e amplamente utilizado na prática para coletar valores aproximados do conteúdo de clorofila em campo.

O desenvolvimento deste dataset foi estimulado pela seguinte hipótese:

     "Imagens de cameras RGB convencionais são suficientes para fazer uma estimativa precisa do conteúdo de clorofila em folhas de plantas."

#### Detalhes
Smartphone utilizado: Xiaomi Redmi S2
Total de imagens: 300
Tamanho das imagens: 1024x1024

Mamão golden:
	- 75 fotos com fundo natural
	- 75 fotos com fundo branco

Mamão tainung:
	- 75 fotos com fundo natural
	- 75 fotos com fundo branco

## Resultados experimentais

Os resultados de cada métrica foram comparados com os valores de clorofila medidos com o SPAD 502. Os resultados são apresentados em termos do coeficiente de determinação R² para as folhas de mamão golden (gp) e mamão tainung (tp).

### Imagens com fundo natural

![natural-bg-results](https://github.com/esgario/chlestimator/blob/master/images/natural-bg-results.png)

### Imagens com fundo branco

![white-bg-results](https://github.com/esgario/chlestimator/blob/master/images/white-bg-results.png)

# Processamento e análise de dados de precipitação oriundos de radar

## Justificativa

## Objetivos

## Resultados esperados

Espera-se o desenvolvimento de uma aplicação executável em windows que, a partir de comunicação com o usuário a partir de janela de comandos, estruturado conforme a Figura 1.

<table class="image">
<caption align="bottom">Figura 1 - Estruturação das funcionalidades do programa</caption>
<tr><td><img src="funcionalidades.png" alt="funcionalidades" width=500/>
</td></tr>
</table>

Desta forma, os dados necessários para entrada no programa (input) serão arquivos binários selecionados pelo usuário a partir de caixas de diálogo, já os dados de saída serão arquivos txt, gráficos e informações escritas. 

## Detalhamento das partes do programa

A entrega do projeto será feita em 3 etapas, primeiramente será entregue um protótipo capaz de fazer a leitura dos arquivos binários e conversão em arquivos de texto. Feito isso, o próximo protótipo agregará as funcionalidades de relatório de falhas e análise de consistência. Em seguida será entregue um proótipo com todas as funcionalidades, incluindo visualização dos dados.

#### a) Leitura de arquivos binários e conversão para txt

Para a entrada de dados, o usuário poderá selecionar os arquivos a serem adicionados ao programa a partir de caixa de diálogo. O resultado do programa será arquivos em txt no formato padrão de entrada no modelo hidrológico.

#### b) Relatório de falhas e análise de consistência

O usuário poderá escolher se o programa fará relatório de falhas e/ou preenchimento delas a partir de interpolação. Além disso, será possível escolher se será realizada a análise de consistência dos dados utilizando o método da dupla massa e o que acontecerá com os dados inconsistentes (retirada ou substituição por preenchimento de falhas).

### c) Visualização

Com o intuito de facilitar a visualização temporal e espacial das séries de dados, será possível plotar gráficos interativos (hidrogramas e mapas). 

## Metodologia de execução

O planejamento e gerenciamento das atividades do projeto ocorrerá utilizando [github](http://github.com/ewerton94/rain_consistency), [waffle](https://waffle.io/ewerton94/rain_consistency) e slack. O código aberto do programa poderá ser encontrado no github.

## Premissas e restrições

O time de densolvimento tem certa proximidade com o cliente, por isso espera-se que dúvidas levantadas sejam sanadas em até 3 dias. Para que as atividades possam ser realizadas no prazo, cada membro dedicará ao menos 4 horas semanais ao desenvolvimento da etapa de projeto.

## Cronograma

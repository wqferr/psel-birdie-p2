# Processo seletivo Birdie
As etapas do processo foram dividas em diretórios
numerados com respeito à ordem de execução.
Cada diretório com scripts python também possui
scripts shell que os executem com os argumentos corretos.
Também há notebooks jupyter em alguns passos.
Mais informações abaixo sobre cada passo.
## Passo a passo
### 1. Scraping
#### TL;DR
1. Rodar `collect_data.sh`
2. Saída no arquivo `products.tsv`

#### Detalhes
Para rodar a etapa de scraping por completo, basta executar o script shell `collect_data.sh`.
O arquivo de saída é `products.tsv`.

Para mais controle sobre o processo, os scripts `scrape.sh` e `group.sh` realizam, respectivamente, o scraping e o agrupamento dos dados no arquivo `products.tsv`.

O arquivo `categories.txt` contém a lista de categorias a serem buscadas. Para modificar a lista, basta adicionar ou remover linhas do arquivo. As categorias podem ser encontradas como a última parte do URL de busca do buscapé.
Por exemplo, no URL

    https://www.buscape.com.br/celular-e-smartphone
A categoria é `celular-e-smartphone`.

O argumento `-p` para o script `scrape.py` indica o número de páginas a serem raspadas por informações.
O script `scrape.sh` usa o valor `20`, mas pode ser editado facilmente para usar outro valor.

### 2. Classificação
#### TL;DR
1. Rodar notebook `create_model.ipynb`
2. Rodar `classify.sh`
3. Saída no arquivo `labeled_data.tsv`

#### Detalhes
O notebook `create_model.ipynb` mostra o processo de seleção do classificador,
bem como sua criação e seu treinamento sobre os dados coletados.

O modelo escolhido é o Bag of Words, e é serializado no arquivo `model.clf`.

Após a criação do modelo, o script `classify.sh` usa-o para classificar os dados de `products.tsv` no diretório do passo anterior. As entradas classificadas são salvas no arquivo `labeled_data.tsv`.

O threshold usado para classificação pode ser configurado como argumento do script `classify.py`. O script `classify.sh` usa o valor `0.25`, determinado informalmente e superficialmente. Novamente, esse valor pode ser editado diretamente no script shell.

As features extraídas para o uso dos classificadores Perceptron e Naive Bayes encontram-se no script `extract_features.py` como expressões regulares.

Mais informações sobre o processo de decisão podem ser encontradas no notebook `create_model.ipynb`.

### 3. Extração de features
#### TL;DR
1. Rodar `filter.sh`
2. Rodar notebook `extract_features.ipynb`
3. Saída no arquivo `features.tsv`

#### Detalhes
O script `filter.sh` seleciona apenas os produtos marcados com `SMARTPHONE` `True` do arquivo `labeled_data.tsv` do passo anterior.
Tais produtos são salvos no arquivo intermediário `smartphones.tsv`.

O notebook `extract_features.ipynb` utiliza as features definidas no script `smartphone_features.py`.

Os títulos, IDs e features extraídas dos produtos em `smartphones.tsv` são salvos em `features.tsv`. Valores desconhecidos são marcados com a string `N/A` na coluna correspondente.

### 4. Matching / Deduplicação
#### TL;DR
1. Rodar notebook `match_products.ipynb`
2. Saída no arquivo `matches.tsv`

#### Detalhes
O notebook define e descreve as funções e métodos usados para a deduplicação de produtos.

O arquivo `matches.tsv` contém apenas produtos considerados duplicados, com uma coluna a mais nomeada `UNCERTAINTY`.

A coluna `UNCERTAINTY` no arquivo de saída indica o número de campos `None` em uma das ou em ambas as instâncias comparadas.

Incluir uma métrica de incerteza permite que algorítmos mais à frente na pipeline possam configurar a qualidade vs quantidade de pares utilizados.

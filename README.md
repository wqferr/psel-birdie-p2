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
Para rodar a etapa de scraping por completo, basta executar o script shell `collect_data.sh`.
O arquivo de saída é `products.tsv`.

#### Avançado
Para mais controle sobre o processo, os scripts `scrape.sh` e `group.sh` realizam, respectivamente, o scraping e o agrupamento dos dados no arquivo `products.tsv`.

O arquivo `categories.txt` contém a lista de categorias a serem buscadas. Para modificar a lista, basta adicionar ou remover linhas do arquivo. As categorias podem ser encontradas como a última parte do URL de busca do buscapé.
Por exemplo, no URL

    https://www.buscape.com.br/celular-e-smartphone
A categoria é `celular-e-smartphone`.

O argumento `-p` para o script `scrape.py` indica o número de páginas a serem raspadas por informações.
O script `scrape.sh` usa o valor `20`, mas pode ser editado facilmente para usar outro valor.

### 2. Classificação
#### TL;DR
O notebook `create_model.ipynb` mostra o processo de seleção do classificador,
bem como sua criação e seu treinamento sobre os dados coletados.
O modelo escolhido é o Bag of Words, e é serializado no arquivo `model.clf`.

Após a criação do modelo, o script `classify.sh` usa-o para classificar os dados de `products.tsv` no diretório do passo anterior. As entradas classificadas são salvas no arquivo `labeled_data.tsv`.

#### Avançado
O threshold usado para classificação pode ser configurado como argumento do script `classify.py`. O script `classify.sh` usa o valor `0.25`, determinado informalmente e superficialmente. Novamente, esse valor pode ser editado diretamente no script shell.

As features extraídas para o uso dos classificadores Perceptron e Naive Bayes encontram-se no script `extract_features.py` como expressões regulares.

Mais informações sobre o processo de decisão podem ser encontradas no notebook `create_model.ipynb`.

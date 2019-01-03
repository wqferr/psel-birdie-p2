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
O script `scrape.sh` usa o valor 20, mas pode ser editado facilmente para usar outro valor.

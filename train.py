import numpy as np
import pandas as pd

#%%

def stratified_sample(df, col='CATEGORY', n_per_class=2):
    return df.groupby(col, group_keys=False).apply(
        lambda x: x.sample(min(len(x), n_per_class)))

#%% Carregamento do arquivo de treino

data = pd.read_csv('products.tsv', sep='\t')
data.set_index('ID', inplace=True)
data['SMARTPHONE'] = data.CATEGORY == 'celular-e-smartphone'

#%%

stratified_sample(data)

#%%

print('Frequência das primeiras palavras de cada produto categorizado ' +
        'como celular')
phone_titles = data[data.CATEGORY == 'celular-e-smartphone'].TITLE
first_words = phone_titles.apply(lambda t: t.split()[0])

first_words.value_counts()

#%%

clean_titles = phone_titles.apply(lambda t: ' '.join(t.split()[1:]))
smartphones = data[data.CATEGORY == 'celular-e-smartphone']
trimmed_smartphones_idx = smartphones.sample(frac=0.6).index
data.loc[trimmed_smartphones_idx, 'TITLE'] = clean_titles

#%%

data[data.CATEGORY == 'celular-e-smartphone'].sample(10)

#%%

import re

patterns = [
    r'smart', # contém "smart"
    r'(?:ph|f)one', # contém "fone" ou "phone"
    r'\bcelular\b', # contém a palavra "celular"
    r'\b[a-z]\d\b', # contém, p.e., "G5", "S9", ...
    r'\b(?:capa|case)\b', # contém a palavra "capa" ou "case"
    r'\bpara\b', # contém a palavra "para" (p.e. "antena para celular")
    r'\d+ ?GB', # contém algo que se pareça com uma quantidade de memória
    r'(?:plus|\+)\b' # contém uma palavra que termine com "plus" ou "+"
]

patterns_re = [re.compile(pat, re.IGNORECASE) for pat in patterns]

# Usado para nomear as colunas do DataFrame
attr_names = [
    'smart', 'phone', 'celular',
    'letra_num', 'capa', 'para',
    'mem', 'plus']

attr_col_names = [f're_{col}' for col in attr_names]

#%%

# Transforma um título em uma lista de atributos
def get_attributes(title):
    title_attributes = []
    for pattern in patterns_re:
        if pattern.search(title) is None:
            title_attributes.append(0)
        else:
            title_attributes.append(1)
    return title_attributes

#%%

# Transforma as linhas de um DataFrame nos atributos correspondentes ao título
def get_row_attributes(dataframe):
    attributes = []
    for i in dataframe.index:
        row_attr = get_attributes(dataframe.loc[i].TITLE)
        attributes.append(row_attr)
    attr_df = pd.DataFrame(attributes)
    attr_df.columns = attr_col_names

    res_df = dataframe.copy()
    for col in attr_df:
        res_df.insert(len(res_df.columns), col, attr_df[col])
    return res_df

#%%

features = get_row_attributes(data)

#%%

stratified_sample(features[features.re_plus == 1])

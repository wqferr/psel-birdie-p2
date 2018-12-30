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

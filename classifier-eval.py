import numpy as np
import pandas as pd

#%%

def stratified_sample(df, col='CATEGORY', n_per_class=2):
    return df.groupby(col, group_keys=False).apply(
        lambda x: x.sample(min(len(x), n_per_class)))

#%% Carregamento do arquivo de treino

data = pd.read_csv('products.tsv', sep='\t')
data.set_index('ID', inplace=True)
data['SMARTPHONE'] = (data.CATEGORY == 'celular-e-smartphone').astype(int)

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
    'mem', 'plus'
]

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

clf_features = features[attr_col_names + ['SMARTPHONE']]
stratified_sample(clf_features, col='SMARTPHONE', n_per_class=5)

#%%

stratified_sample(features)

#%%

from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import BernoulliNB

from sklearn.model_selection import cross_val_score

#%%

perceptron = Perceptron(alpha=0.05, max_iter=1e4)
naive_bayes = BernoulliNB(binarize=None)

#%%

X = clf_features[attr_col_names].values
y = clf_features['SMARTPHONE'].values

# %%

def eval_model(model):
    return cross_val_score(model, X, y, scoring='roc_auc', cv=10)

def print_results(name, cv_score):
    print(name)
    print(f'{np.mean(cv_score):.3f} +- {np.std(cv_score):.3f}')
    return # Syntax highlighting do atom quebra sem isso

# %%

perceptron_res = eval_model(perceptron)
naive_bayes_res = eval_model(naive_bayes)

# %%

print_results('Perceptron', perceptron_res)
print()
print_results('Naive Bayes', naive_bayes_res)

#%%

from scipy.stats import ttest_ind

test_result = ttest_ind(perceptron_res, naive_bayes_res)
print(f'p-value: {test_result.pvalue:.3f}')
if test_result.pvalue < 0.05:
    print(f'Classificadores com desempenho diferentes')
else:
    print(f'Não há evidências de que os classificadores tenham desempenhos diferentes')

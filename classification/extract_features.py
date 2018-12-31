import re
import pandas as pd

_patterns = [
    r'smart', # contém "smart"
    r'(?:ph|f)one', # contém "fone" ou "phone"
    r'\bcelular\b', # contém a palavra "celular"
    r'[a-z]+\d+', # contém, p.e., "G5", "S9", ...
    r'\b(?:capa|case)\b', # contém a palavra "capa" ou "case"
    r'\bpara\b', # contém a palavra "para" (p.e. "antena para celular")
    r'pel[íi]cula', # contém "película"
    r'(?:plus|\+)\b', # contém uma palavra que termine com "plus" ou "+"
    r'chip\b', # contém uma palavra que termine com "chip",
    r'MP\b' # contém abreviação de megapixels
]

_patterns_re = [re.compile(pat, re.IGNORECASE) for pat in _patterns]

# Usado para nomear as colunas do DataFrame
attr_names = [
    'smart',
    'phone',
    'celular',
    'letra_num',
    'capa',
    'para',
    'pelicula',
    'plus',
    'chip',
    'MP'
]

attr_col_names = [f're_{col}' for col in attr_names]

# Transforma um título em uma lista de atributos
def _get_attributes(title):
    title_attributes = []
    for pattern in _patterns_re:
        if pattern.search(title) is None:
            title_attributes.append(0)
        else:
            title_attributes.append(1)
    return title_attributes


# Transforma as linhas de um DataFrame nos atributos correspondentes ao título
def get_df_attributes(dataframe):
    attributes = []
    for i in dataframe.index:
        row_attr = _get_attributes(dataframe.loc[i].TITLE)
        attributes.append(row_attr)
    attr_df = pd.DataFrame(attributes)
    attr_df.columns = attr_col_names

    res_df = dataframe.copy()
    for col in attr_df:
        res_df.insert(len(res_df.columns), col, attr_df[col])
    return res_df


def get_attr_X(attr_df):
    return attr_df[attr_col_names]

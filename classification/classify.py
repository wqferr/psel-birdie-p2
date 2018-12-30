import pandas as pd
import numpy as np

from extract_features import get_df_attributes, get_attr_X
from sklearn.linear_model import Perceptron


def read_data(filename, clean_frac=0.6):
    data = pd.read_csv(filename, sep='\t')
    data['ORIGINAL_TITLE'] = data.TITLE
    if 'CATEGORY' in data.columns:
        smartphones_idx = data.CATEGORY == 'celular-e-smartphone'
    else:
        lowercase_titles = data.TITLE.str.lower()
        smartphones_idx = lowercase_titles.str.startswith('celular')
        smartphones_idx |= lowercase_titles.str.startswith('smartphone')

    phone_titles = data.loc[smartphones_idx, 'TITLE']

    smartphones = data[smartphones_idx]
    trimmed_smartphones_idx = smartphones.sample(frac=clean_frac).index
    clean_titles = phone_titles[trimmed_smartphones_idx].apply(
        lambda t: ' '.join(t.split()[1:])
    )
    data.loc[trimmed_smartphones_idx, 'TITLE'] = clean_titles
    return data

if __name__ == '__main__':
    perceptron = Perceptron(max_iter=1e4)
    train_data = read_data('products.tsv')
    train_attr = get_df_attributes(train_data)
    train_X = get_attr_X(train_attr)
    train_y = train_attr.CATEGORY == 'celular-e-smartphone'

    data = read_data('data_estag_ds.tsv')
    data_attr = get_df_attributes(data)
    X = get_attr_X(data_attr)

    perceptron.fit(train_X, train_y)
    predicted_labels = perceptron.predict(X)
    output = data.copy()
    output['SMARTPHONE'] = predicted_labels

    output.TITLE = output.ORIGINAL_TITLE
    output.drop('ORIGINAL_TITLE', axis=1, inplace=True)

    output.to_csv('output.tsv', sep='\t', index=False)

import pandas as pd
import pickle

from extract_features import get_df_attributes, get_attr_X

from sys import argv


def read_data(filename, clean_frac=0.0):
    data = pd.read_csv(filename, sep='\t')
    data['ORIGINAL_TITLE'] = data.TITLE

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


def main():
    threshold = float(argv[1])

    with open('model.clf', 'rb') as f:
        model = pickle.load(f)

    data = read_data('../data_estag_ds.tsv')
    data_attr = get_df_attributes(data)
    X = get_attr_X(data_attr)

    probas = model.predict_proba(X)[:, 1]
    prediction = probas > threshold

    output = data.copy()
    output['SMARTPHONE'] = prediction

    # output.TITLE = output.ORIGINAL_TITLE
    output.drop('ORIGINAL_TITLE', axis=1, inplace=True)

    output.to_csv('labeled_data.tsv', sep='\t', index=False)


if __name__ == '__main__':
    main()

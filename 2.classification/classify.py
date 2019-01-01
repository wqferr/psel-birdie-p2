import pandas as pd
import pickle

from sys import argv


def main():
    threshold = float(argv[1])

    with open('model.clf', 'rb') as f:
        model = pickle.load(f)

    data = pd.read_csv('../data_estag_ds.tsv', sep='\t')
    X = data.TITLE

    probas = model.predict_proba(X)[:, 1]
    prediction = probas > threshold

    output = data.copy()
    output['SMARTPHONE'] = prediction

    output.to_csv('labeled_data.tsv', sep='\t', index=False)


if __name__ == '__main__':
    main()

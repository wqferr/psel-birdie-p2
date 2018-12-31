'''
Usage:
    filter_smartphones <products_file> <output_file>
'''

import pandas as pd
from docopt import docopt


def main():
    args = docopt(__doc__)
    labeled_products_path = args['<products_file>']
    output_path = args['<output_file>']
    data = pd.read_csv(labeled_products_path, sep='\t')
    data.set_index('ID', inplace=True)
    smartphones = data[data.SMARTPHONE]
    smartphones = data[['TITLE']]
    smartphones.to_csv(output_path, sep='\t')


if __name__ == '__main__':
    main()

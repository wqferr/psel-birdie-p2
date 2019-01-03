'''
Usage:
    group <input_dir> <output_file> [--index]
'''


import pandas as pd

from docopt import docopt
from glob import glob
from os.path import join as path_join


def main():
    args = docopt(__doc__)
    in_dir = args['<input_dir>']
    in_files = glob(path_join(in_dir, '*.json'))
    out_file = args['<output_file>']

    tables = [pd.read_json(filename) for filename in in_files]
    full_table = pd.concat(tables, ignore_index=True)
    full_table.index.name = 'ID'

    full_table.to_csv(out_file, sep='\t')


if __name__ == '__main__':
    main()

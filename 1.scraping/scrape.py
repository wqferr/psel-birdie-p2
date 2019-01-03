'''
Usage:
    scrape [options] [--] <spider_name> [- <cat_list_file> | <categories>...]

Options:
    -c              Clear output dir before running
    -o <outdir>     Path to output directory
    -p <pages>      Number of pages to scrap
'''

from docopt import docopt
from subprocess import Popen
from os import remove
from os.path import join as path_join
from glob import glob
from time import sleep


def main():
    args = docopt(__doc__)
    spider_name = args['<spider_name>']
    categories = get_categories(args)
    n_pages = args['-p'] or 20
    out_path = args['-o'] or './out/'

    if args['-c']:
        clear_out_dir(out_path)

    pool = []
    for category in categories:
        process = Popen(
            f'scrapy crawl {spider_name} -a n_pages={n_pages} '
            + f'-a category={category} -o {path_join(out_path, category)}.json'
        )
        pool.append(process)

    while pool:
        pool = list(filter(process_not_done, pool))
        sleep(2)


def clear_out_dir(out_path):
    for filename in glob(f'{path_join(out_path, "*")}'):
        remove(filename)


def get_categories(args):
    category_file_path = args['<cat_list_file>']
    return args['<categories>'] or read_file(category_file_path)


def read_file(file_path):
    with open(file_path, 'r') as f:
        return [category.strip() for category in f.readlines()]


def process_not_done(proc):
    return proc.poll() is None


if __name__ == '__main__':
    main()

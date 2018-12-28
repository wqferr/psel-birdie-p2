'''
Usage:
    scrape [options] [--] <spider_name> <categories>...

Options:
    -o <outdir>     Path to output directory
    -p <pages>      Number of pages to scrap
    -s <suffix>     URL suffix
'''

from docopt import docopt
from subprocess import Popen, call
from os.path import join as path_join
from time import sleep


def main():
    args = docopt(__doc__)
    spider_name = args['<spider_name>']
    categories = args['<categories>']
    n_pages = args['-p'] or 20
    out_path = args['-o'] or './out/'

    pool = []
    for category in categories:
        process = Popen(f'scrapy crawl {spider_name} -a n_pages={n_pages} ' +
            f'-a category={category} -o {path_join(out_path, category)}.json')
        pool.append(process)

    while pool:
        pool = list(filter(process_not_done, pool))
        sleep(2)


def process_not_done(proc):
    return proc.poll() is None


if __name__ == '__main__':
    main()

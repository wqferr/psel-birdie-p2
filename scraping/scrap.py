'''
Usage:
    scrap [options] [--] <spider_name>

Options:
    -o <out>      File to append with results
    -p <pages>    Number of pages to scrap
'''

from docopt import docopt
from subprocess import call


def main():
    args = docopt(__doc__)
    spider_name = args['<spider_name>']
    n_pages = args['-p'] or 20
    out_path = args['-o'] or 'out.json'

    call(f'scrapy crawl {spider_name} -a n_pages={n_pages} -o {out_path}')


if __name__ == '__main__':
    main()
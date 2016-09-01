
#############################
#   Santiago Larrain        #
#   slarrain@uchicago.edu   #
#   @slarrain               #
#############################
#
# Small script that adds the
# comuna code to the svg file.
# It uses the clcomuna package
#

import clcomuna
import argparse
from bs4 import BeautifulSoup as bf4

def load_file(filename):
    svg = open(filename, 'r').read()
    return svg

def parse_svg (svg):
    '''
    Beautiful Soup in action
    '''
    soup = bf4(svg, "xml", selfClosingTags=['defs'])
    paths = soup.findAll('path')
    return paths, soup

def add_code(paths, args):
    for p in paths:
        name = p['id']
        if args.threshold:
            cod = clcomuna.get_steps(name, True, int(args.threshold))
            if cod:
                p['cod'] = str(cod)
        else:
            cod = clcomuna.get_steps(name, True)
            p['cod'] = str(cod)

def save(soup, name):
    '''
    Saves the SVG file
    '''
    with open(name, 'w') as f:
        f.write(soup.prettify())

def main(args):
    svg = load_file(args.input_SVG)
    paths, soup = parse_svg(svg)
    add_code(paths, args)
    save(soup, args.output_SVG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adds code to comunas SVG files')
    parser.add_argument('input_SVG', type=str, help='the filename of the SVG input file')
    parser.add_argument('output_SVG', type=str, help='the filename of the SVG output file')
    parser.add_argument('-t', '--threshold', type=int, help='Threshold for the fuzzy get comunas')
    args = parser.parse_args()
    main(args)

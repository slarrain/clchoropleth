#############################
#   Santiago Larrain        #
#   slarrain@uchicago.edu   #
#   @slarrain               #
#############################

from bs4 import BeautifulSoup
import pandas as pd
from clchoropleth.add_comuna_code_to_svg import load_file, parse_svg, save
import clcomuna

orange = ['#feedde','#fdbe85','#fd8d3c','#e6550d','#a63603']
blue = ['#eff3ff','#bdd7e7','#6baed6','#3182bd','#08519c']
green = ['#edf8e9','#bae4b3','#74c476','#31a354','#006d2c']
red = ['#fee5d9','#fcae91','#fb6a4a','#de2d26','#a50f15']
purple = ['#f2f0f7','#cbc9e2','#9e9ac8','#756bb1','#54278f']

colors5 = {'orange': orange, 'blue': blue,
            'green': green, 'red': red, 'purple': purple}

def prepare_data(data, t=70, noNone=False):
    '''
    If its a dictionary, it turns it into a pd.Series
    If it has several version of a comuna (e.g. "Calera" and "La Calera"), it
    uniforms the data under the same code.
    If noNone=True, it drops the 'None' values (e.g. a Comuna was below the threshold)
    '''
    if type(data) == dict:
        data = pd.Series(data)
    if type(data) == pd.Series:
        new_data = {}
        for comuna in data.index:
            name = clcomuna.get_steps(comuna, True, t)
            new_data[name] = new_data.get(name, 0) + data[comuna]
        new_data = pd.Series(new_data)
        if noNone:
            new_data = new_data.drop(None)
        return new_data
    else:
        print ("Invalid Argument: Argument needs to be a pandas.Series or a dictionary")

def select_comunas_from_region (data, region):
    '''
    Given the hole dataset and a region number, returns a subset with only the
    comunas from that region number
    '''
    assert isinstance (region, str), ('"region" parameter needs to a "string"')
    all_comunas = list(data.index)
    comunas = []
    for comuna in all_comunas:
        if comuna.startswith(region):
            comunas.append(comuna)
    return data[comunas]

def discretize(data, bins=5, quantile=False):
    '''
    Creates 'bins' number of bins and discretizes the data.
    Uses cut function by default. qcut function otherwise.
    '''
    if quantile:
        new_data = pd.qcut(data, bins, labels=list(range(bins)))
    else:
        new_data = pd.cut(data, bins, labels=list(range(bins)))
    return new_data

def fill_color(tag, color):
    '''
    Adds the color to the comuna
    '''
    seq = "fill:"
    color_length = 7
    index = tag.find(seq)+len(seq)
    return tag[:index] + color + tag [index+color_length:]


def make_map(data, filename, region, colors='orange'):
    '''It creates the choropleth map and saves it to filename destination.

    Args:
        data: The pd.Series with the data. The index needs to be the code and
            the value the bin number.
        filename: The filename of the map we are going to save.
        region: we need to specify the region again, as a string ("09"), to open
            the original svg file and modify it.
        colors: it can be a string, if is one of the 5 pre-set color lists:
            orange, blue, green, red, pruple. Or it can be a list of strings, with
            each string being a color. For example:
            ['#ffffcc','#c2e699','#78c679','#31a354','#006837']
            It needs to have the same length as the number of bins.
            For more colors: http://colorbrewer2.org/

    Returns:
        It saves the map. No return valule.
    '''
    assert isinstance (region, str), ('"region" parameter needs to a "string"')
    svg = load_file('svgs/'+region+'.svg')
    paths, soup = parse_svg(svg)
    if type(colors) == str:
        colors = colors5[colors]
    assert len(colors)>=len(data.unique())  #Number of colors musn't be less than
                                            # the number of bins
    for p in paths:
        if 'cod' in p.attrs:
            cod = p['cod']
            if cod not in data:
                print ("Warning: There was a comuna code in the SVG file not present on the dataset:", cod)
            else:
                color = colors[data[cod]]
                p['style'] = fill_color(p['style'], color)
    save(soup, filename)



def run(data, filename, region, colors='orange', bins=5, quantile=False):
    '''
    Wrapper function that runs all other functions
    '''
    make_map(discretize(select_comunas_from_region(data, region), bins, quantile), filename, region, colors)

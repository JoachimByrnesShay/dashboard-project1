""" from pygal documentation, import Style allows to define custom styles for the below chart attributes """
from pygal.style import Style

barchart_style = Style(
    background='#EDDCD2',
    plot_background='#EAFBFB',
    foreground='#370617',
    foreground_srrong='#FFFFFF',
    foreground_subtle='#000000',
    opacity='1',
    opacity_hover='0.3',
    title_font_size=30,
    transition='400ms ease-in')

piechart_style = Style(
    background='#343A40',
    plot_background="#FEFFE9",
    foreground='#FFFFFF',
    foreground_strong='#FFFFFF',
    foreground_subtle='#000000',
    opacity='1',
    opacity_hover='1',
    title_font_size=24,
    transition='400ms ease-in')
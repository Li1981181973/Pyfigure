from .handle import *
from .scatter import *
from .sline import *
from .hyplot import *

def set_fig_size(fig_size:list=[8, 4.5]):
    """
    设置图的大小
    """
    handle.rc['figure.figsize'] = fig_size

def set_font_size(font_size:float=10):
    """
    设置字体大小
    """
    handle.rc['font.size'] = font_size

def set_fig_dpi(dpi:float=330):
    """
    设置图的dpi
    """
    handle.rc['figure.dpi'] = dpi

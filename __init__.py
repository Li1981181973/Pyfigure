from .handle import *
from .scatter import *
from .sline import *
from .mline import *
from .hyplot import *
from matplotlib import cm

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

def brewer_colors(n, palette='plasma'):
    """
    获取 brewer 颜色
    """
    cmap = plt.cm.get_cmap(palette)
    if n <= cmap.N:
        return cmap(np.arange(n))
    else:
        # 超出颜色数量，循环使用
        # 循环使用颜色，但是要保证前面重复的颜色有个随机扰动
        # 先获取完整的颜色序列
        indices = np.tile(np.arange(cmap.N), (n // cmap.N) + 1)[:n]
        # 对前面重复的颜色添加随机扰动
        for i in range(cmap.N):
            indices[indices == i] += np.random.uniform(-0.2, 0.2, size=(indices[indices == i].shape[0],))
        return cmap(indices)
# 获取离散颜色    
def get_discrete_colors(n):
    """
    获取离散颜色
    """
    if n <= 10:
       cmp = plt.cm.get_cmap('tab10')
       return cmp(np.arange(n))
    elif n<=20:
        cmp = plt.cm.get_cmap('tab20')
        return cmp(np.arange(n))
    else:
        cmp = plt.cm.get_cmap('tab20b')
        color_sequence = [cmp(i % cmp.N) for i in range(n)]
        return color_sequence

# 获取连续颜色
def get_continuous_colors(n, palette='plasma'):
    """
    获取连续颜色
    """
    cmap = plt.cm.get_cmap(palette)
    return cmap(np.linspace(0, 1, n))

def get_colors(n, palette='plasma'):
    """
    获取颜色
    """
    if n <= 20:
        return get_discrete_colors(n)
    else:
        return get_continuous_colors(n, palette)
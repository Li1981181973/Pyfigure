import math
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import List
rc = {
        "font.family":'serif',
        "mathtext.fontset":'stix',
        "font.serif": ['Times New Roman','SimSun'],
        'axes.unicode_minus' : True,
        #'font.serif': 'Times New Roman',
        #'mathtext.fontset': 'stix',
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'axes.titlesize': 20,
        'font.size': 20,
        'lines.linewidth': 1.5,
        'figure.figsize': [10,6.18],
        'figure.dpi': 330,
      }
preferred_step = [1, 2, 3, 4, 5] # 优先使用的步长前缀列表
#计算轴的标签
def calculate_ticks(ticks_min: float, ticks_max: float, axis: str = 'x', count: int = 5,type:str = '')->List[float]:
    
    step_len = abs((ticks_max - ticks_min) / float(count - 1))
    step_len, power = power_scale(step_len)
    suffix = min(preferred_step, key=lambda i: abs(i - step_len))
    step_len = suffix * 10 ** power
    ticks = []
    if axis == 'x':
        if type is not None and type == 'terminal':
            start_tick = math.ceil(ticks_min/step_len)*step_len
            ticks.append(ticks_min)
            while start_tick < ticks_max:
                ticks.append(start_tick)
                start_tick += step_len
            ticks.append(ticks_max)
        if type is not None and type == 'auto':
            start_tick = math.floor(ticks_min/step_len)*step_len
            # if abs(start_tick-ticks_min) >= 0.5* step_len:
            #     ticks.append(start_tick-step_len*0.5)
            while start_tick < ticks_max:
                ticks.append(start_tick)
                start_tick += step_len
            # if abs(ticks_max-ticks[-1]) >= 0.5* step_len:
            #     ticks.append(start_tick-step_len*0.5)
    if axis == 'y':
        if type is not None:
            #对称
            if type == 'sys':
                if ticks_max * ticks_min > 0:
                    type = 'auto'
                else:
                    end_tick = math.ceil(max(abs(ticks_min),abs(ticks_max))/step_len)*step_len
                    start_tick = 0
                    while start_tick <= end_tick:
                        ticks.append(start_tick)
                        start_tick += step_len
                    start_tick = -end_tick
                    while start_tick < 0:
                        ticks.append(start_tick)
                        start_tick += step_len
                    ticks.sort()
            if type == 'terminal':
                start_tick = math.ceil(ticks_min/step_len)*step_len
                ticks.append(ticks_min)
                while start_tick < ticks_max:
                    ticks.append(start_tick)
                    start_tick += step_len
                ticks.append(ticks_max)
            start_tick = math.floor(ticks_min/step_len)*step_len
            end_tick = math.ceil(ticks_max/step_len)*step_len
            if type == 'auto':
                while start_tick < end_tick:
                    ticks.append(start_tick)
                    start_tick += step_len
                ticks.append(end_tick)
            
    return ticks
#考虑数据绘制区域的边界计算方法
def calculate_limits(data,region_ratio: float =0.8,_min= None,_max =None)->tuple[float,float]:
    min_data = np.min(data)
    max_data = np.max(data)
    #当值为0时，调整边界
    if min_data == 0:
        min_data = min_data-0.05*(max_data-min_data)
    if max_data == 0:
        max_data = max_data+0.05*(max_data-min_data)
    max_t = max(max_data,np.quantile(data, 0.9)/region_ratio) 
    min_t = min(min_data,np.quantile(data, 0.1)/region_ratio)
    if _max is not None and _max > max_t:
        max_t = _max
    if _min is not None and _min < min_t:
        min_t = _min
    return min_t,max_t

def power_scale(a:float)->tuple[float,int]:
    power = 0
    if a < 0:
        a = -a
        power = 1
    if a == 0:
        return 0,1
    while a > 1.0:
        a /= 10
        power += 1
    while a < 1.0:
        a *= 10
        power -= 1
    return a, power

def plot_marker_lines(ax, value: float, **options):
    axis_type = options.get('axis', 'x')
    ylims = ax.get_ylim()
    xlims = ax.get_xlim()
    if axis_type == 'x':
        if 1.05 * xlims[0] - 0.05 * xlims[1] < value < 0.95 * xlims[1] + 0.05 * xlims[0]:
            line = ax.axvline(value)
            line.set_color(options['color'])
            line.set_linewidth(options['width'])
            line.set_linestyle(options['style'])
            txt = options.pop('txt',None)
            if txt and txt.strip():
                ax.text(value ,1.01*ylims[1]-0.01*ylims[0] ,txt, horizontalalignment='center',
                        verticalalignment='bottom',fontname='SimSun',fontsize = 10)
    if axis_type == 'y':
        if 1.05 * ylims[0] - 0.05 * ylims[1] < value < 0.95 * ylims[1] + 0.05 * ylims[0]:
            line = ax.axhline(value)
            line.set_color(options['color'])
            line.set_linewidth(options['width'])
            line.set_linestyle(options['style'])
            txt = options.pop('txt',None)
            if txt and txt.strip():
                ax.text(0.99*xlims[1]+0.01*xlims[0],value ,txt, horizontalalignment='right',
                        verticalalignment='bottom',fontname='SimSun',fontsize = 10)
                

def get_options_single(**option)->dict:
    options = option.copy()
    options['xname'] = option.get('xname','axis_x')
    options['yname'] = option.get('yname','axis_y')
    options['xunit'] = option.get('xunit','')
    options['yunit'] = option.get('yunit','')
    options['xtick'] = option.get('xtick',{})
    options['ytick'] = option.get('ytick',{})
    options['colors'] = option.get('colors',[])
    options['markers'] = option.get('markers',[])
    options['legend'] = option.get('legend',{})
    options['grid_on'] = option.get('grid_on',False)
    options['styles'] = option.get('styles',[])
    options['xlines'] = option.get('xlines',[])
    options['ylines'] = option.get('ylines',[])
    options['widths'] = option.get('widths',[])
    return options
def get_options_multify(**option)->dict:
    options = option.copy()
    options['xname'] = option.get('xname','axis_x')
    options['ynames'] = option.get('ynames','axis_y')
    options['xunit'] = option.get('xunit','')
    options['yunits'] = option.get('yunits','')
    options['xticks'] = option.get('xticks',{})
    options['yticks'] = option.get('yticks',{})
    options['colors'] = option.get('colors',[])
    options['markers'] = option.get('markers',[])
    options['legend'] = option.get('legend',{})
    options['grid_on'] = option.get('grid_on',False)
    options['styles'] = option.get('styles',[])
    options['xlines'] = option.get('xlines',[])
    options['ylines'] = option.get('ylines',[])
    options['widths'] = option.get('widths',[])
    return options

def remove_mask_ticks(ticks:list,ax:Axes,fig:Figure,type ='x'):
    if len(ticks)<4:
        return ticks,ticks[1]- ticks[0]
    ticks_range = ticks[-1]-ticks[0]
    first_tick_factor = (ticks[1]- ticks[0])/ticks_range
    last_tick_factor = (ticks[-1]- ticks[-2])/ticks_range
    ticks_len = ticks[2]-ticks[1]
    if ax:
        # 重新计算每点对应的数据单位
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        axis_len:float =  bbox.width
        font_size:float = rc['font.size']/72.0
        if type == 'y':
            axis_len = bbox.height
        if type == 'x':
            font_size *=0.8
        first_tick_len = first_tick_factor*bbox.width
        last_tick_len = last_tick_factor*bbox.width
        
        first_tick_digit = (power_scale(ticks[1])[1]+power_scale(ticks[0])[1])/2*font_size
        last_tick_digit = (power_scale(ticks[-1])[1]+power_scale(ticks[-2])[1])/2*font_size
        if type == 'y':
            first_tick_digit = font_size
            last_tick_digit = font_size
        if first_tick_digit > first_tick_len:
            ticks.remove(ticks[1])
        if last_tick_digit > last_tick_len:
            ticks.remove(ticks[-2])
        return ticks,ticks_len
import matplotlib.pylab as plt
if __name__ == '__main__':
    x = np.arange(200)
    ticks = [0,50,100,150,200]
    y = np.sin(2*np.pi*x/20)
    fig= plt.figure(figsize=[20,10])
    plt.plot(x,y)
    remove_mask_ticks(ticks=ticks,ax = fig.gca(),fig=fig)
    plt.show()
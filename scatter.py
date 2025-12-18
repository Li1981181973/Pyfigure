from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
from . import handle

def figure_scatter(x,*y_data,**options):
    if y_data is None:
        return
    x_name = options.get('xName','x')
    y_name = options.get('yName','y')
    x_unit = options.get('xUnit','')
    y_unit = options.get('yUnit','')

    xtick: dict = options.get('xtick',{})
    ytick: dict = options.get('ytick',{})

    xtick_type:str = xtick.pop('type','terminal')
    ytick_type:str = ytick.pop('type','auto')

    # ticks type parser
    xtick_region = xtick.pop('region',1.0)
    ytick_region = ytick.pop('region',0.8)
    xtick_count = xtick.pop('count',8)
    ytick_count = ytick.pop('count',5)
    xtick_digit:int = xtick.pop('digit',-1)
    ytick_digit:int = ytick.pop('digit',-1)
    if not xtick_type in ['terminal','auto','manual']:
        xtick_type = 'terminal'
    if not ytick_type in ['terminal','auto','manual']:
        ytick_type = 'auto'
    if xtick_type == 'manual' and len(xtick.get('ticks',[])) == 0:
        xtick_type = 'terminal'
    if ytick_type == 'manual' and len(ytick.get('ticks',[])) == 0:
        ytick_type = 'auto'

    output = options.pop('outputPath','')
    colors = options.pop('colors',[])
    markers = options.pop('markers',[])
    legend: dict = options.pop('legend',{})
    grid_on = options.get('grid_on',False)
    x_lines : list = options.pop('xLines',[])
    y_lines : list = options.pop('yLines',[])

    plt.rcParams.update(handle.rc)
    legend_labeals = legend.get('labels',[])
    fig, ax = plt.subplots()
    ymin = np.inf
    ymax = -ymin
    line_idx = 0
    for data in y_data:
        marker_type = 'o'
        color_type = 'k'
        label_name = None
        if line_idx < len(markers):
            marker_type = markers[line_idx]
        if line_idx < len(colors):
            color_type = colors[line_idx]
        if line_idx < len(legend_labeals):
            label_name = legend_labeals[line_idx]
        if data is None:
            break
        data = np.array(data)
        if data.ndim == 1:
            ymin,ymax = handle.calculate_limits(data,ytick_region,ymin,ymax)
            ax.scatter(x,data,s = 16,marker=marker_type,facecolors = 'none',edgecolor = color_type,label = label_name)
            line_idx+=1
        else:
            for i in range(data.shape[1]):
                if line_idx < len(markers):
                    marker_type = markers[line_idx]
                if line_idx < len(colors):
                    color_type = colors[line_idx]
                if line_idx < len(legend_labeals):
                    label_name = legend_labeals[line_idx]
                ymin,ymax = handle.calculate_limits(data[:,i],ytick_region,ymin,ymax)
                ax.scatter(x,data[:,i],s = 16,marker=marker_type,facecolors = 'none',
                           edgecolor = color_type,label = label_name)
                line_idx+=1
        
    #绘图完成
    if xtick_type == 'manual':
        xTicks: list = xtick.get('ticks',[])
    else:
        xTicks = handle.calculate_ticks(min(x),max(x),'x',xtick_count,xtick_type)
        xTicks,x_step_len = handle.remove_mask_ticks(xTicks,ax=ax,fig= fig,type='x')
    if ytick_type =='manual':
        yTicks: list = ytick.get('ticks',[])
    else:
        yTicks = handle.calculate_ticks(ymin,ymax,'y',ytick_count,ytick_type)
        yTicks,y_step_len = handle.remove_mask_ticks(yTicks,ax=ax,fig= fig,type='y')
    ax.set_ylim([yTicks[0],yTicks[-1]])
    
    ax.set_yticks(yTicks)
    ax.set_xticks(xTicks)
    ax.set_xlim([xTicks[0] ,xTicks[-1]])
    if xtick_digit >= 0:
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{xtick_digit}f'))
    if ytick_digit >= 0:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{ytick_digit}f'))

    #次刻度
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5*x_step_len))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5*y_step_len))
    if x_unit:
        ax.set_xlabel(fr'{x_name}/$\rm {x_unit}$' ,fontname='SimSun')
    else:
        ax.set_xlabel(fr'{x_name}',fontname='SimSun')
    if y_unit:
        ax.set_ylabel(fr'{y_name}/$\rm {y_unit}$',fontname='SimSun')
    else:
        ax.set_ylabel(fr'{y_name}',fontname='SimSun')
    if legend:
        legend_ncols = legend.get('ncols',1)
        ax.legend(loc='upper right',framealpha= 1.0,frameon = True,ncol = legend_ncols,
                  fancybox = False,edgecolor = 'k' ,borderpad=0.2,
                  prop={'size' :handle.rc['font.size']-1.5 ,'family' :'SimSun'}).get_frame().set_linewidth(0.5)
    for y_line in y_lines:
        value = y_line.pop('value')
        if value:
            handle.plot_marker_lines(ax,value, axis ='y', color=y_line.pop('color' ,'k'),
                                width=y_line.pop('width' ,0.5),style=y_line.pop('style' ,'--'),
                                txt=y_line.pop('txt',''))
    for x_line in x_lines:
        value = x_line.pop('value')
        if value:
            handle.plot_marker_lines(ax,value, axis ='x', color=x_line.pop('color','k'),
                                width=x_line.pop('width',0.5),style=x_line.pop('style','--'),
                                txt=x_line.pop('txt',''))
    if grid_on:
       plt.grid(linestyle = '-',which='major',linewidth = 0.5,color = 'lightgray') 
    plt.tight_layout()

    #plt.show()
    if output:
        fig.savefig(output)
    plt.close()


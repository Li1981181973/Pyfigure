"""
该文件包含用于绘制多条曲线的线条图和多y轴线条图的函数包。

banch_name: 2025-1-12
version: 1.0.7
修改部分：
    — 优化了轴的标签计算算法。
    - 优化了轴标签值的显示，减少标签相互重叠发生的可能。

version: 1.0.6
修改部分：
    - 修复了X轴端点显示异常问题。

version: 1.0.5
修改部分
    — 添加自定义轴的设置功能：
        xticks:{'type':'terminal'|'auto'|'manual','count':5,'ticks':[],'region':1.0,'digit':-1} 
        yticks:{'type':'terminal'|'auto'|'manual','count':5,'ticks':[],'region':0.8,'digit':-1}
    — 删除xtickType参数，删除了region参数，集成到xticks、yticks参数中。
    注：默认情况下，x轴的ticks类型为'terminal'，y轴的ticks类型为'auto'。
    其中，terminal：将会显示轴端点刻度，无论端点值是否为标签步长整数倍。
         auto：会自动根据曲线数值范围，并考虑数据所占画幅比例region。
         x轴regin默认为1，y轴的region默认为0.8。
         manual：手动设置ticks，ticks为列表，如[0,1,2,3,4,5]。
         'digit'：标签显示小数位数
    
version: 1.0.4
修改部分:
    -考虑了绘图区域比例的y轴刻度修正
    -添加了xtickType参数，用于控制x轴的ticks类型，可选值有'auto'和'terminal'，默认为'auto'。
    -添加了region参数，用于控制y轴的显示范围，默认为0.8。
    -修复了多y轴的曲线图在绘制时，曲线颜色、曲线线型、曲线标记等被不正确设置问题。
    -修改了多y轴的曲线图，y轴位置设置算法， 形式为：…… Y5| Y3 | Y0 |绘图区域| Y1 | Y2 | Y4 ……
    -多y轴的曲线图绘制函数参数接受兼容了链表类型、以及多维数组等作为同一图层指示。
    -添加函数__calculate_limits__(),以实现轴最大值和最小值预计算。
日期：2024-1-6

version: 1.0.2
功能描述：
    - figure_simple: 绘制单y轴的多条曲线图。
    - figure_multi_y: 绘制多y轴的曲线图。
    - __plot_marker_lines__: 绘制平行于坐标轴的标记线。
    - __calculate_ticks__: 计算坐标轴的刻度。

版权所有 (c) 2024 Li Taotao
作者邮箱地址: li1981181973@my.swjtu.edu.cn

请注意，这些函数需要matplotlib支持。
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import figure_tools.handle as handle 


#绘图设置
'''
绘制多条曲线的线条图
    *data: 为曲线数值序列。
    xName: 为横轴变量的名称
    xUnit: 为横轴变量的单位,复合单位应该添加()，如(m·s^{-2}),可使用Latex语法。
    yName: 为纵轴的名称.
    yUnit: 为纵轴变量的单位，复合单位应该添加()，如(m·s^{-2}),可使用Latex语法。
    outputPath(str): 输出路径，默认为空，不输出
    colors(list):接受颜色名称列表，可以是：'black','k'或者十六进制编码的颜色
    colors(list):接受颜色名称列表，可以是：'black','k'或者十六进制编码的颜色
    legends：不设置，或设置为空时，则不显示legend
    makers(list):接受以下字符,如'.'、','、'o'、'v'、'^'、'<'、'>'、'*'、'+'、'x'、'X'、'D'、'd'、's'
    lineStyles(list): 曲线的线型,如'-'、'-.'、':'、'--'
    xLines(list): 绘制平行与x轴的直线,并标注[{'value'= 0,'txt':'','style':':','width':1,'color':'black'}]
    yLines(list): 绘制平行与y轴的直线,并标注[{'value'= 0,'txt':'','style':':','width':1,'color':'black'}]
    xticks:{'type':'terminal'|'auto'|'manual','count':5,'ticks':[],'region':1.0,'digit':-1} 
    yticks:{'type':'terminal'|'auto'|'manual','count':5,'ticks':[],'region':0.8,'digit':-1}
示例：

'''
def figure_lines(x, *datas,**kargs):
    if datas is None:
        return
    #读取参数
    xName = kargs.pop('xName' ,'axis_x')
    xUnit = kargs.pop('xUnit' ,'')
    yName = kargs.pop('yName' ,'axis_y')
    yUnit = kargs.pop('yUnit' ,'')
    
    #ticks type parser
    xtick:dict = kargs.pop('xticks' ,{})
    ytick:dict = kargs.pop('yticks' ,{})
    xtick_type:str = xtick.pop('type','terminal')
    ytick_type:str = ytick.pop('type','auto')
    xtick_region = xtick.pop('region',1.0)
    ytick_region = ytick.pop('region',0.8)
    xtick_count = xtick.pop('count',5)
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
    outputPath:str = kargs.pop('outputPath' ,'')
    colors :list = kargs.pop('colors' ,[])
    lineStyles :list = kargs.pop('lineStyles' ,[])
    markers :list = kargs.pop('markers' ,[])
    legend :dict = kargs.pop('legend' ,{})
    # legend : {labels:[],ncols:1}
    xLines :list = kargs.pop('xLines' ,[])
    yLines :list = kargs.pop('yLines' ,[])
    
    grid_on = kargs.pop('grid_on',True)
    plt.rcParams.update(handle.rc)
    fig ,ax = plt.subplots()
    #存放曲线信息
    ymin = np.inf
    ymax = -ymin
    #绘制数据
    for data in datas:
        if data is None:
            break
        data = np.array(data)
        if data.ndim == 1:
            ymin,ymax = handle.calculate_limits(data,ytick_region,ymin,ymax)
            ax.plot(x ,data)
        else:
            for index in range(data.shape[1]):
                ymin,ymax = handle.calculate_limits(data[:,index],ytick_region,ymin,ymax)
                ax.plot(x ,data[:,index])
    #设置轴的ticks
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
    ax.set_xlim([xTicks[0] ,xTicks[-1]])
    ax.set_ylim([yTicks[0] ,yTicks[-1]])
    #主刻度

    x_step_len = xTicks[2]-xTicks[1]
    y_step_len = yTicks[2]-yTicks[1]
    if xtick_type == 'terminal':
        if(abs(xTicks[1]-xTicks[0])<=0.08*x_step_len):
            xTicks.remove(xTicks[1])
        if(abs(xTicks[-1]-xTicks[-2])<=0.09*x_step_len*handle.power_scale(xTicks[-1])[1]):
            xTicks.remove(xTicks[-2])
    if xtick_digit >= 0:
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{xtick_digit}f'))
    if ytick_digit >= 0:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{ytick_digit}f'))
    ax.xaxis.set_ticks(xTicks)
    ax.yaxis.set_ticks(yTicks)
    #次刻度
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5*x_step_len))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5*y_step_len))
    #设置label
    if xUnit:
        ax.set_xlabel(fr'{xName}/$\rm {xUnit}$' ,fontname='SimSun')
    else:
        ax.set_xlabel(xName ,fontname='SimSun')
    if yUnit:
        ax.set_ylabel(fr'{yName}/$\rm {yUnit}$' ,fontname='SimSun')
    else:
        ax.set_ylabel(yName ,fontname='SimSun')
    #设置格式：曲线颜色、曲线线性和、图例名称
    lines_list = ax.get_lines()
    legend_labels = legend.get('labels',[])
    for idx, line in enumerate(lines_list):
        if idx < len(colors):
            line.set_color(colors[idx])
        if idx < len(lineStyles):
            line.set_linestyle(lineStyles[idx])
        if idx < len(legend_labels):
            line.set_label(legend_labels[idx])
        if idx < len(markers):
            line.set_marker(markers[idx])
    if legend:
        legend_ncols = legend.get('ncols',1)
        ax.legend(loc='upper right',framealpha= 1.0,frameon = True,ncol = legend_ncols,
                  fancybox = False,edgecolor = 'k' ,borderpad=0.2,
                  prop={'size' :handle.rc['font.size']-1.5 ,'family' :'SimSun'}).get_frame().set_linewidth(0.5)
        
    #绘制标注曲线
    for option in xLines:
        value = option.pop('value')
        if value:
            handle.plot_marker_lines(ax,value,axis ='x', color=option.pop('color' ,'k'),
                                width=option.pop('width' ,0.5),style=option.pop('style' ,'--'),
                                txt=option.pop('txt',''))
    for option in yLines:
        value = option.pop('value')
        if value:
            handle.plot_marker_lines(ax,value, axis ='y', color=option.pop('color' ,'k'),
                                width=option.pop('width' ,0.5),style=option.pop('style' ,'--'),
                                txt=option.pop('txt',''))
    plt.tight_layout()
    if grid_on:
       plt.grid(linestyle = '-',which='major',linewidth = 0.5,color = 'lightgray')
    #plt.show()
    if outputPath and outputPath.strip():
        fig.savefig(outputPath,bbox_inches='tight')
    plt.close()

def figure_multi_y(x ,*datas ,**kargs):
    """
    绘制多条曲线的线条图(多y轴)
    *data: 为曲线数值序列，在同一图层内绘制的曲线，请使用中括号括起来，或者以一个二维数组的方式传入。
    xName: 为横轴变量的名称
    xUnit: 为横轴变量的单位,复合单位应该添加()，如(m·s^{-2}),可使用Latex语法
    yNames: 为纵轴的名称列表.
    yUnits: 为纵轴变量的单位列表，复合单位应该添加()，如(m·s^{-2}),可使用Latex语法
    legends：不设置，或设置为空时，则不显示legend
    yTicksCount(int): y轴的推荐刻度数，默认值为5，但真实刻度数不完全是推荐值。
    colors(list):接受颜色名称列表，可以是：'black','k'或者十六进制编码的颜色。
    outputPath:接受文件保存路径
    
    """
    if datas is None:
        return
    #绘图选项解析
    xName = kargs.pop('xName' ,'axis_x')
    xUnit = kargs.pop('xUnit' ,None)
    yNames = kargs.pop('yNames' ,[])
    yUnits = kargs.pop('yUnits' ,[])
    
    #ticks type parser
    xtick:dict = kargs.pop('xticks' ,{})
    ytick:dict = kargs.pop('yticks' ,{})
    xtick_type:str = xtick.pop('type','terminal')
    ytick_type:str = ytick.pop('type','auto')
    xtick_region = xtick.pop('region',1.0)
    ytick_region = ytick.pop('region',0.8)
    xtick_count = xtick.pop('count',5)
    ytick_count = ytick.pop('count',5)
    xtick_digit:int = xtick.pop('digit',-1)
    ytick_digit:int = ytick.pop('digit',-1)
    if not xtick_type in ['terminal','auto','manual']:
        xtick_type = 'terminal'
    if not ytick_type in ['terminal','auto','manual'] :
        ytick_type = 'auto'
    if xtick_type == 'manual' and len(xtick.get('ticks',[])) == 0:
        xtick_type = 'terminal'
    if ytick_type == 'manual':
        ytick_type = 'auto'
    
    outputPath = kargs.pop('outputPath' ,'')
    colors :list = kargs.pop('colors' ,[])
    lineStyles :list = kargs.pop('lineStyles' ,[])
    markers :list = kargs.pop('markers' ,[])
    legends :list = kargs.pop('legends' ,[])
    xLines = kargs.pop('xLines' ,[])
    yLines = kargs.pop('yLines' ,[])
    grid_on = options.get('grid_on',False)
    plt.rcParams.update(handle.rc)
    fig = plt.figure()
    ax_list = []
    for i, item in enumerate(datas):
        #绘制新的一个图层
        ymin ,ymax = np.inf ,-np.inf
        if i == 0:
            ax_list.append(plt.subplot())
        else:
            ax_list.append(ax_list[0].twinx())
        if isinstance(item,list):
            item = np.array(item).T
            if item.shape[0] != x.shape[0]:
                print('数据维度不匹配')
                return
        else:
            item = np.array(item)
            if item.shape[0] != x.shape[0]:
                print('数据维度不匹配')
                return
        if item.ndim == 1:
            ymin,ymax = handle.calculate_limits(item,ytick_region)
            ax_list[i].plot(x ,item)
        else:
            for index in range(item.shape[1]):
                ymin,ymax = handle.calculate_limits(item[:,index],ytick_region,ymin,ymax)
                ax_list[i].plot(x ,item[:,index])
        #设置轴的ticks
        if xtick_type == 'manual':
            xTicks = xtick.get('ticks')
        else:
            xTicks = handle.calculate_ticks(min(x), max(x), 'x', xtick_count,xtick_type)

        yTicks = handle.calculate_ticks(ymin, ymax, 'y', ytick_count,ytick_type)
        ax_list[i].set_xlim(xTicks[0] ,xTicks[-1])
        ax_list[i].set_ylim(yTicks[0] ,yTicks[-1])
        x_step_len = xTicks[2]-xTicks[1]
        y_step_len = yTicks[2]-yTicks[1]
        if xtick_type == 'terminal':
            if(abs(xTicks[1]-xTicks[0])<=0.08*x_step_len):
                xTicks.remove(xTicks[1])
            if(abs(xTicks[-1]-xTicks[-2])<=0.09*x_step_len*handle.power_scale(xTicks[-1])[1]):
                xTicks.remove(xTicks[-2])
        if xtick_digit >= 0:
            ax_list[i].xaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{xtick_digit}f'))
        if ytick_digit >= 0:
            ax_list[i].yaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{ytick_digit}f'))
        ax_list[i].xaxis.set_ticks(xTicks)
        ax_list[i].xaxis.set_minor_locator(ticker.MultipleLocator(x_step_len/2))
        ax_list[i].yaxis.set_ticks(yTicks)
        ax_list[i].yaxis.set_minor_locator(ticker.MultipleLocator(y_step_len/2))
        
        #设置多y轴的位置
        if i == 1 or (i % 2 == 0 and i != 0):
            if i > 1:
                ax_list[i].spines['right'].set_position(('outward', 50))
            ax_list[i].spines['left'].set_visible(False)
            ax_list[i].yaxis.set_ticks_position('right')
            ax_list[i].yaxis.set_label_position('right')
        else:
            if i > 0:
                ax_list[i].spines['left'].set_position(('outward', 50))
            ax_list[i].spines['right'].set_visible(False)
            ax_list[i].yaxis.set_ticks_position('left')
            ax_list[i].yaxis.set_label_position('left')
    #设置图层的轴标题以及轴的颜色
    units_count = len(yUnits)
    yNames_count = len(yNames)
    i :int = 0
    yLabels = []
    while i < max(yNames_count ,units_count):
        tmp_label = ''
        if i< yNames_count:
            tmp_label += yNames[i]
        if i < units_count:
            if yUnits[i] and tmp_label:
                tmp_label += fr'/$\rm {yUnits[i]}$'
        yLabels.append(tmp_label)
        i += 1
    #设置图层的轴标题
    for yLabel, ax in zip(yLabels, ax_list):
        ax.set_ylabel(yLabel, fontname='SimSun')
    if xUnit:
        ax_list[0].set_xlabel(fr'{xName}/$\rm {xUnit}$', fontname='SimSun')
    else:
        ax_list[0].set_xlabel(xName, fontname='SimSun')
    #线条颜色设置,y轴、轴标题、轴刻度及标签颜色
    line_index = 0
    for ax in ax_list:
        level_color = 'k'
        for i, line in enumerate(ax.get_lines()):
            if line_index < len(colors):
                line.set_color(colors[line_index])
                if i == 0:
                    level_color = colors[line_index]
            elif i == 0:
                level_color = line.get_color()
            if line_index < len(markers):
                line.set_marker(markers[line_index])
            if line_index < len(lineStyles):
                line.set_linestyle(lineStyles[line_index])
            if line_index < len(legends):
                line.set_label(legends[line_index])
            line_index += 1
        ax.yaxis.label.set_color(level_color)
        ax.tick_params(axis='y',which='major', colors=level_color)
        ax.tick_params(axis='y',which='minor', colors=level_color)
        ax.spines['left'].set_color(level_color)
        ax.spines['right'].set_color(level_color)
    #显示标签
    if legends:
        fig.legend(prop={'family': "SimSun",'size':handle.rc['font.size']},framealpha= 1.0,frameon = True,
                   fancybox = False,edgecolor = 'k' ,bbox_to_anchor=(1, 1), 
                   bbox_transform=ax_list[0].transAxes).get_frame().set_linewidth(0.75)

    for options in xLines:
        ax_index = options.get('level',0)
        value = options.get('value')
        if value and ax_index < len(ax_list):
            handle.plot_marker_lines(ax_list[ax_index], value,axis = 'x',color = options.pop('color','k'),
                                style=options.pop('style','--'),width=options.pop('width',0.5),
                                txt = options.pop('txt',''))
    for options in yLines:
        ax_index = options.pop('level',0)
        value = options.pop('value')
        if value and ax_index < len(ax_list):
            handle.plot_marker_lines(ax_list[ax_index], value,axis = 'y',color = options.pop('color','k'),
                                style=options.pop('style','--'),width=options.pop('width',0.5),
                                txt = options.pop('txt',None))
    if grid_on:
       plt.grid(linestyle = '-',which='major',linewidth = 0.5,color = 'lightgray',axis = 'both')
    plt.tight_layout()
    
    #plt.show()
    #保存图片
    if outputPath and outputPath.strip():
        fig.savefig(outputPath)
    plt.close()


def plot_test(x,*datas):
    if datas is None:
        return
    plt.rcParams.update(handle.rc)
    fig ,ax = plt.subplots()
    for data in datas:
        if data is None:
            break
        data = np.array(data)
        if data.ndim == 1:
            ax.plot(x ,data)
        else:
            for index in range(data.shape[1]):
                ax.plot(x ,data[:,index])
    plt.tight_layout()            
    plt.show()
    plt.close()
    
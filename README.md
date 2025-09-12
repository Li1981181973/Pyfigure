# Pyfigure
Drawing line charts, scatter plots, and corresponding multi y-axis graphs based on the secondary development of matplotlib library
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

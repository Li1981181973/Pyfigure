from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import figure_tools.handle as handle

def figure_hyper(x,*data,**options):
    if data == None:
        return
    if options == None:
        options = {}
    options_tmp = handle.get_options_single(**options)
    xtick = options_tmp['xtick']
    ytick = options_tmp['ytick']
    xtick_type = xtick.get('type','terminal')
    ytick_type = ytick.get('type','auto')
    xtick_count = xtick.pop('count',5)
    ytick_count = ytick.pop('count',5)
    xtick_digit:int = xtick.pop('digit',-1)
    ytick_digit:int = ytick.pop('digit',-1)
    legend = options_tmp['legend']
    legend_label = legend.get('labels',[])
    legend_ncol = legend.get('ncols',1)
    xlines = options_tmp['xlines']
    ylines = options_tmp['ylines']
    outputPath = options_tmp.get('outputPath' ,'')

    if not xtick_type in ['terminal','auto','manual']:
        xtick_type = 'terminal'
    if not ytick_type in ['terminal','auto','manual'] :
        ytick_type = 'auto'
    if xtick_type == 'manual' and len(xtick.get('ticks',[])) == 0:
        xtick_type = 'terminal'
    if ytick_type == 'manual':
        ytick_type = 'auto'
    # 加载数据绘制类型 
    kinds = options_tmp.get('kinds',[])
    
    plt.rcParams.update(handle.rc)
    fig = plt.figure(figsize= handle.rc['figure.figsize'])
    ax_list = []
    level_idx = 0
    line_idx = 0
    level_color = None

    for data_item in data:
        data_item = np.asarray(data_item,dtype=np.float32)
        data_min, data_max = np.inf,-np.inf
        if level_idx == 0:
            ax_list.append(plt.subplot())
        else:
            ax_list.append(ax_list[0].twinx())
        kind_cur = kinds[level_idx] if level_idx < len(kinds) else 'line'
        ynames = options_tmp['ynames']
        yunits = options_tmp['yunits']
        y_name_cur = ynames[level_idx] if level_idx <len(ynames) else 'y_axis'
        y_unit_cur = yunits[level_idx] if level_idx <len(yunits) else ''
        if y_unit_cur == '':
            y_label_cur = y_name_cur
        else:
            y_label_cur = rf'{y_name_cur}/$\rm {y_unit_cur}$'
        line_color,line_style,line_width,line_marker,line_lagend = None,'-',1,None,None
        if data_item.ndim == 1:
            #获取绘图设置
            ax = None
            line_color = options_tmp['colors'][line_idx] if line_idx < len(options_tmp['colors']) else 'k'
            level_color = line_color
            line_style = options_tmp['styles'][line_idx] if line_idx < len(options_tmp['styles']) else '-'
            line_width = options_tmp['widths'][line_idx] if line_idx < len(options_tmp['widths']) else 1
            line_marker = options_tmp['markers'][line_idx] if line_idx < len(options_tmp['markers']) else None
            line_lagend = legend_label[line_idx] if line_idx < len(legend_label) else None
            if len(data_item) != len(x):
                raise ValueError('x and data must be the same length')
            if kind_cur == 'line':
                ax_list[level_idx].plot(x,data_item,color = line_color,linestyle = line_style,linewidth = line_width,marker = line_marker,label = line_lagend)
            elif kind_cur == 'scatter':
                ax_list[level_idx].scatter(x,data_item,color = line_color,marker = line_marker,label = line_lagend,s = 18)
            else:
                raise ValueError('kind must be line or scatter')
            data_min_tmp, data_max_tmp = handle.calculate_limits(data = data_item,region_ratio = ytick.get('region',0.8))
            data_min = min(data_min,data_min_tmp)
            data_max = max(data_max,data_max_tmp)
            line_idx +=1
        else:
            idx_tmp = 0
            for data in data_item:
                
                if data.shape[0] != x.shape[0]:
                    raise ValueError('x and data must be the same length')
                line_color = options_tmp['colors'][line_idx] if line_idx < len(options_tmp['colors']) else None
                line_style = options_tmp['styles'][line_idx] if line_idx < len(options_tmp['styles']) else '-'
                line_width = options_tmp['widths'][line_idx] if line_idx < len(options_tmp['widths']) else 1
                line_marker = options_tmp['markers'][line_idx] if line_idx < len(options_tmp['markers']) else None
                line_lagend = legend_label[line_idx] if line_idx < len(legend_label) else None
                data_min_tmp, data_max_tmp = handle.calculate_limits(data = data,region_ratio = ytick.get('region',0.8))
                data_min = min(data_min,data_min_tmp)
                data_max = max(data_max,data_max_tmp)
                if kind_cur == 'line':
                    ax_list[level_idx].plot(x,data,color = line_color,linestyle = line_style,linewidth = line_width,marker = line_marker,label = line_lagend)
                elif kind_cur == 'scatter':
                    ax_list[level_idx].scatter(x,data,color = line_color,marker = line_marker,label = line_lagend,s = 18)
                else:
                    raise ValueError('kind must be line or scatter')
                if idx_tmp == 0:
                    level_color = line_color
                idx_tmp += 1
                line_idx +=1
        # 设置坐标轴
        if xtick_type == 'manual':
            x_tick = xtick['ticks']
        else:
            x_tick = handle.calculate_ticks(min(x),max(x),'x',xtick_count,xtick_type)
            x_tick,x_step_len = handle.remove_mask_ticks(x_tick,ax=ax_list[level_idx],fig=fig,type= 'x')
        y_tick = handle.calculate_ticks(data_min,data_max,'y',ytick_count,ytick_type)
        y_tick,y_step_len = handle.remove_mask_ticks(y_tick,ax=ax_list[level_idx],fig= fig,type='y')
        ax_list[level_idx].set_xlim(x_tick[0],x_tick[-1])
        ax_list[level_idx].set_ylim(y_tick[0],y_tick[-1])

        xname: str = options_tmp['xname']
        xunit: str = options_tmp['xunit']
        if len(xunit) > 0:
            xlabel = rf'{xname}/$\rm {xunit}$'
            ax_list[level_idx].set_xlabel(xlabel,fontname = 'SimSun')
        else:
            ax_list[level_idx].set_xlabel(xname,fontname = 'SimSun')
        if xtick_digit >= 0:
            ax_list[level_idx].xaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{xtick_digit}f'))
        if ytick_digit >= 0:
            ax_list[level_idx].yaxis.set_major_formatter(ticker.FormatStrFormatter(f'%.{ytick_digit}f'))
        ax_list[level_idx].xaxis.set_ticks(x_tick)
        ax_list[level_idx].xaxis.set_minor_locator(ticker.MultipleLocator(x_step_len/2))
        ax_list[level_idx].yaxis.set_ticks(y_tick)
        ax_list[level_idx].yaxis.set_minor_locator(ticker.MultipleLocator(y_step_len/2))
        ax_list[level_idx].set_ylabel(y_label_cur,fontname='SimSun')
        ax_list[level_idx].yaxis.label.set_color(level_color)
        ax_list[level_idx].tick_params(axis='y',which='major', colors=level_color)
        ax_list[level_idx].tick_params(axis='y',which='minor', colors=level_color)
        ax_list[level_idx].spines['left'].set_color(level_color)
        ax_list[level_idx].spines['right'].set_color(level_color)

        if level_idx==1 or (level_idx%2==0 and level_idx!=0):
            if level_idx > 1:
                ax_list[level_idx].spines['right'].set_position(('outward', 50))
            ax_list[level_idx].spines['left'].set_visible(False)
            ax_list[level_idx].yaxis.set_ticks_position('right')
            ax_list[level_idx].yaxis.set_label_position('right')
        else:
            if level_idx > 0:
                ax_list[level_idx].spines['left'].set_position(('outward', 50))
            ax_list[level_idx].spines['right'].set_visible(False)
            ax_list[level_idx].yaxis.set_ticks_position('left')
            ax_list[level_idx].yaxis.set_label_position('left')
        level_idx += 1
        if options_tmp['grid_on']:
            plt.grid(axis = 'both',linestyle = '-',which='major',linewidth = 0.5,color = 'lightgray')
    if len(legend_label) > 0:
            fig.legend(prop={'family': "SimSun",'size':handle.rc['font.size']-2},
                       framealpha= 1.0,frameon = True,ncol = legend_ncol,loc = 'upper center',
                    fancybox = False,edgecolor = 'k' ,bbox_to_anchor=(0.5, 1),borderpad=0.2,
                    bbox_transform=ax_list[0].transAxes).get_frame().set_linewidth(0.5)
    for op in xlines:
        ax_index = options.get('level',0)
        value = options.get('value')
        if value and ax_index < len(ax_list):
            handle.plot_marker_lines(ax_list[ax_index], value,axis = 'x',color = options.pop('color','k'),
                                style=options.pop('style','--'),width=options.pop('width',0.5),
                                txt = options.pop('txt',''))
    for op in ylines:
        ax_index = options.get('level',0)
        value = options.get('value')
        if value and ax_index < len(ax_list):
            handle.plot_marker_lines(ax_list[ax_index], value,axis = 'y',color = options.pop('color','k'),
                                style=options.pop('style','--'),width=options.pop('width',0.5),
                                txt = options.pop('txt',''))
    if options_tmp['grid_on']:
        plt.grid(axis = 'both',linestyle = '-',which='major',linewidth = 0.5,color = 'lightgray')
    plt.tight_layout()
    if outputPath and outputPath.strip():
        fig.savefig(outputPath)
    plt.close()
                
    
    

    
    
    

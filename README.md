# Pyfigure

Pyfigure是一个基于matplotlib的高级绘图工具库，专注于简化科研与数据分析中的图表绘制流程。该库提供了多种预设的图表绘制函数，支持单y轴线条图、多y轴线条图、散点图等多种可视化类型，并内置了智能刻度计算、标签优化、样式统一等功能，帮助用户快速生成高质量图表。


## 功能特点

- 支持多种图表类型：单y轴线条图、多y轴线条图、散点图等
- 智能刻度计算：自动优化坐标轴刻度，减少标签重叠
- 灵活的样式定制：支持自定义颜色、线型、标记、图例等
- 便捷的参考线绘制：可添加平行于坐标轴的标记线并标注文本
- 支持多维度数据输入：兼容一维数组、二维数组等多种数据格式
- 完善的单位支持：支持LaTeX语法的单位表示，自动格式化坐标轴标签


## 安装说明

### 依赖环境
- Python 3.6+
- matplotlib >= 3.3.0
- numpy >= 1.18.0

### 安装方法
1. 克隆或下载项目代码到本地
```bash
git clone https://github.com/yourusername/Pyfigure.git
```
2. 安装依赖包
```bash
pip install matplotlib numpy
```
3. 将项目目录添加到Python路径（或直接将项目文件夹放在工作目录下）


## 核心功能模块

### 1. 单y轴线条图（`pline.figure_lines`）
用于绘制共享同一y轴的多条曲线，适用于比较同量级的多组数据。

#### 主要参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| `x` | 数组 | x轴数据 |
| `*datas` | 数组/数组列表 | 一个或多个y轴数据（可传入多个数组或二维数组） |
| `xName` | str | x轴名称 |
| `xUnit` | str | x轴单位（支持LaTeX语法，如`(m·s^{-1})`） |
| `yName` | str | y轴名称 |
| `yUnit` | str | y轴单位 |
| `xticks` | dict | x轴刻度设置，格式：`{'type':'terminal'|'auto'|'manual','count':5,'ticks':[],'region':1.0,'digit':-1}` |
| `yticks` | dict | y轴刻度设置（格式同上） |
| `colors` | list | 曲线颜色列表 |
| `lineStyles` | list | 线型列表（如`'-'`、`'--'`） |
| `markers` | list | 标记样式列表（如`'o'`、`'*'`） |
| `legend` | dict | 图例设置，格式：`{'labels':[], 'ncols':1}` |
| `xLines`/`yLines` | list | 参考线设置，格式：`[{'value':0, 'txt':'', 'style':':', 'width':1, 'color':'black'}]` |
| `outputPath` | str | 图像输出路径（为空时不输出） |


### 2. 多y轴线条图（`pline.figure_multi_y`）
用于绘制具有多个独立y轴的曲线，适用于比较不同量级或不同单位的多组数据。

#### 主要参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| `x` | 数组 | x轴数据 |
| `*datas` | 数组/数组列表 | 多组y轴数据（同一y轴的数据用列表或二维数组包裹） |
| `yNames` | list | 各y轴名称列表 |
| `yUnits` | list | 各y轴单位列表 |
| 其他参数 | - | 与`figure_lines`类似，部分参数为列表形式（对应多个y轴） |


### 3. 散点图（`scatter.figure_scatter`）
用于绘制散点图，支持多组数据对比，可自定义标记样式。

#### 主要参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| `x` | 数组 | x轴数据 |
| `*y_data` | 数组/数组列表 | 一个或多个y轴数据 |
| 其他参数 | - | 与`figure_lines`类似，增加散点特定样式设置 |


### 4. 混合图表（`hyper.figure_hyper`）
支持在同一图表中混合绘制线条图和散点图，支持多y轴配置。


## 刻度设置说明（`xticks`/`yticks`）
刻度设置字典包含以下键：
- `type`：刻度类型
  - `'terminal'`：显示端点刻度（默认x轴）
  - `'auto'`：自动计算刻度（默认y轴）
  - `'manual'`：手动指定刻度
- `count`：刻度数量（自动模式下有效）
- `ticks`：手动刻度列表（手动模式下有效）
- `region`：数据占画幅比例（控制坐标轴范围）
- `digit`：显示小数位数（-1为自动）


## 使用示例

### 1. 绘制单y轴线条图
```python
import numpy as np
from Pyfigure import pline

# 生成示例数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) + np.cos(x)

# 绘制图表
pline.figure_lines(
    x, y1, y2, y3,
    xName="时间", xUnit="s",
    yName="振幅", yUnit="m",
    colors=['r', 'g', 'b'],
    lineStyles=['-', '--', '-.'],
    markers=['o', '', '*'],
    legend={'labels': ['正弦', '余弦', '合成'], 'ncols': 3},
    xticks={'type': 'auto', 'count': 6, 'digit': 1},
    yticks={'type': 'auto', 'count': 5},
    xLines=[{'value': np.pi, 'txt': 'π', 'color': 'k', 'style': '--'}],
    outputPath="sin_cos.png"
)
```

### 2. 绘制散点图
```python
import numpy as np
from Pyfigure import scatter

x = np.random.rand(50)
y1 = np.random.rand(50)
y2 = np.random.rand(50) * 2

scatter.figure_scatter(
    x, y1, y2,
    xName="变量X",
    yName="变量Y",
    colors=['blue', 'red'],
    markers=['o', 's'],
    legend={'labels': ['数据组1', '数据组2']},
    grid_on=True,
    outputPath="scatter_example.png"
)
```


## 版本历史
- **1.0.7**（2025-1-12）
  - 优化轴标签计算算法
  - 减少标签重叠问题
- **1.0.6**
  - 修复X轴端点显示异常问题
- **1.0.5**
  - 添加自定义轴设置功能（`xticks`/`yticks`参数）
  - 移除旧版`xtickType`和`region`参数
- **1.0.4**
  - 优化y轴刻度计算（考虑绘图区域比例）
  - 修复多y轴样式设置问题
  - 优化多y轴位置算法


## 版权信息
- 版权所有 (c) 2024 Li Taotao
- 作者邮箱：li1981181973@my.swjtu.edu.cn
- 本项目基于matplotlib开发，遵循相关开源协议

# 绘图工具库 README

## 项目简介

本项目是一个基于Matplotlib的高级绘图工具库，提供了简洁易用的接口用于绘制多种类型的图表，包括单y轴线条图、散点图、多y轴线条图等。该库支持丰富的自定义配置，如坐标轴样式、图例、线条属性、参考线等，能够满足科研和工程绘图的多样化需求。

## 核心功能

- 绘制单y轴多条曲线（`sline`函数）
- 绘制散点图（`scatter`函数）
- 绘制多y轴线条图（`mline`函数）
- 支持混合类型多y轴图（`hyplot`函数，可同时包含线图和散点图）
- 灵活的坐标轴刻度配置（支持自动、终端对齐、手动三种模式）
- 自定义线条颜色、样式、标记点
- 支持添加参考线及标注
- 完善的图例管理和网格配置

## 安装依赖

本库依赖以下Python库：
- matplotlib >= 3.0.0
- numpy >= 1.18.0

安装命令：
```bash
pip install matplotlib numpy
```

## 快速开始

### 1. 单y轴线条图示例

```python
import numpy as np
from your_package import sline

# 生成示例数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) + np.cos(x)

# 绘制多条曲线
sline(
    x, y1, y2, y3,
    xName="时间", xUnit="s",
    yName="振幅", yUnit="m",
    colors=['red', 'blue', 'green'],
    lineStyles=['-', '--', '-.'],
    markers=['o', 's', '*'],
    legend={'labels': ['正弦', '余弦', '合成波'], 'ncols': 3},
    outputPath="line_plot.png"
)
```

### 2. 散点图示例

```python
import numpy as np
from your_package import scatter

# 生成示例数据
x = np.linspace(0, 5, 50)
y1 = np.random.normal(0, 1, 50)
y2 = np.random.normal(2, 1, 50)

# 绘制散点图
scatter(
    x, y1, y2,
    xName="X轴", yName="Y轴",
    colors=['purple', 'orange'],
    markers=['o', '^'],
    legend={'labels': ['数据组1', '数据组2']},
    grid_on=True,
    outputPath="scatter_plot.png"
)
```

### 3. 多y轴线条图示例

```python
import numpy as np
from your_package import mline

# 生成示例数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = 10 * np.cos(x)
y3 = np.exp(x/10)

# 绘制多y轴图
mline(
    x, y1, y2, y3,
    xName="时间", xUnit="s",
    ynames=["位移", "力", "能量"],
    yunits=["m", "N", "J"],
    colors=['red', 'blue', 'green'],
    legend={'labels': ['正弦位移', '余弦力', '指数能量'], 'ncols': 3},
    outputPath="multi_y_plot.png"
)
```

## API 文档

### 1. 通用参数说明

| 参数名 | 类型 | 描述 |
|--------|------|------|
| `x` | array-like | x轴数据 |
| `*datas` | array-like | 可变参数，y轴数据（可传入多个数据集） |
| `xName` | str | x轴名称 |
| `xUnit` | str | x轴单位（支持LaTeX语法） |
| `yName`/`ynames` | str/list | y轴名称（单y轴用yName，多y轴用ynames列表） |
| `yUnit`/`yunits` | str/list | y轴单位（单y轴用yUnit，多y轴用yunits列表） |
| `outputPath` | str | 图像输出路径（为空时不输出） |
| `colors` | list | 线条颜色列表（支持颜色名称或十六进制编码） |
| `lineStyles`/`styles` | list | 线条样式列表（如'-'、'--'、':'等） |
| `markers` | list | 标记点样式列表（如'o'、's'、'*'等） |
| `legend` | dict | 图例配置，包含`labels`（标签列表）和`ncols`（列数） |
| `xLines` | list | x轴参考线配置，格式：`[{'value': 值, 'txt': 标注, 'style': 样式, ...}]` |
| `yLines` | list | y轴参考线配置，格式同上 |
| `xticks`/`yticks` | dict | 坐标轴刻度配置 |
| `grid_on` | bool | 是否显示网格线（默认True） |

### 2. 坐标轴刻度配置（xticks/yticks）

刻度配置为字典类型，包含以下键：
- `type`: 刻度类型，可选`'terminal'`（终端对齐）、`'auto'`（自动计算）、`'manual'`（手动指定）
- `count`: 刻度数量（自动模式下有效）
- `ticks`: 手动刻度列表（手动模式下有效）
- `region`: 数据显示区域比例（0-1）
- `digit`: 显示小数位数（-1表示自动）

示例：
```python
xticks={
    'type': 'auto',
    'count': 6,
    'region': 0.9,
    'digit': 1
}
```

### 3. 主要函数说明

#### `sline(x, *datas, **kargs)`
绘制单y轴多条曲线，支持自定义线条样式、坐标轴和图例。

#### `scatter(x, *y_data, **options)`
绘制散点图，支持多组数据对比，可配置标记点样式和颜色。

#### `mline(x, *data, **options)`
绘制多y轴线条图，每个数据集使用独立y轴，适合展示不同量级数据。

#### `hyplot(x, *data, **options)`
混合类型多y轴图，支持同时绘制线图和散点图（通过`kinds`参数指定，'l'为线图，'s'为散点图）。

## 版本历史

- **v1.0.7** (2025-1-12)
  - 优化了轴的标签计算算法
  - 优化了轴标签值的显示，减少重叠

- **v1.0.6**
  - 修复了X轴端点显示异常问题

- **v1.0.5**
  - 添加自定义轴的设置功能（xticks/yticks参数）
  - 集成region参数到xticks/yticks中
  - 默认x轴ticks类型为'terminal'，y轴为'auto'

- **v1.0.4**
  - 优化y轴刻度计算，考虑绘图区域比例
  - 修复多y轴图样式设置问题
  - 改进多y轴位置算法

- **v1.0.2**
  - 初始版本，包含基础绘图功能

## 版权信息

版权所有 (c) 2024 Li Taotao

作者邮箱: li1981181973@my.swjtu.edu.cn

本工具库基于Matplotlib开发，使用前请确保遵守相关开源协议。

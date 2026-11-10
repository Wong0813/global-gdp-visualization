"""
全球GDP动态柱状图生成脚本 (1960-2019)
Global GDP Dynamic Bar Chart (1960-2019)

技术栈: Python + Pyecharts
功能: 读取 1960-2019 年全球历史 GDP 数据，提取每年 GDP 前八名的国家，
      生成基于 Timeline（时间线）的动态可交互水平柱状图。
"""

import os
import sys

# 兼容 Windows 控制台输出中文与特殊符号
if sys.platform == "win32" and sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from pyecharts.globals import ThemeType


def load_gdp_data(file_path: str) -> dict:
    """
    读取并清洗全球GDP数据CSV文件
    返回格式: { year: [[country, gdp], ...], ... }
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"未找到数据文件: {file_path}")

    # 尝试不同编码读取文件 (常见有 GBK, GB2312, UTF-8)
    lines = None
    for encoding in ["GB2312", "GBK", "utf-8", "utf-8-sig"]:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                lines = f.readlines()
            break
        except UnicodeDecodeError:
            continue

    if lines is None:
        raise ValueError("无法使用常见编码解析数据文件！")

    # 去除表头 (year, GDP, rate)
    header = lines.pop(0)

    # 组织数据结构: 年份 -> 国家与GDP列表
    data_dict = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) < 3:
            continue

        year = int(parts[0])
        country = parts[1]
        # GDP原始数据以元为单位（科学计数法表示），转换为浮点数
        gdp = float(parts[2])

        if year not in data_dict:
            data_dict[year] = []
        data_dict[year].append([country, gdp])

    return data_dict


def create_gdp_timeline_chart(data_dict: dict, output_path: str = "1960-2019全球gdp前八国家.html"):
    """
    根据GDP数据字典构建时间线动态柱状图，并导出为 HTML 文件
    """
    # 创建时间线对象，使用浅色主题 (ThemeType.LIGHT)
    timeline = Timeline(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))

    # 按年份升序排序 (1960 -> 2019)
    sorted_years = sorted(data_dict.keys())

    for year in sorted_years:
        year_data = data_dict[year]
        # 按 GDP 从大到小降序排列
        year_data.sort(key=lambda item: item[1], reverse=True)

        # 截取当年 GDP 前 8 名国家
        top8 = year_data[:8]

        # 核心技巧：因为横向柱状图（reversal_axis）从下往上绘制，
        # 为了让第1名显示在最顶端，我们需要将数据反转
        top8.reverse()

        country_list = [item[0] for item in top8]
        # 将 GDP 数值转换为以“亿元”为单位 (除以 10^8)
        gdp_list = [item[1] / 100000000 for item in top8]

        # 构建单个年份的柱状图
        bar = Bar()
        bar.add_xaxis(country_list)
        bar.add_yaxis(
            series_name="GDP（亿）",
            y_axis=gdp_list,
            label_opts=opts.LabelOpts(position="right")  # 数值显示在柱体右侧
        )
        bar.reversal_axis()  # x/y轴反转，变为水平柱状图
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title=f"{year}年全球前八GDP数据")
        )

        # 将当前年份的柱状图添加到时间线上
        timeline.add(chart=bar, time_point=str(year))

    # 配置时间线自动播放与动画参数
    timeline.add_schema(
        play_interval=750,      # 自动播放间隔 750毫秒
        is_timeline_show=True,  # 显示时间线轴
        is_auto_play=True,      # 打开页面自动播放
        is_loop_play=False      # 播放完2019年后停留在最终年份
    )

    # 渲染生成交互式 HTML
    timeline.render(output_path)
    print(f"✅ 生成成功: {output_path}")


def main():
    # 优先在当前目录或 data 目录下寻找数据源
    possible_paths = [
        "1960-2019全球GDP数据.csv",
        os.path.join("data", "1960-2019全球GDP数据.csv"),
        os.path.join(os.path.dirname(__file__), "data", "1960-2019全球GDP数据.csv"),
        os.path.join(os.path.dirname(__file__), "1960-2019全球GDP数据.csv"),
    ]

    csv_path = None
    for p in possible_paths:
        if os.path.exists(p):
            csv_path = p
            break

    if not csv_path:
        raise FileNotFoundError("未找到 '1960-2019全球GDP数据.csv'，请确认文件路径！")

    print(f"正在加载数据: {csv_path}")
    data_dict = load_gdp_data(csv_path)
    print(f"数据加载完成，共涵盖 {len(data_dict)} 个年份的数据。")

    output_file = os.path.join(os.path.dirname(__file__), "1960-2019全球gdp前八国家.html")
    create_gdp_timeline_chart(data_dict, output_file)


if __name__ == "__main__":
    main()

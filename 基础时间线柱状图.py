"""
基础时间线柱状图示例 (Basic Timeline Bar Chart)

功能: Pyecharts 的 Timeline（时间线）与 Bar（柱状图）基础学习案例。
学习要点:
1. 掌握 Bar 柱状图的基础构建与坐标轴反转 (reversal_axis)。
2. 掌握 LabelOpts 标签配置（数值显示位置）。
3. 掌握 Timeline 时间线轮播组件的初始化、节点关联与播放模式配置。
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


def create_basic_timeline_bar(output_path: str = "基础时间线柱状图.html"):
    # 1. 创建第 1 个时间点的柱状图
    bar1 = Bar()
    bar1.add_xaxis(["中国", "美国", "英国"])
    bar1.add_yaxis(
        series_name="GDP",
        y_axis=[30, 20, 10],
        label_opts=opts.LabelOpts(position="right")
    )
    bar1.reversal_axis()

    # 2. 创建第 2 个时间点的柱状图
    bar2 = Bar()
    bar2.add_xaxis(["中国", "美国", "英国"])
    bar2.add_yaxis(
        series_name="GDP",
        y_axis=[50, 30, 20],
        label_opts=opts.LabelOpts(position="right")
    )
    bar2.reversal_axis()

    # 3. 创建第 3 个时间点的柱状图
    bar3 = Bar()
    bar3.add_xaxis(["中国", "美国", "英国"])
    bar3.add_yaxis(
        series_name="GDP",
        y_axis=[70, 60, 60],
        label_opts=opts.LabelOpts(position="right")
    )
    bar3.reversal_axis()

    # 4. 创建时间线并添加各个节点
    timeline = Timeline(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    timeline.add(bar1, "点1")
    timeline.add(bar2, "点2")
    timeline.add(bar3, "点3")

    # 5. 配置自动循环播放
    timeline.add_schema(
        play_interval=1000,     # 每秒切换一次
        is_timeline_show=True,  # 显示时间线轴
        is_auto_play=True,      # 自动播放
        is_loop_play=True       # 循环播放
    )

    timeline.render(output_path)
    print(f"✅ 生成成功: {output_path}")


if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "基础时间线柱状图.html")
    create_basic_timeline_bar(out_file)

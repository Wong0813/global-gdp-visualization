"""
Generate static screenshots and animated GIF for global GDP visualization project.
使用 matplotlib 与 Pillow 生成高保真运行截图和 5 秒动态演变 GIF。
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PIL import Image

# 兼容 Windows 编码
if sys.platform == "win32" and sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

font_prop = None
for fname in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
    if os.path.exists(fname):
        font_prop = fm.FontProperties(fname=fname)
        break

# 全局配置中文字体
if font_prop:
    plt.rcParams["font.sans-serif"] = [font_prop.get_name(), "Microsoft YaHei", "SimHei", "sans-serif"]
else:
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

# ECharts Light 经典色板
PALETTE = [
    "#5470c6", "#91cc75", "#fac858", "#ee6666",
    "#73c0de", "#3ba272", "#fc8452", "#9a60b4"
]

def load_data(csv_path):
    lines = None
    for enc in ["GB2312", "GBK", "utf-8", "utf-8-sig"]:
        try:
            with open(csv_path, "r", encoding=enc) as f:
                lines = f.readlines()
            break
        except UnicodeDecodeError:
            continue
    lines.pop(0)
    data_dict = {}
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) >= 3:
            year = int(parts[0])
            country = parts[1]
            gdp = float(parts[2])
            if year not in data_dict:
                data_dict[year] = []
            data_dict[year].append((country, gdp))
    return data_dict

def render_chart_frame(year, top8_data, total_years=60, current_idx=0):
    """
    绘制单帧柱状图，包含标题、数值标签、时间线指示器
    top8_data: 8个元素的列表 [(country, gdp), ...]，升序排列（最大值在最后）
    """
    fig, (ax, ax_timeline) = plt.subplots(
        2, 1, 
        figsize=(10, 6), 
        gridspec_kw={"height_ratios": [9, 1]},
        dpi=120
    )
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    countries = [item[0] for item in top8_data]
    gdps = [item[1] / 100000000 for item in top8_data]  # 转换为亿元

    y_pos = np.arange(len(countries))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(countries))]

    bars = ax.barh(y_pos, gdps, height=0.55, color="#5470c6", edgecolor="none")

    # 坐标轴和网格
    ax.set_yticks(y_pos)
    ax.set_yticklabels(countries, fontproperties=font_prop, fontsize=12, color="#333333")
    ax.tick_params(axis="x", labelsize=10, colors="#666666")
    ax.grid(axis="x", linestyle="--", alpha=0.5, color="#cccccc")
    ax.set_axisbelow(True)

    # 移除多余边框
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#cccccc")

    # 动态留白 X 轴最大值
    max_val = max(gdps) if gdps else 1
    ax.set_xlim(0, max_val * 1.22)

    # 在柱子右侧标注具体数值
    for bar, val in zip(bars, gdps):
        val_str = f"{val:,.1f}" if val >= 1000 else f"{val:.2f}"
        ax.text(
            bar.get_width() + max_val * 0.015,
            bar.get_y() + bar.get_height() / 2,
            val_str,
            va="center",
            ha="left",
            fontsize=10,
            fontweight="bold",
            color="#444444"
        )

    # 标题与图例
    title_text = f"{year}年全球前八GDP数据"
    ax.set_title(title_text, fontproperties=font_prop, fontsize=18, fontweight="bold", pad=15, loc="left", color="#222222")
    ax.text(
        0.98, 1.03, "GDP（亿）",
        transform=ax.transAxes,
        fontproperties=font_prop,
        fontsize=11,
        ha="right",
        color="#666666"
    )

    # 时间轴绘制 (模拟 Timeline 组件)
    ax_timeline.set_facecolor("#ffffff")
    for spine in ax_timeline.spines.values():
        spine.set_visible(False)
    ax_timeline.set_xticks([])
    ax_timeline.set_yticks([])
    ax_timeline.set_xlim(0, 1)
    ax_timeline.set_ylim(-0.5, 0.5)

    # 轴线
    ax_timeline.plot([0.05, 0.95], [0, 0], color="#dcdcdc", lw=3, zorder=1)
    # 进度条
    progress = 0.05 + (0.90 * (current_idx / max(total_years - 1, 1)))
    ax_timeline.plot([0.05, progress], [0, 0], color="#5470c6", lw=3, zorder=2)
    # 游标
    ax_timeline.scatter([progress], [0], color="#ffffff", edgecolor="#5470c6", s=100, lw=3, zorder=3)
    ax_timeline.text(
        progress, -0.4, str(year),
        ha="center", va="top",
        fontproperties=font_prop,
        fontsize=10,
        fontweight="bold",
        color="#5470c6"
    )
    ax_timeline.text(
        0.05, 0.35, "1960",
        ha="center", va="bottom",
        fontsize=9, color="#999999"
    )
    ax_timeline.text(
        0.95, 0.35, "2019",
        ha="center", va="bottom",
        fontsize=9, color="#999999"
    )

    plt.tight_layout()
    fig.canvas.draw()

    # 转换图像为 PIL Image
    rgba = np.asarray(fig.canvas.buffer_rgba())
    image = Image.fromarray(rgba)
    plt.close(fig)
    return image

def render_basic_timeline(output_path: str):
    """绘制基础时间线示例截图 (基础时间线柱状图.html 的点1)"""
    fig, (ax, ax_timeline) = plt.subplots(
        2, 1,
        figsize=(9, 5.2),
        gridspec_kw={"height_ratios": [8, 1.2]},
        dpi=120
    )
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    countries = ["英国", "美国", "中国"]
    gdps = [10, 20, 30]

    y_pos = np.arange(len(countries))
    bars = ax.barh(y_pos, gdps, height=0.5, color="#5470c6")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(countries, fontproperties=font_prop, fontsize=12, color="#333333")
    ax.tick_params(axis="x", labelsize=10, colors="#666666")
    ax.grid(axis="x", linestyle="--", alpha=0.5, color="#cccccc")
    ax.set_axisbelow(True)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#cccccc")

    ax.set_xlim(0, 36)
    for bar, val in zip(bars, gdps):
        ax.text(
            bar.get_width() + 0.6,
            bar.get_y() + bar.get_height() / 2,
            str(val),
            va="center",
            ha="left",
            fontsize=11,
            fontweight="bold",
            color="#444444"
        )

    ax.set_title("基础时间线柱状图测试 (点1)", fontproperties=font_prop, fontsize=16, fontweight="bold", pad=12, loc="left", color="#222222")
    ax.text(
        0.98, 1.03, "GDP",
        transform=ax.transAxes,
        fontproperties=font_prop,
        fontsize=11,
        ha="right",
        color="#666666"
    )

    # 绘制基础时间线 (点1, 点2, 点3)
    ax_timeline.set_facecolor("#ffffff")
    for spine in ax_timeline.spines.values():
        spine.set_visible(False)
    ax_timeline.set_xticks([])
    ax_timeline.set_yticks([])
    ax_timeline.set_xlim(0, 1)
    ax_timeline.set_ylim(-0.5, 0.5)

    ax_timeline.plot([0.15, 0.85], [0, 0], color="#dcdcdc", lw=3, zorder=1)
    # 3个点坐标: 0.15 (点1), 0.50 (点2), 0.85 (点3)
    points = [0.15, 0.50, 0.85]
    labels = ["点1", "点2", "点3"]

    for pt, lbl in zip(points, labels):
        is_active = (pt == 0.15)
        color = "#5470c6" if is_active else "#b0b0b0"
        ax_timeline.scatter([pt], [0], color="#ffffff" if is_active else "#b0b0b0", edgecolor=color, s=90 if is_active else 60, lw=2.5, zorder=3)
        ax_timeline.text(
            pt, -0.4, lbl,
            ha="center", va="top",
            fontproperties=font_prop,
            fontsize=10,
            fontweight="bold" if is_active else "normal",
            color=color
        )

    plt.tight_layout()
    fig.savefig(output_path, facecolor="#ffffff", edgecolor="none", dpi=120)
    plt.close(fig)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # 项目根目录
    csv_path = os.path.join(base_dir, "data", "1960-2019全球GDP数据.csv")
    screenshots_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    print("加载 GDP 数据...")
    data_dict = load_data(csv_path)
    sorted_years = sorted(data_dict.keys())

    # 1. 生成 1960 年截图
    print("生成 1960 年运行截图...")
    data_1960 = sorted(data_dict[1960], key=lambda x: x[1], reverse=True)[:8]
    data_1960.reverse()
    img_1960 = render_chart_frame(1960, data_1960, len(sorted_years), 0)
    img_1960.save(os.path.join(screenshots_dir, "1960_gdp_top8.png"))

    # 2. 生成 2019 年截图
    print("生成 2019 年运行截图...")
    data_2019 = sorted(data_dict[2019], key=lambda x: x[1], reverse=True)[:8]
    data_2019.reverse()
    img_2019 = render_chart_frame(2019, data_2019, len(sorted_years), len(sorted_years) - 1)
    img_2019.save(os.path.join(screenshots_dir, "2019_gdp_top8.png"))

    # 3. 生成基础示例截图
    print("生成基础示例截图...")
    basic_demo_path = os.path.join(screenshots_dir, "basic_timeline_demo.png")
    render_basic_timeline(basic_demo_path)

    # 4. 生成 5 秒动态演变 GIF (抽取关键年份，约 25-30 帧，形成平滑生动的动画)
    print("生成 5 秒动态演变 GIF 动画...")
    # 选取代表年份：每 2 年一帧，外加 1960 和 2019 停留延长
    frames = []
    durations = []
    
    step_years = [y for y in sorted_years if (y % 2 == 0 or y == 2019)]
    for idx, yr in enumerate(step_years):
        data_yr = sorted(data_dict[yr], key=lambda x: x[1], reverse=True)[:8]
        data_yr.reverse()
        frame_img = render_chart_frame(yr, data_yr, len(sorted_years), sorted_years.index(yr))
        frames.append(frame_img)
        # 首帧和尾帧停留更长，中间每帧约 150ms，总时长约 5 秒
        if yr == 1960:
            durations.append(900)
        elif yr == 2019:
            durations.append(1800)
        else:
            durations.append(140)

    gif_path = os.path.join(screenshots_dir, "gdp_timeline_preview.gif")
    # 量化压缩调色板，保证画质与体积兼顾
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"✅ GIF 动画生成完毕: {gif_path}")
    print("所有截图与动图生成完成！")

if __name__ == "__main__":
    main()

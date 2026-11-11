# Global GDP Visualization (1960-2019) 

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pyecharts](https://img.shields.io/badge/pyecharts-v2.0%2B-brightgreen.svg)](https://pyecharts.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

### Project Overview
This project processes historical global GDP datasets with Python and uses `pyecharts` to generate interactive dynamic timeline horizontal bar charts, showing the ranking and economic changes among the world's top 8 economies from 1960 to 2019.

### Demo & Screenshots

#### 1. Dynamic Evolution Preview (1960-2019)
![GDP Timeline Preview](screenshots/gdp_timeline_preview.gif)

#### 2. Comparison: 1960 vs 2019
| Top 8 in 1960 | Top 8 in 2019 |
| :---: | :---: |
| ![1960 Top 8](screenshots/1960_gdp_top8.png) | ![2019 Top 8](screenshots/2019_gdp_top8.png) |

#### 3. Basic Timeline Bar Test
![Basic Demo](screenshots/basic_timeline_demo.png)

### Tech Stack
* **Language:** Python 3.8+
* **Visualization:** Pyecharts (Apache ECharts)
* **Output Format:** Interactive HTML

### Files
* `data/1960-2019全球GDP数据.csv`: Historical GDP dataset.
* `1960-2019全球GDP动态柱状图.py`: Core data processing and timeline chart generation script.
* `1960-2019全球gdp前八国家.html`: Main interactive visualization output.
* `基础时间线柱状图.py`: Basic test case script for Pyecharts Timeline component.
* `基础时间线柱状图.html`: Output for the basic test case.
* `screenshots/`: Screenshots and animated GIF preview.
* `requirements.txt`: Python package requirements.

### Quick Start
```bash
# Clone repository
git clone https://github.com/Wong0813/global-gdp-visualization.git
cd global-gdp-visualization

# Install dependencies
pip install -r requirements.txt

# Run generation script
python 1960-2019全球GDP动态柱状图.py

# Open '1960-2019全球gdp前八国家.html' in any web browser.
```

### About
This project was developed as a milestone during self-learning Python data visualization, focusing on data formatting, cleaning, and combined usage of Pyecharts `Bar` and `Timeline` components.

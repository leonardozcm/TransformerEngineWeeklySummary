#!/usr/bin/env python3
"""
自动更新 GitHub Pages 主页脚本
扫描 te-summary 目录下的所有周报文件，按日期排序后更新 index.html
"""

import os
import re
from pathlib import Path
from datetime import datetime


def extract_date_from_filename(filename):
    """从文件名提取日期，用于排序"""
    # 匹配 te-weekly-report-YYYY-MM-DD-MM.html 格式
    pattern = r'te-weekly-report-(\d{4})-(\d{2})-(\d{2})-(\d{2})\.html'
    match = re.match(pattern, filename)
    if match:
        year, month, day, end_day = match.groups()
        # 返回起始日期用于排序
        return datetime(int(year), int(month), int(day))
    return datetime.min


def format_date_range(filename):
    """格式化日期范围显示"""
    pattern = r'te-weekly-report-(\d{4})-(\d{2})-(\d{2})-(\d{2})\.html'
    match = re.match(pattern, filename)
    if match:
        year, month, start_day, end_day = match.groups()
        return f"{year}-{month}-{start_day} ~ {month}-{end_day}"
    return filename


def get_week_number(filename):
    """计算周数"""
    date = extract_date_from_filename(filename)
    if date != datetime.min:
        return date.isocalendar()[1]
    return 0


def get_relative_time(date):
    """获取相对时间描述"""
    now = datetime.now()
    diff = now - date
    days = diff.days
    
    if days == 0:
        return "今天"
    elif days == 1:
        return "昨天"
    elif days < 7:
        return f"{days} 天前"
    elif days < 14:
        return "1 周前"
    elif days < 21:
        return "2 周前"
    elif days < 30:
        return "3 周前"
    elif days < 60:
        return "1 个月前"
    else:
        return f"{days // 30} 个月前"


def generate_index_html(reports):
    """生成 index.html 内容"""
    if not reports:
        return ""
    
    latest_report = reports[0]
    latest_path = f"./te-summary/{latest_report['filename']}"
    
    # 生成近期报告列表（最多5个）
    report_items = []
    for i, report in enumerate(reports[:5]):
        date_range = format_date_range(report['filename'])
        week_num = get_week_number(report['filename'])
        path = f"./te-summary/{report['filename']}"
        
        if i == 0:
            badge = '<span class="badge-latest">最新</span>'
        else:
            relative_time = get_relative_time(report['date'])
            badge = f'<span class="report-date">{relative_time}</span>'
        
        item = f'''      <li class="report-item">
        <a href="{path}">
          <span>{date_range} (W{week_num})</span>
          {badge}
        </a>
      </li>'''
        report_items.append(item)
    
    report_list_html = '\n'.join(report_items)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="0; url={latest_path}">
<title>Transformer Engine Weekly Summary</title>
<style>
  :root {{
    --bg: #0d1117;
    --card: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --text-muted: #8b949e;
    --link: #58a6ff;
    --green: #76b900;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px 20px;
  }}
  .container {{
    text-align: center;
    max-width: 600px;
  }}
  .logo {{
    font-size: 3em;
    margin-bottom: 16px;
  }}
  h1 {{
    font-size: 1.8em;
    margin-bottom: 8px;
    color: var(--green);
  }}
  .subtitle {{
    color: var(--text-muted);
    font-size: 1em;
    margin-bottom: 32px;
  }}
  .loading {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--text-muted);
    font-size: 0.9em;
  }}
  .spinner {{
    width: 16px;
    height: 16px;
    border: 2px solid var(--border);
    border-top-color: var(--green);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }}
  @keyframes spin {{
    to {{ transform: rotate(360deg); }}
  }}
  .redirect-notice {{
    margin-top: 16px;
    font-size: 0.85em;
    color: var(--text-muted);
  }}
  .redirect-notice a {{
    color: var(--link);
    text-decoration: none;
  }}
  .redirect-notice a:hover {{
    text-decoration: underline;
  }}
  .recent-reports {{
    margin-top: 48px;
    padding-top: 32px;
    border-top: 1px solid var(--border);
    width: 100%;
  }}
  .recent-reports h2 {{
    font-size: 1em;
    color: var(--text-muted);
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}
  .report-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .report-item {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    transition: border-color 0.2s;
  }}
  .report-item:hover {{
    border-color: var(--green);
  }}
  .report-item a {{
    color: var(--text);
    text-decoration: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .report-item a:hover {{
    color: var(--link);
  }}
  .report-date {{
    font-size: 0.85em;
    color: var(--text-muted);
  }}
  .badge-latest {{
    background: rgba(118,185,0,0.15);
    color: var(--green);
    border: 1px solid rgba(118,185,0,0.3);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: 600;
  }}
</style>
</head>
<body>

<div class="container">
  <div class="logo">📊</div>
  <h1>Transformer Engine Weekly</h1>
  <div class="subtitle">GitHub Repository Weekly Tracking Report</div>
  
  <div class="loading">
    <div class="spinner"></div>
    <span>正在跳转到最新周报...</span>
  </div>
  
  <div class="redirect-notice">
    如果没有自动跳转，请 <a href="{latest_path}">点击这里</a>
  </div>

  <div class="recent-reports">
    <h2>近期周报</h2>
    <ul class="report-list">
{report_list_html}
    </ul>
  </div>
</div>

</body>
</html>'''
    return html


def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    summary_dir = script_dir / 'te-summary'
    
    if not summary_dir.exists():
        print(f"错误: 目录 {summary_dir} 不存在")
        return 1
    
    # 扫描所有周报文件
    reports = []
    for file in summary_dir.glob('te-weekly-report-*.html'):
        date = extract_date_from_filename(file.name)
        reports.append({
            'filename': file.name,
            'date': date,
            'path': file
        })
    
    # 按日期降序排序（最新的在前）
    reports.sort(key=lambda x: x['date'], reverse=True)
    
    if not reports:
        print("未找到任何周报文件")
        return 1
    
    # 生成新的 index.html
    html_content = generate_index_html(reports)
    
    # 写入文件
    index_path = script_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 已更新 {index_path}")
    print(f"📊 共找到 {len(reports)} 个周报")
    print(f"🆕 最新周报: {reports[0]['filename']}")
    
    return 0


if __name__ == '__main__':
    exit(main())

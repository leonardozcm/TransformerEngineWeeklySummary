#!/usr/bin/env python3
"""
自动更新 index.html 中的 reportFiles 数组
扫描 te-summary 目录下的所有周报文件，按日期排序后更新 index.html
"""

import os
import re
from pathlib import Path


def extract_date_from_filename(filename):
    """从文件名提取日期，用于排序
    
    匹配格式: te-weekly-report-YYYY-MM-DD.html
    """
    pattern = r'te-weekly-report-(\d{4})-(\d{2})-(\d{2})\.html'
    match = re.match(pattern, filename)
    if match:
        year, month, day = match.groups()
        # 返回 (year, month, day) 元组用于排序
        return (int(year), int(month), int(day))
    return None


def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    summary_dir = script_dir / 'te-summary'
    index_path = script_dir / 'index.html'
    
    if not summary_dir.exists():
        print(f"错误: 目录 {summary_dir} 不存在")
        return 1
    
    if not index_path.exists():
        print(f"错误: 文件 {index_path} 不存在")
        return 1
    
    # 扫描所有周报文件
    report_files = []
    for file in summary_dir.glob('te-weekly-report-*.html'):
        date = extract_date_from_filename(file.name)
        if date:
            report_files.append((date, file.name))
    
    if not report_files:
        print("未找到任何周报文件")
        return 1
    
    # 按日期降序排序（最新的在前）
    report_files.sort(key=lambda x: x[0], reverse=True)
    
    # 生成新的 reportFiles 数组内容
    file_list = [f"    '{filename}'" for _, filename in report_files]
    new_array_content = "[\n" + ",\n".join(file_list) + "\n  ]"
    
    # 读取 index.html 内容
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则替换 reportFiles 数组
    # 匹配 const reportFiles = [...] 中的数组部分
    pattern = r"(const reportFiles\s*=\s*)\[[\s\S]*?\]"
    replacement = r"\1" + new_array_content
    
    new_content = re.sub(pattern, replacement, content)
    
    # 检查是否成功替换
    if new_content == content:
        print("警告: 未能找到或替换 reportFiles 数组")
        return 1
    
    # 写回文件
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已更新 {index_path}")
    print(f"📊 共找到 {len(report_files)} 个周报")
    print(f"🆕 最新周报: {report_files[0][1]}")
    
    return 0


if __name__ == '__main__':
    exit(main())

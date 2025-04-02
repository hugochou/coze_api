"""
测试文件路径和数据目录
"""

import os
from pathlib import Path
import sys

def main():
    # 当前工作目录
    cwd = os.getcwd()
    print(f"当前工作目录: {cwd}")
    
    # 直接访问data目录
    data_dir = Path(cwd) / 'data'
    print(f"数据目录: {data_dir}")
    print(f"数据目录是否存在: {data_dir.exists()}")
    
    if data_dir.exists():
        print("数据目录内容:")
        for item in data_dir.iterdir():
            if item.is_dir():
                print(f"  目录: {item.name}")
                # 列出子目录内容
                for subitem in item.iterdir():
                    if subitem.is_file():
                        print(f"    文件: {subitem.name}, 大小: {subitem.stat().st_size} 字节")
    
    # 检查特定目录
    for dirname in ['uploads', 'audio', 'output']:
        dir_path = data_dir / dirname
        print(f"\n{dirname}目录: {dir_path}")
        print(f"{dirname}目录是否存在: {dir_path.exists()}")
        
        if dir_path.exists():
            files = [f for f in dir_path.glob('*') if f.is_file() and not f.name.startswith('.')]
            print(f"{dirname}目录中有 {len(files)} 个非隐藏文件:")
            for f in files:
                print(f"  {f.name}: {f.stat().st_size} 字节")

if __name__ == "__main__":
    main() 
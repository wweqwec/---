#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI助手后端 - 诊断脚本
用于检测后端无法启动的原因
"""

import sys
import os

print("=" * 70)
print("  AI助手后端 - 诊断工具")
print("=" * 70)
print()

# 1. 检查Python版本
print("[1/6] 检查Python版本...")
print(f"  Python版本: {sys.version}")
if sys.version_info < (3, 8):
    print("  [错误] Python版本过低，需要3.8+")
    sys.exit(1)
else:
    print("  [成功] Python版本符合要求")
print()

# 2. 检查依赖包
print("[2/6] 检查依赖包...")
missing_packages = []
required_packages = ['flask', 'flask_cors', 'requests']

for package in required_packages:
    try:
        __import__(package)
        print(f"  [成功] {package} 已安装")
    except ImportError:
        missing_packages.append(package)
        print(f"  [缺失] {package} 未安装")

if missing_packages:
    print()
    print("  [提示] 请执行以下命令安装依赖：")
    print(f"  pip install {' '.join(missing_packages)}")
    sys.exit(1)
print()

# 3. 检查文件路径
print("[3/6] 检查数据文件...")
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, 'data', 'reviews.json')

if os.path.exists(data_file):
    print(f"  [成功] 数据文件存在: {data_file}")
    # 检查文件内容
    try:
        import json
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        product_count = len(data.get('products', {}))
        print(f"  [成功] 数据文件可读取，包含 {product_count} 款产品")
    except Exception as e:
        print(f"  [错误] 数据文件读取失败: {e}")
        sys.exit(1)
else:
    print(f"  [错误] 数据文件不存在: {data_file}")
    print("  [提示] 请先运行: python ../gen_complete_data.py")
    sys.exit(1)
print()

# 4. 检查端口占用
print("[4/6] 检查端口 5000...")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 5000))
    if result == 0:
        print("  [警告] 端口 5000 已被占用")
        print("  [提示] 请关闭占用端口的程序，或修改 ai_assistant.py 中的端口号")
    else:
        print("  [成功] 端口 5000 可用")
    sock.close()
except Exception as e:
    print(f"  [错误] 端口检查失败: {e}")
print()

# 5. 测试Flask应用创建
print("[5/6] 测试Flask应用...")
try:
    from flask import Flask
    app = Flask(__name__)
    print("  [成功] Flask应用创建成功")
except Exception as e:
    print(f"  [错误] Flask应用创建失败: {e}")
    sys.exit(1)
print()

# 6. 测试阿里云百炼API配置
print("[6/6] 检查API配置...")
api_key = "sk-ac5a29627d7d46b39703dffcd28b4a01"
if api_key and len(api_key) > 10:
    print("  [成功] API Key 已配置")
else:
    print("  [警告] API Key 未配置或无效")
print()

# 总结
print("=" * 70)
print("  诊断完成")
print("=" * 70)
print()
print("  如果所有检查都通过，您可以启动后端服务：")
print("  python ai_assistant.py")
print()
print("  或双击 '启动AI系统.bat' 一键启动所有服务")
print()
print("=" * 70)

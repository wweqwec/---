#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动AI助手系统 - 同时启动前端和后端服务
"""

import subprocess
import sys
import time
import os
import signal
from threading import Thread

# 获取当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 进程列表
processes = []

def start_backend():
    """启动后端AI助手服务"""
    print("=" * 70)
    print("  启动后端AI助手服务 (端口 5000)")
    print("=" * 70)
    
    backend_script = os.path.join(BASE_DIR, 'ai_assistant.py')
    
    try:
        proc = subprocess.Popen(
            [sys.executable, backend_script],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(proc)
        
        # 实时输出后端日志
        for line in proc.stdout:
            print(f"[后端] {line.rstrip()}")
            
    except Exception as e:
        print(f"[错误] 启动后端服务失败: {e}")


def start_frontend():
    """启动前端HTTP服务器 (端口 8000)"""
    time.sleep(2)  # 等待后端启动
    
    print("\n" + "=" * 70)
    print("  启动前端HTTP服务器 (端口 8000)")
    print("=" * 70)
    
    try:
        proc = subprocess.Popen(
            [sys.executable, '-m', 'http.server', '8000'],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(proc)
        
        print("\n" + "=" * 70)
        print("  [成功] 系统启动成功！")
        print("=" * 70)
        print("\n  访问地址：")
        print("  前端页面: http://localhost:8000")
        print("  AI助手API: http://localhost:5000/api/health")
        print("\n  功能说明：")
        print("  1. 在首页选择手机品牌和型号")
        print("  2. 在AI助手面板输入问题，获取智能推荐")
        print("  3. 示例问题：'3000元预算推荐哪款手机？'")
        print("\n  按 Ctrl+C 停止所有服务\n")
        print("=" * 70 + "\n")
        
        # 实时输出前端日志
        for line in proc.stdout:
            print(f"[前端] {line.rstrip()}")
            
    except Exception as e:
        print(f"[错误] 启动前端服务失败: {e}")


def signal_handler(sig, frame):
    """处理退出信号"""
    print("\n\n[系统] 正在停止服务...")
    
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except:
            proc.kill()
    
    print("[系统] 所有服务已停止")
    sys.exit(0)


def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("\n" + "=" * 70)
    print("  [系统] 智能手机评价分析系统 - AI助手版")
    print("=" * 70)
    print("\n  正在启动服务...\n")
    
    # 启动后端线程
    backend_thread = Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # 启动前端（主线程）
    start_frontend()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
OpenClaw Gateway 守护进程
适用于 WSL 和 Linux 环境
"""

import subprocess
import time
import os
import sys
import signal
import psutil

PID_FILE = "/tmp/gateway-guardian.pid"
LOG_FILE = "/tmp/gateway-guardian.log"

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def get_gateway_pid():
    """获取 Gateway 进程 PID"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'openclaw-gateway' in proc.info['name']:
                return proc.info['pid']
        except:
            pass
    return None

def is_gateway_running():
    """检查 Gateway 是否在运行"""
    return get_gateway_pid() is not None

def start_gateway():
    """启动 Gateway"""
    try:
        env = os.environ.copy()
        env["PATH"] = "/home/zx/.nvm/versions/node/v24.13.1/bin:" + env.get("PATH", "")
        
        proc = subprocess.Popen(
            ["openclaw", "gateway", "start"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd="/home/zx/.openclaw/workspace",
            env=env,
            start_new_session=True
        )
        return proc.pid
    except Exception as e:
        log(f"启动失败: {e}")
        return None

def stop_gateway():
    """停止 Gateway"""
    pid = get_gateway_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)
            if is_gateway_running():
                os.kill(pid, signal.SIGKILL)
            log(f"Gateway 已停止 (PID: {pid})")
        except Exception as e:
            log(f"停止失败: {e}")
    else:
        log("Gateway 未运行")

def daemon_loop():
    """守护循环"""
    log("=" * 50)
    log("Gateway 守护进程启动")
    log("=" * 50)
    
    while True:
        try:
            if not is_gateway_running():
                log("Gateway 离线，正在启动...")
                pid = start_gateway()
                if pid:
                    time.sleep(5)
                    if is_gateway_running():
                        new_pid = get_gateway_pid()
                        log(f"Gateway 启动成功 (PID: {new_pid})")
                    else:
                        log("Gateway 启动失败")
                else:
                    log("启动命令执行失败")
            
            time.sleep(10)
        except KeyboardInterrupt:
            log("收到中断信号，守护进程退出")
            break
        except Exception as e:
            log(f"错误: {e}")
            time.sleep(10)

def write_pid():
    """写入 PID 文件"""
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

def remove_pid():
    """删除 PID 文件"""
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

def is_already_running():
    """检查是否已有守护进程在运行"""
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            if psutil.pid_exists(old_pid):
                return True
        except:
            pass
    return False

def main():
    if len(sys.argv) < 2:
        print("用法: guardian.py [start|stop|status]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "start":
        if is_already_running():
            print("守护进程已在运行")
            sys.exit(0)
        
        # 后台运行
        if os.fork():
            sys.exit(0)
        
        write_pid()
        try:
            daemon_loop()
        finally:
            remove_pid()
    
    elif cmd == "stop":
        if os.path.exists(PID_FILE):
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
            try:
                os.kill(pid, signal.SIGTERM)
                remove_pid()
                print("守护进程已停止")
            except:
                print("守护进程未运行")
        else:
            print("守护进程未运行")
        stop_gateway()
    
    elif cmd == "status":
        if is_already_running():
            print("守护进程: 运行中")
        else:
            print("守护进程: 未运行")
        
        if is_gateway_running():
            pid = get_gateway_pid()
            print(f"Gateway: 运行中 (PID: {pid})")
        else:
            print("Gateway: 未运行")
    
    else:
        print(f"未知命令: {cmd}")
        print("用法: guardian.py [start|stop|status]")

if __name__ == "__main__":
    main()

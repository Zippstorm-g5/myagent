#!/bin/bash

# 检查是否提供了参数
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <token>"
    exit 1
fi

# 将提供的参数赋值给一个变量
TOKEN=$1

# 更新包列表并安装所需包
apt update && apt install wget curl python3 python3-requests python3-netifaces -y

# 下载Python脚本，赋予执行权限并执行
wget -L https://raw.githubusercontent.com/Zippstorm-g5/myagent/main/main.py
chmod +x main.py
python3 main.py https://monitor.zippstorm.com/api/v1/server $TOKEN

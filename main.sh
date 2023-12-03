#!/bin/bash

# 检查是否提供了足够的参数
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <server_url> <token>"
    exit 1
fi

# 将提供的参数赋值给变量
SERVER_URL=$1
TOKEN=$2

# 更新包列表并安装所需包
apt update && apt install wget curl python3 python3-requests python3-netifaces -y

# 下载Python脚本，赋予执行权限并执行
wget -OL https://raw.githubusercontent.com/Zippstorm-g5/myagent/main/main.py
chmod +x main.py
python3 main.py $SERVER_URL $TOKEN

import requests
import random
import string
import json
import sys
import os

def display_options(options):
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def find_missing_value(dict_list):
    # 将所有 "id" 的值加入一个集合
    id_values = set()
    for d in dict_list:
        if "displayindex" in d:
            id_value = d["displayindex"]
            if isinstance(id_value, int) and id_value <= 1000:
                id_values.add(id_value)

    # 从 0 开始逐个查找缺失的值
    missing_value = None
    for i in range(1001):  # 假设最大值为 1000
        if i not in id_values:
            missing_value = i
            break
    tags = list(set([d["tag"] for d in dict_list if "tag" in d]))
    return missing_value,tags


def jsondata(url,headers):
    data = {
        "ID": 0, #新添加所以ID为0
        "Name": "test",
        "DisplayIndex": 6000,
        "Secret": 'qL6r8aaGw6PdyYzpAh',
        "Tag": '测试',
        "Note": "测试",
        "HideForGuest ": "off",
    }
    datas = requests.get(url+"/list", headers=headers).json()["result"]
    missvalue,groups = find_missing_value(datas)
    groupsnum=len(groups)
    groups.append('新建组')
    data['DisplayIndex']=missvalue
    secret=generate_random_string(20)
    data['Secret']=secret
    data['Name'] = input("请输入服务器名：")
    while True:
        display_options(groups)
        choice = input("请选择服务器组：")
        choice_index = int(choice) - 1
        if 0 <= choice_index < groupsnum:
            data['Tag'] = groups[choice_index]
            break
        elif choice_index==groupsnum:
            data['Tag']=input("请输入服务器组名：")
            break
        else:
            pass
    data['Note'] = input("请输入服务器备注（回车为空）：")
    guest=input("请输入游客可见性（回车为Y/n,默认Y）：")
    if guest=='N' or 'n':
        data['HideForGuest'] = "on"
    else:
        data['HideForGuest'] = "off"
    json_data = json.dumps(data)
    return secret,json_data



if __name__ == "__main__":
    args = sys.argv[1:]
    url = args[0]
    token=args[1]

    headers = {
        "Authorization": token
    }

    secret,json_data=jsondata(url,headers)
    response = requests.post(url, data=json_data, headers=headers)

    if args[2]==None:
        interface=' '
    else:
        interface=args[2]
    command = "curl -L https://raw.githubusercontent.com/Zippstorm-g5/myagent/main/myagent.sh -o nezha.sh && " \
              "chmod +x nezha.sh && ./nezha.sh install_agent example.com 5555 %s %s --tls" % (secret, interface)
    os.system(command)

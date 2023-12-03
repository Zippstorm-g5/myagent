import netifaces
import requests
import random
import string
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

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
        "Tag": 'test',
        "Note": "test",
        "HideForGuest ": "off",
    }
    datas = requests.get(url+"/list", headers=headers).json()["result"]
    missvalue,groups = find_missing_value(datas)
    groupsnum=len(groups)
    groups.append('New group')
    data['DisplayIndex']=missvalue
    secret=generate_random_string(18)
    data['Secret']=secret
    data['Name'] = input("Key in a server name:")
    while True:
        display_options(groups)
        choice = input("Select a server group:")
        choice_index = int(choice) - 1
        if 0 <= choice_index < groupsnum:
            data['Tag'] = groups[choice_index]
            break
        elif choice_index==groupsnum:
            data['Tag']=input("Key in a server group name:")
            break
        else:
            pass
    data['Note'] = input("Key in the note:")
    guest=input("Show For Guest? default：Y")
    if guest in ['N', 'n']:
        data['HideForGuest'] = "on"
    else:
        data['HideForGuest'] = "off"
    json_data = json.dumps(data)
    return secret,json_data



if __name__ == "__main__":
    url = os.getenv('SERVER_URL')
    token = os.getenv('TOKEN')
    
    headers = {
        "Authorization": token
    }
    interface_list = netifaces.interfaces()
    display_options(interface_list)
    num = input("Select an interface:")
    index = int(num) - 1
    if 0 <= index < len(interface_list):
        interface = interface_list[index]
    else:
        interface=''
    
    secret,json_data=jsondata(url,headers)
    response = requests.post(url, data=json_data, headers=headers)

    command = "curl -L https://raw.githubusercontent.com/Zippstorm-g5/myagent/main/myagent.sh -o nezha.sh && " \
              "chmod +x nezha.sh && ./nezha.sh install_agent example.com 5555 %s %s --tls" % (secret, interface)
    os.system(command)
    command ="systemctl restart nezha-agent2"
    os.system(command)

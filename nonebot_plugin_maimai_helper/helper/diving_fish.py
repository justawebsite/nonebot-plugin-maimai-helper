import json

import requests
from nonebot_plugin_maimai_helper.data import root_path

URL = "https://www.diving-fish.com/api/maimaidxprober/player/update_records"


def sega_data_pre_format(sega_data):
    with open(root_path + '/game_data/diving_music_list.json', 'r', encoding='utf-8') as file:
        music_list = json.load(file)
    for old in sega_data:
        old['title'] = None
        old['type'] = None
        for music in music_list:
            if music['id'] == f"{old['musicId']}":
                old['title'] = music['title']
                old['type'] = music['type']
        if old['comboStatus'] == 0:
            old['comboStatus'] = ""
        elif old['comboStatus'] == 1:
            old['comboStatus'] = "fc"
        elif old['comboStatus'] == 2:
            old['comboStatus'] = "fcp"
        elif old['comboStatus'] == 3:
            old['comboStatus'] = "ap"
        elif old['comboStatus'] == 4:
            old['comboStatus'] = "app"
        else:
            old['comboStatus'] = ""
        if old['syncStatus'] == 0:
            old['syncStatus'] = ""
        elif old['syncStatus'] == 1:
            old['syncStatus'] = "fs"
        elif old['syncStatus'] == 2:
            old['syncStatus'] = "fsp"
        elif old['syncStatus'] == 3:
            old['syncStatus'] = "fsd"
        elif old['syncStatus'] == 4:
            old['syncStatus'] = "fsdp"
        elif old['syncStatus'] == 5:
            old['syncStatus'] = "sync"
        else:
            old['syncStatus'] = ""
    return sega_data


def change_data(sega_data):
    sega_data = sega_data_pre_format(sega_data)
    print(sega_data)
    diving_fish_data = []
    count = 0
    for old in sega_data:
        if old['title'] == None:
            continue
        diving_fish_data.append({
            "achievements": old['achievement'] / 10000.0,
            "dxScore": old['deluxscoreMax'],
            "fc": old['comboStatus'],
            "fs": old['syncStatus'],
            "level_index": old['level'],
            "title": old['title'],
            "type": old['type'],
        })
        count += 1

    return diving_fish_data, count


def send_user_data(data, token):
    back = {"status": None, "msg": None}
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    headers = {
        "Import-Token": token,
        "Content-Type": "application/json"
    }
    try:
        request = requests.post(URL, headers=headers, data=data.encode('utf-8'))
        request.encoding = 'utf-8'
        back['status'] = request.status_code
        back['msg'] = json.loads(request.text)
        return back
    except Exception as e:
        back['status'] = 0
        back['msg'] = str(e)
        return back



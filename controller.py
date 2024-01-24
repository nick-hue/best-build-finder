import requests
from bs4 import BeautifulSoup
from collections import Counter
import json 
import urllib.request
from PIL import ImageTk, Image
import customtkinter as ctk
import io

def get_matches(depth, champion_id):
    matches = []

    for current_depth in range(depth):
    
        headers = {
            'authority': 'u.gg',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': '',
            'content-type': 'application/json',
            'origin': 'https://probuildstats.com',
            'referer': 'https://probuildstats.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        json_data = {
            'operationName': 'ChampionMatchList',
            'variables': {
                'championId': champion_id,
                'isOtp': False,
                'pageNumber': current_depth,
            },
            'query': 'query ChampionMatchList($championId: Int, $league: String, $recommendedFirst: Boolean, $role: String, $victoryOnly: Boolean, $opponentChampionId: Int, $leagueBlocklist: [String], $teamBlocklist: [String], $proBlocklist: [String], $pageNumber: Int, $isWorlds: Boolean, $isOtp: Boolean, $proTeam: String) {\n  getProChampionMatchList(\n    championId: $championId\n    league: $league\n    recommendedFirst: $recommendedFirst\n    role: $role\n    victoryOnly: $victoryOnly\n    opponentChampionId: $opponentChampionId\n    leagueBlocklist: $leagueBlocklist\n    teamBlocklist: $teamBlocklist\n    proBlocklist: $proBlocklist\n    pageNumber: $pageNumber\n    isWorlds: $isWorlds\n    isOtp: $isOtp\n    proTeam: $proTeam\n  ) {\n    matchList {\n      calculatedRole\n      championId\n      cs\n      completedItems\n      currentTeam\n      finalBuild\n      gold\n      itemPath {\n        itemId\n        timestamp\n        type\n        __typename\n      }\n      jungleCs\n      killParticipation\n      matchDuration\n      matchId\n      isWorlds\n      matchTimestamp\n      normalizedName\n      proInfo {\n        league\n        mainRole\n        currentTeam\n        officialName\n        tags\n        region\n        __typename\n      }\n      opponentChampionId\n      proLeague\n      regionId\n      runes {\n        perk0\n        perk1\n        perk2\n        perk3\n        perk4\n        perk5\n        primaryStyle\n        subStyle\n        __typename\n      }\n      riotUserName\n      riotTagLine\n      statShards\n      seasonId\n      skillEvolveOrders\n      skillOrders\n      summonerSpells\n      teamId\n      totalAssists\n      totalDeaths\n      totalKills\n      version\n      win\n      __typename\n    }\n    mostPopularItems {\n      itemId\n      pickRate\n      __typename\n    }\n    mostPopularBoots {\n      itemId\n      pickRate\n      __typename\n    }\n    __typename\n  }\n}',
        }

        try:
            response = requests.post('https://u.gg/api', headers=headers, json=json_data).json()
            current_matches = response['data']['getProChampionMatchList']['matchList']
            for match in current_matches:
                matches.append(match)

        except Exception as e:
            print(f"Error getting matches: {e}")
            return None
        

    return matches

def get_item_ids_to_json():
    response = requests.get("https://darkintaqt.com/blog/item-ids")
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('div', class_ = 'table')
    items = table.find_all('td')

    items_dict = {}
    for i in range(0, len(items), 3):
        if len(items[i].text) > 4:
            items_dict[int(items[i].text[2:])] = items[i+2].text
        else:
            items_dict[int(items[i].text)] = items[i+2].text

    with open("item_ids.json", "w") as outfile: 
        json.dump(items_dict, outfile)

def get_items_count(matches, items_dict):
    all_items = []
    for match in matches:
        #print(match['finalBuild'])
        for item in match['completedItems']:
            if item == 0:
                continue
            #print(item, items_dict[item])
            all_items.append(items_dict[str(item)])
        #print()
            
    #print(all_items)
    remove_list = ["Berserker's Greaves", "Boots of Swiftness", "Ionian Boots of Lucidity", "Mercury's Treads", \
                   "Mobility Boots", "Plated Steelcaps", "Sorcerer's Shoes"]
    result = [i for i in all_items if i not in remove_list]
    #print(result)
    count = dict(Counter(result))
    return {k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}

def get_champion_ids_json():
    with open('id_data.txt', 'r') as f:
        data = f.readlines()

    my_dict = {}

    for line in data:
        line_info = line.strip().replace("\t", " ").split(" ")
        print("len=",len(line_info))
        id = line_info[0]
        
        data_length = len(line_info)

        if 4 < data_length < 8 :
            name = line_info[1] + " " + line_info[2]
        elif data_length == 8:
            name = line_info[1] + " " + line_info[2] + " " + line_info[3]
        else: 
            name = line_info[1]

        # print(f"ID: {id}, Name: {name}")

        my_dict[name] = id

    # print(my_dict)

    with open("champion_ids.json", "w") as outfile: 
        json.dump(my_dict, outfile)

def get_champion_image(champion_name):
    print(f"Champ id: {champion_name}")
    highfen = "'"
    url = f"https://cdn.lolrift.com/img/champion/tiles/{champion_name.replace(' ', '').replace(highfen, '')}_0.webp"

    try:
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

    try:
        image = Image.open(io.BytesIO(raw_data))
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    img = ctk.CTkImage(light_image=image, dark_image=image, size=((188, 212)))

    return img

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def get_build_image(items, ITEMS_IDS):
    images = []
    for item in list(items.keys())[:8]:
        
        id = list(ITEMS_IDS.keys())[list(ITEMS_IDS.values()).index(item)]

        url = f"https://cdn.darkintaqt.com/lol/c-assets/items/{id}.png.webp"
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = urllib.request.Request(url=url, headers=headers)

        try:
            with urllib.request.urlopen(req) as u:
                raw_data = u.read()
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None

        try:
            image = Image.open(io.BytesIO(raw_data))
        except Exception as e:
            print(f"Error opening image: {e}")
            return None
        
        images.append(image)

    tmp1 = get_concat_h(images[0], images[1])
    tmp1 = get_concat_h(tmp1, images[2])
    tmp1 = get_concat_h(tmp1, images[3])
    #tmp1.show()

    tmp2 = get_concat_h(images[4], images[5])
    tmp2 = get_concat_h(tmp2, images[6])
    tmp2 = get_concat_h(tmp2, images[7])
    #tmp2.show()

    tmp_result = get_concat_v(tmp1, tmp2)
    
    result = ctk.CTkImage(light_image=tmp_result, dark_image=tmp_result, size=((250, 175)))

    return result

def load_json(json_filename):
    with open(json_filename) as json_file:
        data = json.load(json_file)

    return data
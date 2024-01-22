import requests
from bs4 import BeautifulSoup
from collections import Counter
import json 

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

        response = requests.post('https://u.gg/api', headers=headers, json=json_data).json()
        current_matches = response['data']['getProChampionMatchList']['matchList']
        for match in current_matches:
            matches.append(match)

    return matches

def get_item_ids():
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

    return items_dict

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
            
    count = dict(Counter(all_items))
    return {k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}

def get_champion_ids():
    with open("id_data.txt", "r") as f:
        data = f.readlines()

    my_dict = {}

    for item in data:
        info = item.split(" ")
        # print(info)
        if len(info) > 5:
            _, current_id, _, name, name2, _ = item.split(" ")
            final_name = name.replace('"', "").replace(";","") + " " + name2.replace('"', "").replace(";","")

        else:
            _, current_id, _, name, _ = item.split(" ")
            final_name = name.replace('"', "").replace(";","")

        final_id = current_id.replace(":", "")

        #print(f"ID: {final_id:>4}| Name: {final_name}")

        my_dict[final_name] = final_id

    myKeys = list(my_dict.keys())
    myKeys.sort()
    sorted_dict = {i: my_dict[i] for i in myKeys}

    return sorted_dict

def get_champion_ids_json():
    with open("id_data.txt", "r") as f:
        data = f.readlines()

    my_dict = {}

    for item in data:
        info = item.split(" ")
        # print(info)
        if len(info) > 5:
            _, current_id, _, name, name2, _ = item.split(" ")
            final_name = name.replace('"', "").replace(";","") + " " + name2.replace('"', "").replace(";","")

        else:
            _, current_id, _, name, _ = item.split(" ")
            final_name = name.replace('"', "").replace(";","")

        final_id = current_id.replace(":", "")

        #print(f"ID: {final_id:>4}| Name: {final_name}")

        my_dict[final_name] = final_id

    myKeys = list(my_dict.keys())
    myKeys.sort()
    sorted_dict = {i: my_dict[i] for i in myKeys}

    with open("champion_ids.json", "w") as outfile: 
        json.dump(sorted_dict, outfile)

def load_json(json_filename):
    with open(json_filename) as json_file:
        data = json.load(json_file)

    return data
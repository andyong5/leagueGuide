import json
import requests
import sys
import string


def getSummonerID(region, summonerName, APIKey):
    url = "https://" + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + \
        summonerName + '?api_key=' + APIKey
    response = requests.get(url)
    response.status_code
    data = json.loads(response.content)
    return data["accountId"]


def getTop3Mastery(region, APIKey, summonerID):
    url = "https://" + region + '.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + \
        summonerID + "?api_key=" + APIKey
    response = requests.get(url)
    response.status_code
    data = json.loads(response.content)
    i = 0
    for i in range(3):
        print("champion id =" + str(data[i]["championId"]) +
              " and champion Mastery = " + str(data[i]["championPoints"]))


'''
def getAccountID(region, summonerName, APIKey):
    url = "https://" + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' +
        summonerName + '?api_key=' + APIKey
    response = requests.get(url)
    response.status_code
    data = json.loads(response.content)
    return data["accountId"]
'''


def getSummonerIDjson(region, summonerID, APIKey):
    url = "https://" + region + '.api.riotgames.com/lol/summoner/v4/summoners/' + \
        summonerName + '?api_key=' + APIKey
    response = requests.get(url)
    if(response.status_code != requests.codes.ok):
        return
    data = json.loads(response.content)
    return data["summonerLevel"]


def getChampionRotation(region, APIKey):
    url = "https://" + region + \
        '.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=' + APIKey
    response = requests.get(url)
    if(response.status_code != requests.codes.ok):
        return
    data = json.loads(response.content)
    return data


def printCurrentRankings(region, APIKey, queueType, tier, division):
    url = "https://" + region + ".api.riotgames.com/lol/league-exp/v4/entries/" + \
        queueType + "/" + tier + "/" + division + "?page=1&api_key=" + apiKey
    response = requests.get(url)
    if(response.status_code != requests.codes.ok):
        return
    data = json.loads(response.content)
    i = 0
    for i in range(len(data)):
        winRatio = (data[i]["wins"] /
                    (data[i]["wins"] + data[i]["losses"])) * 100
        print(str(i + 1) + '. ' + data[i]["summonerName"] + " with " +
              str(data[i]["leaguePoints"]) +
              " League Points with " + str(data[i]["wins"])
              + " wins and " +
              str(data[i]["losses"]) + " losses and with a win ratio of " +
              str(int(round(winRatio, 0))) + "%")


def addSpaceInName(name):
    if ' ' in name:
        for i in name:
            name = name.replace(" ", "%20")
    return name


def getRankData(region, APIKey, summonerID):
    url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + \
        summonerID + "?page=1&api_key=" + apiKey
    response = requests.get(url)
    response.status_code
    return json.loads(response.content)


apiKey = "RGAPI-61d4746c-5157-4888-923e-320ac18fdd9c"
region = "na1"


nameInput = input("Please enter your summoner name: ")

summonerName = addSpaceInName(nameInput)

print(summonerName)
summonerID = getSummonerID(region, summonerName, apiKey)
print(summonerID)

'''
printCurrentRankings(region, apiKey, "RANKED_SOLO_5x5", "CHALLENGER", "I")
'''

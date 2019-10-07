import json
import requests
import sys
import string


def getMatchID(region, accountId, apiKey, endIndex):
    url = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + \
        accountId + "?endindex=" + endIndex + "&api_key=" + apiKey
    response = requests.get(url)
    response.status_code
    return json.loads(response.content)


def getMatchInfo(region, matchID, apiKey):
    url = "https://" + region + \
        ".api.riotgames.com/lol/match/v4/matches/" + \
        str(matchID) + "?api_key=" + apiKey
    response = requests.get(url)
    response.status_code
    return json.loads(response.content)


apiKey = "RGAPI-76583f7d-fd65-4dec-8230-eb7c01260b5e"
region = "na1"
accountId = "crnmuXAtH_NDGZ4QPI1Tx8S5qVoiEu471YjMriXh8UcwMw"
data = getMatchID("na1", accountId, apiKey, str(10))
print(data["matches"][0]["gameId"])
matchID = data["matches"][0]["gameId"]
matchInfo = getMatchInfo(region, matchID, apiKey)
individualMatchInfo = []
x = 0
for x in range(len(data)):
    individualMatchInfo.append(getMatchInfo(
        region, data["matches"][x]["gameId"], apiKey))
print(len(individualMatchInfo))
j = 0
for x in range(len(data)):
    for j in range(len(individualMatchInfo)):
        print(individualMatchInfo[x]["participantIdentities"]
              [j]["player"]["summonerName"])

from flask import Flask, render_template, session
import random
import sys
import json
import requests
import sys
import string

app = Flask(__name__)

app.secret_key = '5791628bb0b13ce0c676dfde280ba245'


apiKey = "RGAPI-3393379a-cb60-48f6-bca4-cf994e7878cd"


def rewrittenRegion(region):
    if region == "TR1":
        return "Turkey"
    elif region == "KR":
        return "Korea"
    elif region == "JP1":
        return "Japan"
    elif region == "BR1":
        return "Brazil"
    elif region == "EUW1":
        return "Europe West"
    elif region == "EUNE":
        return "Europe Nordic & East"
    elif region == "OC1":
        return "Oceania"
    elif region == "LA2":
        return "Las"
    elif region == "LA1":
        return "Lan"
    elif region == "RU":
        return "Russia"
    else:
        return "North America"


def rewrittenQueueTypes(title):
    if title == "RANKED_SOLO_5x5":
        return "Ranked Solo 5x5"

    elif title == "RANKED_TFT":
        return "Ranked Solo TFT"

    elif title == "RANKED_FLEX_SR":
        return "Ranked Flex 5X5"
    else:
        return "Ranked Flex TFT"


def printCurrentRankings(region, APIKey, queueType, tier, division):
    url = "https://" + region + ".api.riotgames.com/lol/league-exp/v4/entries/" + \
        queueType + "/" + tier + "/" + division + "?page=1&api_key=" + apiKey
    response = requests.get(url)
    response.status_code
    return json.loads(response.content)


def getSummonerInfo(region, APIKey, name):
    url = "https://" + region + \
        '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=' + apiKey
    response = requests.get(url)
    response.status_code
    return json.loads(response.content)


def getRankData(region, APIKey, summonerID):
    url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + \
        summonerID + "?page=1&api_key=" + apiKey
    response = requests.get(url)
    response.status_code
    return json.loads(response.content)


def getTop3Mastery(region, APIKey, summonerID):
    url = "https://" + region + \
        '.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + \
        summonerID + "?api_key=" + APIKey
    response = requests.get(url)
    response.status_code
    data = json.loads(response.content)
    i = 0
    for i in range(3):
        print("champion id =" + str(data[i]["championId"] +
                                    " and champion Mastery = " + str(data[i]["championPoints"])))


def getMatchHistory(region, accountId, apiKey, endIndex):
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


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def hello_world():
    return render_template('home.html')


@app.route('/<region>/ranking/ladder/<queueType>/<tier>')
def printCurrentRanking(region, queueType, tier):
    division = "I"
    data = printCurrentRankings(region, apiKey, queueType, tier, division)
    newQueueType = rewrittenQueueTypes(data[0]["queueType"])
    newRegion = rewrittenRegion(region)
    return render_template('ranking.html', len=len(data), data=data, newQueueType=newQueueType, newRegion=newRegion, region=region)


@app.route('/<region>/ranking/ladder')
def printChallenger(region):
    queueType = "RANKED_SOLO_5x5"
    tier = "CHALLENGER"
    division = "I"
    data = printCurrentRankings(region, apiKey, queueType, tier, division)
    newQueueType = rewrittenQueueTypes(data[0]["queueType"])
    newRegion = rewrittenRegion(region)
    return render_template('ranking.html', len=len(data), data=data, newQueueType=newQueueType, newRegion=newRegion, region=region)


@app.route('/<region>/summoner/<name>')
def summonerSearch(region, name):
    summonerInfo = getSummonerInfo(region, apiKey, name)
    rankData = getRankData(region, apiKey, summonerInfo["id"])
    accountId = summonerInfo["accountId"]
    matchHistoryList = getMatchHistory(region, accountId, apiKey, str(10))
    individualMatchInfo = []
    x = 0
    for x in range(len(matchHistoryList)):
        individualMatchInfo.append(getMatchInfo(
            region, matchHistoryList["matches"][x]["gameId"], apiKey))
    length = len(rankData)
    matchHistoryLength = len(matchHistoryList)
    TFT = 0
    sumRift = 1
    num = 2
    num2 = 6
    return render_template('summoner.html', name=name,
                           summonerInfo=summonerInfo, rankData=rankData,
                           sumRift=sumRift, TFT=TFT, length=length, num=num,
                           individualMatchInfo=individualMatchInfo, matchHistoryLength=matchHistoryLength, num2=num2)


@app.route('/champion/<name>')
def championSearch(name):
    return render_template('champion.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)

import requests
from bs4 import BeautifulSoup
import numpy as np

class Match:
    #team names are str, score is list like [homeScore, awayScore]
    def __init__(self, homeTeam, awayTeam, scoreList):
        self.home = homeTeam
        self.away = awayTeam
        self.score = scoreList

    #Returns true if the score was a draw
    def isDraw(self):
        if(self.score[0] == self.score[1]):
            return True
        return False

    #Returns name of winning team, assuming draw already checked
    def getWinner(self):
        if(self.score[0] > self.score[1]):
            return self.home
        return self.away

    def getHomeTeam(self):
        return self.home

    def getAwayTeam(self):
        return self.away

    def __str__(self):
        return(self.home + " " + str(self.score[0]) + " " + self.away + str(self.score[1]))

def updateElo(match, prevRatings):
    homeRating = float(prevRatings[match.getHomeTeam()])
    awayRating = float(prevRatings[match.getAwayTeam()])
    powerChange = np.power(10,((awayRating - homeRating)/400))
    eHome = float(1/(1 + (powerChange)))
    eAway = 1 - eHome

    if(match.isDraw()):
        homeRating += 16*(0.5 - eHome)
        awayRating += 16*(0.5 - eAway)
        prevRatings[match.getHomeTeam()] = round(homeRating)
        prevRatings[match.getAwayTeam()] = round(awayRating)
        return prevRatings

    winner = match.getWinner()
    if winner == match.getHomeTeam():
        homeRating += 16*(1 - eHome)
        awayRating += 16*(0 - eAway)
        prevRatings[match.getHomeTeam()] = round(homeRating)
        prevRatings[match.getAwayTeam()] = round(awayRating)
    else:
        homeRating += 16*(0 - eHome)
        awayRating += 16*(1 - eAway)
        prevRatings[match.getHomeTeam()] = round(homeRating)
        prevRatings[match.getAwayTeam()] = round(awayRating)
    return prevRatings



teamRatings = {}
f = open('/Users/eliturner/Documents/Python Projects/SoccerRatings/ratings.txt', 'r')
content = f.readlines()
f.close()
prevRound = int(content[0].split()[1])

url = 'https://www.scorespro.com/soccer/england/premier-league/results'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
currentRound = prevRound + 1
Rounds = soup.findAll(class_ = 'ncet')
resultDivs = soup.findAll(class_ = 'compgrp')
resultDiv = []
for i in range(len(Rounds)):
    if(int(Rounds[i].getText().split()[1]) == currentRound):
        resultDiv.append(resultDivs[i])

matchesRaw = []
for result in resultDiv:
    matchesRaw.append(result.select('table.blocks.gteam'))

matches = []
for groupOfMatches in matchesRaw:
    for match in groupOfMatches:
        homeTeam = match.select('td.home.uc')[0].getText().strip()
        awayTeam = match.select('td.away.uc')[0].getText().strip()
        score = []
        for rawScore in match.find('td', class_ = 'score'):
            if(rawScore.name == 'a'):
                scores = rawScore.getText().split()
                score.append(scores[0])
                score.append(scores[2])
                matches.append(Match(homeTeam, awayTeam, score))

teamRatings = {}
for line in content[1:]:
    team = line.split(',')
    teamRatings.update({team[0]:team[1]})

if(len(matches) == 10):
    for match in matches:
        updateElo(match, teamRatings)
    f = open('/Users/eliturner/Documents/Python Projects/SoccerRatings/ratings.txt', 'w+')
    f.write('Week ' + str(currentRound) + '\n')
    for team in teamRatings:
        f.write(team + ',' + str(teamRatings[team]) + '\n')
    f.close()

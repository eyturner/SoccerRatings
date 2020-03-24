import requests
from bs4 import BeautifulSoup
import numpy as np
from Match import Match

def getMatches(matches, prevRound, url):
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

def updateRatings(content, matches, currentRound):
    for line in content[1:]:
        team = line.split(',')
        teamRatings.update({team[0]:team[1]})

    if(len(matches) == 10):
        for match in matches:
            updateElo(match, teamRatings)
        f = open('SoccerRatings/ratings.txt', 'w+')
        f.write('Week ' + str(currentRound) + '\n')
        for team in teamRatings:
            f.write(team + ',' + str(teamRatings[team]) + '\n')
        f.close()

def main():
    teamRatings = {}
    matches = []
    f = open('SoccerRatings/ratings.txt', 'r')
    content = f.readlines()
    f.close()
    prevRound = int(content[0].split()[1])
    url = 'https://www.scorespro.com/soccer/england/premier-league/results'
    getMatches(matches, prevRound, url)
    updateRatings(content, matches, prevRound + 1)
    df = pd.read_csv('SoccerRatings/RatingsSheet.csv', index_col = 'Team')

if __name__ == '__main__':
    main()

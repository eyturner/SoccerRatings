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

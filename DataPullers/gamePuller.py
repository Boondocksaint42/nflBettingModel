import requests
from bs4 import BeautifulSoup, NavigableString

from DataPullers.teamPuller import getTeamName
from game import Game

url = "https://www.pro-football-reference.com/years/{}/games.htm"


def getDate(param):
    split = param.split(' ')
    month = split[0]
    day = split[1]
    day = day if int(day) > 9 else "0%s" % day
    switcher = {
        "January": "1",
        "February": "2",
        "March": "3",
        "April": "4",
        "May": "5",
        "June": "6",
        "July": "7",
        "August": "8",
        "September": "9",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    return switcher.get(month) + day


def pullGames(year, league):
    schedule = []
    response = requests.get(url.format(year))
    soup = BeautifulSoup(response.text, "html.parser")
    soup.prettify()
    game_table = soup.findAll('div', {"id": "div_games"})
    try:
        game_table = game_table[0].contents[1].contents[6]
    except IndexError:
        exit(-2)

    for game in game_table.contents:
        if not (isinstance(game, NavigableString)):
            if isinstance(game.contents[2], NavigableString) or game.contents[2].text.strip() == 'Playoffs':
                continue

            try:
                date = getDate(game.contents[2].text.strip())
                location = game.find('td', {'data-stat': 'game_location'}).text.strip()
                winner = findTeam(league, game.find('td', {'data-stat': 'loser'}).text.strip())
                loser = findTeam(league, game.find('td', {'data-stat': 'winner'}).text.strip())
                winner_points = int(game.find('td', {'data-stat': 'pts_win'}).text.strip())
                loser_points = int(game.find('td', {'data-stat': 'pts_lose'}).text.strip())
                if location == '':
                    schedule.append(Game(winner, loser, winner_points, loser_points, date))
                else:
                    schedule.append(Game(loser, winner, loser_points, winner_points, date))
            except:
                continue
    return schedule


def findTeam(league, team_name):
    for team in league:
        if team.name == getTeamName(team_name):
            return team

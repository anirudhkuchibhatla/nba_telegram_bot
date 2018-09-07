import nba_py
import numpy
from datetime import datetime

from telegram.ext import Updater

updater = Updater(token=bottoken)

dispatcher = updater.dispatcher

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



def scores(bot, update):
    date = datetime.today()
    scoreboard = nba_py.Scoreboard(month=date.month - 3, day=date.day, year=date.year)
    line_score = scoreboard.line_score()

    # Get games
    current_game_sequence = 0
    game_sequence_counter = 0

    games = []


    for team in line_score:
        if team["GAME_SEQUENCE"] != current_game_sequence:
            home = team["TEAM_ABBREVIATION"]
            record_home = "Record: " + team["TEAM_WINS_LOSSES"]

            if (team["PTS"]):
                points = str(team["PTS"]) + " - "

            current_game_sequence = team["GAME_SEQUENCE"]
            game_sequence_counter += 1

        elif game_sequence_counter == 1:
            away = team["TEAM_ABBREVIATION"]
            record_away = "Record: " + team["TEAM_WINS_LOSSES"]

            if (team["PTS"]):
                points += str(team["PTS"])
            else:
                points = "Game did not start yet!"


            current_game = home + " vs. " + away + "\n" + home + " " + record_home + "\n" + away + " " + record_away + "\n" + "Score: " + points

            games.append(current_game)

            # current_game = {}

            game_sequence_counter = 0

    final = ""

    for game in games:

        bot.send_message(chat_id=update.message.chat_id, text=game)



scores_handler = CommandHandler('scores', scores)
dispatcher.add_handler(scores_handler)


def yesterday(bot, update):
    date = datetime.today()
    scoreboard = nba_py.Scoreboard(month=date.month, day=date.day - 1, year=date.year)
    line_score = scoreboard.line_score()

    # Get games
    current_game_sequence = 0
    game_sequence_counter = 0

    games = []


    for team in line_score:
        if team["GAME_SEQUENCE"] != current_game_sequence:
            home = team["TEAM_ABBREVIATION"]
            record_home = "Record: " + team["TEAM_WINS_LOSSES"]

            if (team["PTS"]):
                points = str(team["PTS"]) + " - "


            current_game_sequence = team["GAME_SEQUENCE"]
            game_sequence_counter += 1

        elif game_sequence_counter == 1:
            away = team["TEAM_ABBREVIATION"]
            record_away = "Record: " + team["TEAM_WINS_LOSSES"]

            if (team["PTS"]):
                points += str(team["PTS"])
            else:
                points = "Game did not start yet!"



            current_game = home + " vs. " + away + "\n" + home + " " + record_home + "\n" + away + " " + record_away + "\n" + "Score: " + points

            games.append(current_game)

            game_sequence_counter = 0

    final = ""

    for game in games:

        bot.send_message(chat_id=update.message.chat_id, text=game)



yesterday_handler = CommandHandler('yesterday', yesterday)
dispatcher.add_handler(yesterday_handler)

updater.start_polling()


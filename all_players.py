import os.path
from player_names import get_all_players

all_players = []

if not os.path.isfile('./player_names.txt'):
    all_players = get_all_players(driver)
else:
    player_names_file = open("player_names.txt", "r")
    for line in player_names_file:
        attr = line.split('|')
        player = {
            'name': attr[0],
            'href': attr[1].replace('\n', '')
        }
        all_players.append(player)

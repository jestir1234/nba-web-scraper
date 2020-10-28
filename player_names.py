from constants import ALL_PLAYERS_URL
from bs4 import BeautifulSoup
import string


def get_all_players(driver):
    alphabet = list(string.ascii_lowercase)
    all_players = []
    for letter in alphabet:
        url = '{0}/{1}'.format(ALL_PLAYERS_URL, letter)
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content)
        for th in soup.findAll('th', attrs={'data-stat': 'player'}):
            name = th.find('a')

            if name:
                player = {
                    'name': name.text,
                    'href': name.get('href')
                }
                all_players.append(player)

    outF = open("player_names.txt", "w")
    for player in all_players:
        # write line to output file
        outF.write(player['name'])
        outF.write('|')
        outF.write(player['href'])
        outF.write("\n")
    outF.close()

    return all_players

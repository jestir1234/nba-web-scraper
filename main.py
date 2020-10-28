from selenium import webdriver
import os.path
from bs4 import BeautifulSoup
import csv
import sys
import pandas as pd
from page_parser import PageParser
from constants import BASE_SCRAPE_URL
from all_players import all_players

driver = webdriver.Chrome("/Users/matthewnguyen/Documents/chromedriver")
PER_GAME = 'per_game'
ADVANCED = 'advanced'
PER_GAME_DIV_ID = 'all_per_game'
ADVANCED_DIV_ID = 'div_advanced'
PER_GAME_FILE = './per_game_stats.csv'
ADVANCED_FILE = './advanced_stats.csv'

def export_scraped_stats(content_id, filename):
    existing_player_rows = set([])
    driver.get('{0}{1}'.format(BASE_SCRAPE_URL, '/players/a/abdelal01.html'))
    content = driver.page_source
    soup = BeautifulSoup(content)
    headers_data = ['Name']
    headers = soup.find('div', attrs={'id': content_id}).find(
        'thead').find('tr').findAll('th')
    print('searching headers...')
    for header in headers:
        headers_data.append(header.text)
    
    # Open csv file if it exists otherwise create one and fill in the column headers
    if not os.path.isfile(filename):
        with open(filename, 'w') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(headers_data)
            headers_data.pop(0) # remove name from headers_data
    
    # Open stats csv 
    with open(filename, 'r+') as myfile:
        reader = csv.reader(myfile, delimiter=',')
        
        # Read player name column from all lines and store names in Set for quick read access
        for line in reader:
            existing_player_rows.add(line[0])
        print('existing_player_rows', existing_player_rows)


        # Loop through all players, skipping names already captured in existing_player_row set
        # Scrape data on player and append stats to csv file
        for player in all_players:
            if player['name'] in existing_player_rows:
                print('{0} already saved in csv file! Skipping!'.format(player['name']))
                continue

            print('Scraping stats for {0}'.format(player['name']))
            page_parser = PageParser(player, driver, content_id, headers_data)
            page_parser.scrape_stats()
            for row in page_parser.stats:
                wr = csv.writer(myfile)
                wr.writerow(row)
    

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

def run():
    for arg in sys.argv:
        if arg == PER_GAME:
            export_scraped_stats(PER_GAME_DIV_ID, PER_GAME_FILE)

        if arg == ADVANCED:
            export_scraped_stats(ADVANCED_DIV_ID, ADVANCED_FILE)

run()

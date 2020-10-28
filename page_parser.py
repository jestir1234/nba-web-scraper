from constants import BASE_SCRAPE_URL
from bs4 import BeautifulSoup
import time
import pandas as pd

class PageParser:

    def __init__(self, player, driver, content_id, headers_data):
        self.player = player
        self.driver = driver
        self.stats = []
        self.content_id = content_id
        self.headers_data = headers_data
    
    def scrape_stats(self):
        print(self.player)
        self.driver.get('{0}{1}'.format(BASE_SCRAPE_URL, self.player['href']))
        content = self.driver.page_source
        soup = BeautifulSoup(content)
        rows_data = []
        content_body = soup.find('div', attrs={'id': self.content_id})
        current_header_texts = []
        if content_body:
            current_headers = content_body.find(
                'thead').find('tr').findAll('th')
        else:
            return None




        for header in current_headers:
            current_header_texts.append(header.text)
        print('self.headers_data...', self.headers_data)
        print('current headers text...', current_header_texts)
        div = soup.find('div', attrs={'id': self.content_id})
        if div:
            rows = div.find('tbody').findAll('tr')
            for row in rows:
                row_data = [''] * len(self.headers_data)
                # row_data[0] = self.player['name']
                columns = row.findAll(['td', 'th'])

                for idx, col in enumerate(columns):
                    true_col_idx = self.headers_data.index(current_header_texts[idx])
                    a = col.find('a')
                    if a:
                        row_data[true_col_idx] = a.text
                    else:
                        row_data[true_col_idx] = col.text
                
                row_data.insert(0, self.player['name'])
                rows_data.append(row_data)
                print('row_data', row_data)
                    
            self.stats = rows_data

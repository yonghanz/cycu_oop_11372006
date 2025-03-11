import requests
from bs4 import BeautifulSoup
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_tvbs_news():
    url = 'https://news.tvbs.com.tw/'
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.find_all('div', class_='news_list')
            
            for item in news_items:
                title = item.find('h2').text.strip()
                link = item.find('a')['href']
                print(f'Title: {title}')
                print(f'Link: {link}')
                print('---')
        else:
            logging.error(f'Failed to retrieve the news, status code: {response.status_code}')
    except requests.RequestException as e:
        logging.error(f'An error occurred: {e}')

if __name__ == '__main__':
    fetch_tvbs_news()
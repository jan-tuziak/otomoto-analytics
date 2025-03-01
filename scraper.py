import requests
from bs4 import BeautifulSoup
import json

def scrape(url) -> BeautifulSoup:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.text, "html.parser")

def scrape_offer_urls(page_num: int) -> dict:
    URL = 'https://www.otomoto.pl/osobowe?page=' + str(page_num)
    soup = scrape(URL)
    articles = soup.find('div', {"data-testid": "search-results"})
    if articles is None:
        print('something went wrong. 14357.')
        return []
    
    articles = articles.find_all('article', {'data-id': True})
    if len(articles) == 0:
        print('something went wrong. 716555.')
        return []
    
    articles = [article for article in articles if not article.find(attrs={'data-testid': 'featured-dealer'})]
    if len(articles) == 0:
        print('something went wrong. 1235784.')
        return []
    
    data = {}
    for article in articles:
        data_id = article.get('data-id')
        id = data_id if data_id else None

        link = article.find('a', href=lambda href: href and "osobowe/oferta" in href)
        url = link['href'] if link else None
        
        if id is None or url is None:
            continue
        
        data[id] = url
    return data

if __name__ == '__main__':
    data = scrape_offer_urls(1)
    import json
    print(json.dumps(data, indent=4))
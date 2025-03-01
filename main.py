import scraper
import json
import sys
from bs4 import BeautifulSoup

def get_number_of_pages(url) -> int:
    first_page = scraper.scrape(url)
    next_page_element = first_page.find('li', {'aria-label': 'Go to next Page'})

    if next_page_element:
        # Znajdź poprzedni element (zawierający numer strony)
        previous_sibling = next_page_element.find_previous_sibling('li')
        if previous_sibling and previous_sibling.text.isdigit():
            return int(previous_sibling.text)
        else:
            return None
    else:
        return None

if __name__== '__main__':
    URL = 'https://www.otomoto.pl/osobowe/'
    num_of_pages = get_number_of_pages(URL)
    if num_of_pages == 0:
        print('num of pages not found')
        sys.exit()

    # Loop over the pages and get URL offers
    urls = {}
    for i in range(1, num_of_pages+1):
        print(f'Scraping page {i} out of {num_of_pages}')
        urls.update(scraper.scrape_offer_urls(i))
        
        if len(urls) > 1000:
            print('saving urls to file')
            with open(f'urls/{i}.json', 'a') as fp:
                json.dump(urls, fp, indent=4)
            urls = {}
    
    print('Done')
    #TODO: investigate the "something went wrong. 14357." error
    


# import requests
import json
# from bs4 import BeautifulSoup
from google.cloud import bigquery
import scraper

def _get_data_from_specification_table(soup, parameter):
    div_element = soup.find('div', attrs={'data-testid': parameter})
    if div_element:
        paragraphs = div_element.find_all("p")
        if len(paragraphs) > 1:
            return paragraphs[1].text.strip()
    
    return None

def _is_professional_seller(soup):
    """ Zwraca True, gdy sprzedający jest profesjonalistą (firma).
    Jeżeli sprzedający jest osobą prywatną zwraca False."""
    div_element = soup.find("div", {"data-testid": "content-seller-area-section"})
    if div_element:
        paragraphs = div_element.find_all("p")
        for p in paragraphs:
            if "profesjonal" in p.text.strip().lower():
                return True
    return False

def _get_location(soup):
    div_element = soup.find("div", {"data-testid": "content-seller-area-section"})
    if div_element:
        anchors = div_element.find_all('a')
        for a in anchors:
            if "google.com/maps" in a['href']:
                return a['href']
    return None

def scrape(url):
    """ Pobiera dane z oferty Otomoto """
    
    # Nagłówki, aby uniknąć blokady scrapowania
    # HEADERS = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    # }
    # response = requests.get(url, headers=HEADERS)
    # soup = BeautifulSoup(response.text, "html.parser")

    soup = scraper.scrape(url)

    data = {}
    data["url"] = url
    data["title"] = soup.find("h1", class_='offer-title').text.strip() if soup.find("h1", class_='offer-title') else None
    data["price"] = soup.find("h3", class_="offer-price__number").text.strip() if soup.find("h3", class_="offer-price__number") else None
    data["currency"] = soup.find("p", class_="offer-price__currency").text.strip() if soup.find("p", class_="offer-price__currency") else None
    
    data["make"] = _get_data_from_specification_table(soup, 'make')
    data["model"] = _get_data_from_specification_table(soup, 'model')
    data["version"] = _get_data_from_specification_table(soup, 'version')
    data["color"] = _get_data_from_specification_table(soup, 'color')
    data["door_count"] = _get_data_from_specification_table(soup, 'door_count')
    data["nr_seats"] = _get_data_from_specification_table(soup, 'nr_seats')
    data["year"] = _get_data_from_specification_table(soup, 'year')
    data["generation"] = _get_data_from_specification_table(soup, 'generation')
    data["fuel_type"] = _get_data_from_specification_table(soup, 'fuel_type')
    data["engine_capacity"] = _get_data_from_specification_table(soup, 'engine_capacity')
    data["engine_power"] = _get_data_from_specification_table(soup, 'engine_power')
    data["body_type"] = _get_data_from_specification_table(soup, 'body_type')
    data["gearbox"] = _get_data_from_specification_table(soup, 'gearbox')
    data["wheel_drive"] = _get_data_from_specification_table(soup, 'transmission')
    data["country_origin"] = _get_data_from_specification_table(soup, 'country_origin')
    data["mileage"] = _get_data_from_specification_table(soup, 'mileage')
    data["new_used"] = _get_data_from_specification_table(soup, 'new_used')
    data["registered_in_poland"] = _get_data_from_specification_table(soup, 'registered')
    data["original_owner"] = _get_data_from_specification_table(soup, 'original_owner')
    data["no_accident"] = _get_data_from_specification_table(soup, 'no_accident')
    data["has_registration"] = _get_data_from_specification_table(soup, 'has_registration')
    data["service_record"] = _get_data_from_specification_table(soup, 'service_record')
    data["is_proffesional_seller"] = _is_professional_seller(soup)

    data["location"] = _get_location(soup)

    return data

if __name__ == '__main__':
    URL = "https://www.otomoto.pl/osobowe/oferta/citroen-c4-citroen-c4-1-2-puretech-max-s-s-eat8-ID6GSrGH.html"
    data = scrape(URL)
    print(json.dumps(data, indent=4))
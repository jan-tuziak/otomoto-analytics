import requests
import json
from bs4 import BeautifulSoup
from google.cloud import bigquery

# URL przykładowej oferty
URL = "https://www.otomoto.pl/osobowe/oferta/citroen-c4-citroen-c4-1-2-puretech-max-s-s-eat8-ID6GSrGH.html"

# Nagłówki, aby uniknąć blokady scrapowania
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_data_from_specification_table(soup, parameter):
    div_element = soup.find('div', attrs={'data-testid': parameter})
    if div_element:
        paragraphs = div_element.find_all("p")
        if len(paragraphs) > 1:
            return paragraphs[1].text.strip()
    
    return None

def is_professional_seller(soup):
    """ Zwraca True, gdy sprzedający jest profesjonalistą (firma).
    Jeżeli sprzedający jest osobą prywatną zwraca False."""
    div_element = soup.find("div", {"data-testid": "content-seller-area-section"})
    if div_element:
        paragraphs = div_element.find_all("p")
        for p in paragraphs:
            if "profesjonal" in p.text.strip().lower():
                return True
    return False

def get_location(soup):
    div_element = soup.find("div", {"data-testid": "content-seller-area-section"})
    if div_element:
        anchors = div_element.find_all('a')
        for a in anchors:
            if "google.com/maps" in a['href']:
                return a['href']
    return None


def scrape_single_otomoto_offer(url):
    """ Pobiera dane z oferty Otomoto """
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    data = {}
    data["title"] = soup.find("h1", class_='offer-title').text.strip() if soup.find("h1", class_='offer-title') else None
    data["price"] = soup.find("h3", class_="offer-price__number").text.strip() if soup.find("h3", class_="offer-price__number") else None
    data["currency"] = soup.find("p", class_="offer-price__currency").text.strip() if soup.find("p", class_="offer-price__currency") else None
    
    data["make"] = get_data_from_specification_table(soup, 'make')
    data["model"] = get_data_from_specification_table(soup, 'model')
    data["version"] = get_data_from_specification_table(soup, 'version')
    data["color"] = get_data_from_specification_table(soup, 'color')
    data["door_count"] = get_data_from_specification_table(soup, 'door_count')
    data["nr_seats"] = get_data_from_specification_table(soup, 'nr_seats')
    data["year"] = get_data_from_specification_table(soup, 'year')
    data["generation"] = get_data_from_specification_table(soup, 'generation')
    data["fuel_type"] = get_data_from_specification_table(soup, 'fuel_type')
    data["engine_capacity"] = get_data_from_specification_table(soup, 'engine_capacity')
    data["engine_power"] = get_data_from_specification_table(soup, 'engine_power')
    data["body_type"] = get_data_from_specification_table(soup, 'body_type')
    data["gearbox"] = get_data_from_specification_table(soup, 'gearbox')
    data["wheel_drive"] = get_data_from_specification_table(soup, 'transmission')
    data["country_origin"] = get_data_from_specification_table(soup, 'country_origin')
    data["mileage"] = get_data_from_specification_table(soup, 'mileage')
    data["new_used"] = get_data_from_specification_table(soup, 'new_used')
    data["registered_in_poland"] = get_data_from_specification_table(soup, 'registered')
    data["original_owner"] = get_data_from_specification_table(soup, 'original_owner')
    data["no_accident"] = get_data_from_specification_table(soup, 'no_accident')
    data["has_registration"] = get_data_from_specification_table(soup, 'has_registration')
    data["service_record"] = get_data_from_specification_table(soup, 'service_record')
    data["is_proffesional_seller"] = is_professional_seller(soup)

    
    data["location"] = get_location(soup)
    data["url"] = url

    return data

# Testujemy scrapera
data = scrape_single_otomoto_offer(URL)
print(json.dumps(data, indent=4))
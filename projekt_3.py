"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Maxim Dotsenko 
email: maximdocenko95@gmail.com
discord: maximrtop
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def get_region_data(region_url):
    """
    Načte stránku územního celku a získá seznam obcí.
    Z tabulky se extrahují základní údaje:
      - kód obce (z prvního sloupce, kde je odkaz)
      - název obce
      - počet voličů v seznamu, vydané obálky, platné hlasy
      - odkaz na detailní výsledky hlasování pro obec
    Vrací seznam slovníků, kdy každý slovník reprezentuje jednu obec.
    """
    response = requests.get(region_url)
    if response.status_code != 200:
        print("Chyba při načítání stránky územního celku.")
        sys.exit(1)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    if not table:
        print("Na stránce nebyla nalezena tabulka s výsledky.")
        sys.exit(1)

    municipalities = []
    rows = table.find_all('tr')
    # První řádek obvykle obsahuje hlavičku, proto začínáme od indexu 1
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue  # přeskočíme řádky bez všech potřebných sloupců

        code_link = cols[0].find('a')
        if code_link:
            municipality_code = code_link.text.strip()
            detail_href = code_link.get('href')
        else:
            municipality_code = cols[0].text.strip()
            detail_href = None

        municipality_name = cols[1].text.strip()
        volici = cols[2].text.strip().replace('\xa0', '').replace(' ', '')
        obalky = cols[3].text.strip().replace('\xa0', '').replace(' ', '')
        platne = cols[4].text.strip().replace('\xa0', '').replace(' ', '')

        # Upravíme odkaz na detail, pokud je relativní
        if detail_href and detail_href.startswith('?'):
            detail_url = "https://www.volby.cz/pls/ps2017nss/" + detail_href
        else:
            detail_url = detail_href

        municipality = {
            'code': municipality_code,
            'name': municipality_name,
            'volici': volici,
            'obalky': obalky,
            'platne': platne,
            'detail_url': detail_url
        }
        municipalities.append(municipality)
    return municipalities

def get_municipality_results(detail_url):
    """
    Načte detailní stránku obce a získá výsledky hlasování pro kandidující strany.
    Předpokládá se, že stránka obsahuje tabulku, kde každý řádek má:
      - název strany
      - počet hlasů
    Vrací slovník, kde klíče jsou názvy stran a hodnoty počet hlasů (jako řetězce).
    """
    response = requests.get(detail_url)
    if response.status_code != 200:
        print("Chyba při načítání detailu obce:", detail_url)
        return {}
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    if not table:
        print("Nebyla nalezena tabulka s výsledky pro obec:", detail_url)
        return {}

    party_results = {}
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 2:
            continue
        party_name = cols[0].text.strip()
        votes = cols[1].text.strip().replace('\xa0', '').replace(' ', '')
        if votes.isdigit():
            party_results[party_name] = votes
    return party_results

def write_csv(municipalities, filename, all_parties):
    """
    Zapíše výsledky do CSV souboru.
    Každý řádek obsahuje:
      - kód obce, název obce, voliče v seznamu, vydané obálky, platné hlasy,
      - následně sloupce s hlasováním pro každou kandidující stranu (seřazené abecedně).
    """
    fieldnames = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy'] + sorted(all_parties)
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for mun in municipalities:
            row = {
                'Kód obce': mun['code'],
                'Název obce': mun['name'],
                'Voliči v seznamu': mun['volici'],
                'Vydané obálky': mun['obalky'],
                'Platné hlasy': mun['platne']
            }
            for party in all_parties:
                row[party] = mun.get('parties', {}).get(party, '')
            writer.writerow(row)

def main():
    # Ověření, zda byly zadány správné argumenty: URL a název CSV souboru
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <URL_územního_celeku> <výstupní_csv>")
        sys.exit(1)

    region_url = sys.argv[1]
    output_csv = sys.argv[2]

    # Získáme seznam obcí z daného územního celku
    municipalities = get_region_data(region_url)
    if not municipalities:
        print("Nebyla nalezena žádná data o obcích.")
        sys.exit(1)

    all_parties = set()
    # Pro každou obec stáhneme detailní výsledky hlasování
    for mun in municipalities:
        detail_url = mun.get('detail_url')
        if detail_url:
            parties = get_municipality_results(detail_url)
            mun['parties'] = parties
            all_parties.update(parties.keys())
        else:
            mun['parties'] = {}

    # Uložíme získaná data do CSV souboru
    write_csv(municipalities, output_csv, all_parties)
    print("Data byla úspěšně uložena do souboru", output_csv)

if __name__ == "__main__":
    main()

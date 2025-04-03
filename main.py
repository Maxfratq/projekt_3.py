"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Maxim Dotsenko 
email: maximdocenko95@gmail.com
discord: maximrtop
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup

# Globální seznamy pro uchování dat
volici = []
obalky = []
platne_hlasy = []

def nacti_stranku(url):
    """Stáhne HTML z dané URL a vrátí objekt BeautifulSoup."""
    odpoved = requests.get(url)
    stranka = BeautifulSoup(odpoved.text, "html.parser")
    print("STAHUJI DATA Z URL:", url)
    return stranka

# Skript očekává přesně 2 argumenty: URL a název výstupního CSV souboru.
if len(sys.argv) == 3:
    region_url = sys.argv[1]
    vystupni_soubor = sys.argv[2]
    region_stranka = nacti_stranku(region_url)
else:
    print('Chyba: Zadejte přesně dva argumenty: URL adresu a název výstupního CSV souboru.')
    sys.exit(1)

def ziskej_nazvy_obci():
    """Vrací seznam názvů obcí z regionové stránky."""
    nazvy = []
    bunky = region_stranka.find_all("td", class_="overflow_name")
    for bunka in bunky:
        nazvy.append(bunka.text)
    return nazvy

def ziskej_detailni_url():
    """Vrací seznam URL adres detailních stránek pro jednotlivé obce."""
    url_list = []
    bunky = region_stranka.find_all("td", class_="cislo", href=True)
    for bunka in bunky:
        relativni_odkaz = bunka.a["href"]
        cela_url = "https://volby.cz/pls/ps2017nss/" + relativni_odkaz
        url_list.append(cela_url)
    return url_list

def ziskej_id_obci():
    """Vrací seznam identifikačních čísel obcí."""
    id_list = []
    bunky = region_stranka.find_all("td", class_="cislo")
    for bunka in bunky:
        id_list.append(bunka.text)
    return id_list

def ziskej_nazvy_stran():
    """Z první detailní stránky obce získá seznam kandidujících stran."""
    detailni_url = ziskej_detailni_url()
    if not detailni_url:
        return []
    odpoved = requests.get(detailni_url[0])
    detail_stranka = BeautifulSoup(odpoved.text, "html.parser")
    strany = []
    bunky = detail_stranka.find_all("td", class_="overflow_name")
    for bunka in bunky:
        strany.append(bunka.text)
    return strany

def sesbir_data_volicu():
    """
    Pro každou detailní stránku obce získá údaje:
      - registrovaní voliči (headers="sa2"),
      - vydané obálky (headers="sa3"),
      - platné hlasy (headers="sa6")
    a uloží je do globálních seznamů.
    """
    for url in ziskej_detailni_url():
        odpoved = requests.get(url)
        detail_stranka = BeautifulSoup(odpoved.text, "html.parser")
        bunky = detail_stranka.find_all("td", headers="sa2")
        for bunka in bunky:
            volici.append(bunka.text.replace('\xa0', ' '))
        bunky = detail_stranka.find_all("td", headers="sa3")
        for bunka in bunky:
            obalky.append(bunka.text.replace('\xa0', ' '))
        bunky = detail_stranka.find_all("td", headers="sa6")
        for bunka in bunky:
            platne_hlasy.append(bunka.text.replace('\xa0', ' '))

def ziskej_procenta_hlasu():
    """
    Pro každou obec získá procentuální výsledky hlasů pro jednotlivé strany.
    Vrací seznam, kde každý prvek je seznam procent pro jednu obec.
    """
    vsechna_procenta = []
    for url in ziskej_detailni_url():
        stranka = nacti_stranku(url)
        procenta = []
        bunky = stranka.find_all("td", class_="cislo", headers=["t1sb4", "t2sb4"])
        for bunka in bunky:
            procenta.append(bunka.text + " %")
        vsechna_procenta.append(procenta)
    return vsechna_procenta

def vytvor_radky_csv():
    """
    Sestaví řádky pro CSV soubor: ID obce, název, registrovaní voliči,
    vydané obálky, platné hlasy a procenta hlasů kandidujících stran.
    """
    radky = []
    sesbir_data_volicu()
    nazvy_obci = ziskej_nazvy_obci()
    id_obci = ziskej_id_obci()
    hlasovani = ziskej_procenta_hlasu()
    zakladni_udaje = list(zip(id_obci, nazvy_obci, volici, obalky, platne_hlasy))
    for udaje, procenta in zip(zakladni_udaje, hlasovani):
        radek = list(udaje) + procenta
        radky.append(radek)
    return radky

def main():
    hlavicka = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
    radky_csv = vytvor_radky_csv()
    strany = ziskej_nazvy_stran()
    for strana in strany:
        hlavicka.append(strana)
    print("UKLÁDÁM DATA DO SOUBORU:", vystupni_soubor)
    with open(vystupni_soubor, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(hlavicka)
        writer.writerows(radky_csv)
    print("UKONČUJI:", sys.argv[0])

if __name__ == '__main__':
    main()

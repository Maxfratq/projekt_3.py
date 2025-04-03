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

volici = []
obalky = []
platne_hlasy = []

def nacti_stranku(url):
    try:
        odpoved = requests.get(url)
    except Exception as e:
        print(f"Chyba při načítání URL: {url}\n{e}")
        sys.exit(1)
    stranka = BeautifulSoup(odpoved.text, "html.parser")
    print("DEBUG: STAHUJI DATA Z URL:", url)
    return stranka

if len(sys.argv) == 3:
    region_url = sys.argv[1]
    vystupni_soubor = sys.argv[2]
    region_stranka = nacti_stranku(region_url)
    print("DEBUG: Regionová stránka načtena.")
else:
    print('Chyba: Zadejte přesně dva argumenty: URL adresu a název výstupního CSV souboru.')
    sys.exit(1)

def ziskej_nazvy_obci():
    nazvy = [bunka.text for bunka in region_stranka.find_all("td", class_="overflow_name")]
    print(f"DEBUG: Nalezeno {len(nazvy)} názvů obcí.")
    return nazvy

def ziskej_detailni_url():
    url_list = []
    bunky = region_stranka.find_all("td", class_="cislo")
    for bunka in bunky:
        a_tag = bunka.find("a")
        if a_tag and a_tag.has_attr("href"):
            relativni_odkaz = a_tag["href"]
            cela_url = "https://volby.cz/pls/ps2017nss/" + relativni_odkaz
            url_list.append(cela_url)
    print(f"DEBUG: Nalezeno {len(url_list)} detailních URL.")
    return url_list

def ziskej_id_obci():
    id_list = [bunka.text for bunka in region_stranka.find_all("td", class_="cislo")]
    print(f"DEBUG: Nalezeno {len(id_list)} ID obcí.")
    return id_list

def ziskej_nazvy_stran():
    detailni_url = ziskej_detailni_url()
    if not detailni_url:
        print("DEBUG: Žádné detailní URL nenalezeny.")
        return []
    odpoved = requests.get(detailni_url[0])
    detail_stranka = BeautifulSoup(odpoved.text, "html.parser")
    strany = [bunka.text for bunka in detail_stranka.find_all("td", class_="overflow_name")]
    print(f"DEBUG: Nalezeno {len(strany)} názvů stran.")
    return strany

def sesbir_data_volicu():
    url_list = ziskej_detailni_url()
    for index, url in enumerate(url_list):
        odpoved = requests.get(url)
        detail_stranka = BeautifulSoup(odpoved.text, "html.parser")
        bunky_volici = detail_stranka.find_all("td", headers="sa2")
        pocet_volici = 0
        for bunka in bunky_volici:
            volici.append(bunka.text.replace('\xa0', ' '))
            pocet_volici += 1
        bunky_obalky = detail_stranka.find_all("td", headers="sa3")
        pocet_obalky = 0
        for bunka in bunky_obalky:
            obalky.append(bunka.text.replace('\xa0', ' '))
            pocet_obalky += 
        bunky_platne = detail_stranka.find_all("td", headers="sa6")
        pocet_platnych = 0
        for bunka in bunky_platne:
            platne_hlasy.append(bunka.text.replace('\xa0', ' '))
            pocet_platnych += 1
        print(f"DEBUG: Obec {index+1}/{len(url_list)}: volici={pocet_volici}, obálky={pocet_obalky}, platné hlasy={pocet_platnych}")

def ziskej_procenta_hlasu():
    vsechna_procenta = []
    url_list = ziskej_detailni_url()
    for index, url in enumerate(url_list):
        stranka = nacti_stranku(url)
        procenta = []
        bunky = stranka.find_all("td", class_="cislo", headers=["t1sb4", "t2sb4"])
        for bunka in bunky:
            procenta.append(bunka.text + " %")
        vsechna_procenta.append(procenta)
        print(f"DEBUG: Obec {index+1}/{len(url_list)}: nalezeno {len(procenta)} procentních hodnot")
    return vsechna_procenta

def vytvor_radky_csv():
    radky = []
    sesbir_data_volicu()
    nazvy_obci = ziskej_nazvy_obci()
    id_obci = ziskej_id_obci()
    hlasovani = ziskej_procenta_hlasu()
    zakladni_udaje = list(zip(id_obci, nazvy_obci, volici, obalky, platne_hlasy))
    print(f"DEBUG: Zakládních údajů nalezeno: {len(zakladni_udaje)}")
    for index, (udaje, procenta) in enumerate(zip(zakladni_udaje, hlasovani)):
        radek = list(udaje) + procenta
        radky.append(radek)
        print(f"DEBUG: Řádek {index+1} vytvořen, délka: {len(radek)} položek")
    print(f"DEBUG: Celkový počet řádků CSV: {len(radky)}")
    return radky

def main():
    hlavicka = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
    radky_csv = vytvor_radky_csv()
    strany = ziskej_nazvy_stran()
    for strana in strany:
        hlavicka.append(strana)
    print("DEBUG: Hlavicka CSV:", hlavicka)
    print("DEBUG: Ukládám data do souboru:", vystupni_soubor)
    with open(vystupni_soubor, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(hlavicka)
        writer.writerows(radky_csv)
    print("DEBUG: Skript ukončen:", sys.argv[0])

if __name__ == '__main__':
    main()

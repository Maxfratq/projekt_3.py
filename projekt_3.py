"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Maxim Dotsenko 
email: maximdocenko95@gmail.com
discord: maximrtop

Argumenty:
  První argument: URL cílového regionu, například:
    https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
  Druhý argument: název výstupního CSV souboru, například:
    vysledky_benesov.csv
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

# Dummy funkce a třída pro testovací režim, pokud není připojení k internetu.
# Za účelem testování bez internetu můžeme nahradit requests.get funkcí dummy_get.
class DummyResponse:
    def __init__(self, content, status_code=200):
        self.content = content.encode("utf-8")
        self.status_code = status_code

def dummy_get(url, *args, **kwargs):
    # Pokud URL obsahuje region, vracíme jednoduchou HTML stránku s tabulkou obcí
    if "ps32?xjazyk=CZ" in url:
        content = """
        <html>
          <body>
            <table>
              <tr>
                <th>Kód</th><th>Název</th><th>Voliči</th><th>Obálky</th><th>Platné</th>
              </tr>
              <tr>
                <td><a href="?xid=1">12345</a></td>
                <td>Testovací obec</td>
                <td>1000</td>
                <td>900</td>
                <td>850</td>
              </tr>
            </table>
          </body>
        </html>
        """
    # Если URL содержит id obce, vracíme jednoduchou HTML stránku s tabulkou výsledků pro strany
    elif "xid=1" in url or "?xid=1" in url:
        content = """
        <html>
          <body>
            <table>
              <tr>
                <th>Strana</th><th>Hlasů</th>
              </tr>
              <tr>
                <td>TestStrana</td>
                <td>100</td>
              </tr>
            </table>
          </body>
        </html>
        """
    else:
        content = ""
    return DummyResponse(content, 200)

# Hlavní program
def main():
    # Kontrola, zda jsou zadány přesně dva argumenty (mimo název skriptu)
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <URL_cílového_regionu> <název_csv_souboru>")
        sys.exit(1)
    
    url_region = sys.argv[1]
    csv_filename = sys.argv[2]
    
    # Stáhneme stránku regionu
    response = requests.get(url_region)
    if response.status_code != 200:
        print("Chyba při načítání stránky:", url_region)
        sys.exit(1)
    html_region = response.content
    soup = BeautifulSoup(html_region, "html.parser")
    
    # Najdeme tabulku s obcemi
    table = soup.find("table")
    if table is None:
        print("Nebyla nalezena tabulka s výsledky.")
        sys.exit(1)
    
    # Vytvoříme prázdný seznam pro uložení dat o obcích
    obce = []
    rows = table.find_all("tr")
    # Přeskočíme první řádek s hlavičkou
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue
        # Získáme kód obce a odkaz z prvního sloupce
        a_tag = cols[0].find("a")
        if a_tag:
            kod = a_tag.text.strip()
            href = a_tag.get("href")
        else:
            kod = cols[0].text.strip()
            href = ""
        nazev = cols[1].text.strip()
        volici = cols[2].text.strip().replace("\xa0", "").replace(" ", "")
        obalky = cols[3].text.strip().replace("\xa0", "").replace(" ", "")
        platne = cols[4].text.strip().replace("\xa0", "").replace(" ", "")
        # Pokud je odkaz relativní, přidáme základní URL
        if href.startswith("?"):
            detail_url = "https://www.volby.cz/pls/ps2017nss/" + href
        else:
            detail_url = href
        # Uložíme data o obci do slovníku
        obec = {"kod": kod, "nazev": nazev, "volici": volici, "obalky": obalky, "platne": platne, "detail_url": detail_url}
        obce.append(obec)
    
    # Pro každou obec získáme výsledky hlasování pro strany
    vsechny_strany = set()  # budeme si pamatovat všechny strany
    for obec in obce:
        detail_url = obec["detail_url"]
        if detail_url == "" or detail_url is None:
            obec["strany"] = {}
            continue
        # Stáhneme detailní stránku obce
        response_detail = requests.get(detail_url)
        if response_detail.status_code != 200:
            obec["strany"] = {}
            continue
        soup_detail = BeautifulSoup(response_detail.content, "html.parser")
        # Najdeme tabulku s výsledky hlasování pro strany
        tables = soup_detail.find_all("table")
        party_table = None
        for t in tables:
            ths = t.find_all("th")
            if len(ths) >= 2:
                party_table = t
                break
        # Pokud tabulka byla nalezena, načteme výsledky
        vysledky = {}
        if party_table is not None:
            rows_detail = party_table.find_all("tr")
            # Přeskočíme hlavičku (první řádek)
            for row_detail in rows_detail[1:]:
                cols_detail = row_detail.find_all("td")
                if len(cols_detail) < 2:
                    continue
                strana = cols_detail[0].text.strip()
                hlasy = cols_detail[1].text.strip().replace("\xa0", "").replace(" ", "")
                if hlasy.isdigit():
                    vysledky[strana] = hlasy
                    vsechny_strany.add(strana)
        else:
            vysledky = {}
        obec["strany"] = vysledky

    # Zápis výsledků do CSV souboru
    # Nejprve sestavíme seznam názvů sloupců (hlavičku)
    fieldnames = ["Kód obce", "Název obce", "Voliči", "Obálky", "Platné hlasy"]
    # Přidáme sloupce pro strany seřazené abecedně
    fieldnames += sorted(list(vsechny_strany))
    
    # Otevřeme CSV soubor pro zápis
    csv_file = open(csv_filename, "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    # Zapíšeme data každé obce
    for obec in obce:
        radek = {}
        radek["Kód obce"] = obec["kod"]
        radek["Název obce"] = obec["nazev"]
        radek["Voliči"] = obec["volici"]
        radek["Obálky"] = obec["obalky"]
        radek["Platné hlasy"] = obec["platne"]
        # Pro každou stranu, pokud obec má výsledek, zapíšeme ho, jinak prázdné pole
        for strana in vsechny_strany:
            if strana in obec["strany"]:
                radek[strana] = obec["strany"][strana]
            else:
                radek[strana] = ""
        writer.writerow(radek)
    csv_file.close()
    
    print("Data byla úspěšně uložena do souboru:", csv_filename)

# Spuštění programu
if __name__ == "__main__":
    # Pokud nejsou předány argumenty, přepneme se do testovacího režimu s dummy daty
    if len(sys.argv) == 1:
        sys.argv = ["projekt_3.py",
                    "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101",
                    "dummy_output.csv"]
        # Pro testování bez internetu nahraďme requests.get dummy_get
        requests.get = dummy_get
    main()

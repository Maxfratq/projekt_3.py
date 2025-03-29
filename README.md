# Elections scraper
Projekt 3 pro Engeto Python Akademii

## Popis projektu
Cílem je extrahování výsledků parlamentních voleb v roce 2017 pro vybraný okres [z tohoto odkazu](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) (sloupec *Výběr obce*) a jejich uložení do csv souboru.

## Instalace knihoven
Knihovny použité v kódu jsou uložené v souboru requirements.txt. 

## Spuštění projektu
Soubor projekt_3.py se spouští z příkazového řádku a požaduje dva argumenty.

> python projekt_3.py <odkaz_uzemniho_celku> <vystupni_soubor>

Výstupem pak je soubor .csv s výsledky voleb.

## Ukázka projektu
Výsledky pro okres Cheb:
> 1. argument -> https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101
> 2. argument -> volby.csv.csv


Spuštění programu:
> python   volby17.py   "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101"   "volby.csv"


Běh programu
> stahuji data z URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101
> 
> stahuji data z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=5&xobec=554499&xvyber=4101
> 
> stahuji data z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=5&xobec=554502&xvyber=4101
> 
> stahuji data z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=5&xobec=554511&xvyber=4101
> 
> ...
> 
> UKLÁDÁM DATA DO SOUBORU: volby.csv
> 
> UKONČUJI: projekt_3.py


Částečný výstup:
> Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie,Česká str.sociálně demokrat.,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy, Strana zelených, ...

>554499,Aš,9 766,4 289,4 254,"6,48 %","0,86 %","5,14 %","3,97 %","8,67 %","3,64 %","1,24 %","1,01 %","0,37 %","0,47 %","8,76 %","0,23 %","3,59 %","40,12 %","0,30 %","2,20 %","0,35 %","0,09 %","0,07 %","12,10 %","0,23 %"

>554502,Dolní Žandov,943,532,528,"5,87 %","0,56 %","4,35 %","3,97 %","17,61 %","0,56 %","1,89 %","1,13 %","0,00 %","0,00 %","9,84 %","0,00 %","3,03 %","35,60 %","0,75 %","1,89 %","0,94 %","0,37 %","0,75 %","10,60 %","0,18 %"

>554511,Drmoul,769,486,481,"10,18 %","0,41 %","4,57 %","8,73 %","6,44 %","0,41 %","0,62 %","1,24 %","0,00 %","0,00 %","10,60 %","0,00 %","2,28 %","37,62 %","0,20 %","4,57 %","0,62 %","0,00 %","0,62 %","10,60 %","0,20 %"

# Elections scraper – Projekt 3 do Engeto Online Python Akademie

## Popis projektu
Cílem tohoto projektu je extrahování výsledků parlamentních voleb v roce 2017 pro vybraný okres. Skript načítá data ze stránky, kde je uveden sloupec *Výběr obce*, a následně stahuje detailní stránky jednotlivých obcí. Ze získaných dat jsou extrahovány informace o:
- registrovaných voličích,
- vydaných obálkách,
- platných hlasů,
- procentuálních výsledcích hlasování pro kandidující strany.

Výstupem projektu je CSV soubor, který obsahuje:
- Kód obce,
- Název obce,
- Voliči v seznamu,
- Vydané obálky,
- Platné hlasy,
- Procentuální výsledky hlasů pro jednotlivé strany.

## Instalace knihoven
Všechny knihovny potřebné ke spuštění tohoto skriptu jsou uvedeny v souboru `requirements.txt`.  
Pro instalaci závislostí spusťte:
```bash
pip install -r requirements.txt

## Spuštění projektu  
Skript `main.py` se spouští z příkazového řádku a vyžaduje dva argumenty:  
1. URL územního celku (např. https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3206`)  
2. Název výstupního CSV souboru (např. `vysledky_okresu.csv`)

## Příklad spuštění:
DEBUG: Nalezeno 68 detailních URL.
DEBUG: STAHUJI DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=541095&xvyber=3206
DEBUG: Obec 1/68: nalezeno 25 procentních hodnot
DEBUG: STAHUJI DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=559725&xvyber=3206
DEBUG: Obec 2/68: nalezeno 25 procentních hodnot
DEBUG: STAHUJI DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=559733&xvyber=3206
DEBUG: Obec 3/68: nalezeno 25 procentních hodnot
DEBUG: STAHUJI DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=559741&xvyber=3206
DEBUG: Obec 4/68: nalezeno 25 procentních hodnot
DEBUG: STAHUJI DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=559750&xvyber=3206
DEBUG: Obec 5/68: nalezeno 25 procentních hodnot
DEBUG: STAHUJI DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=559768&xvyber=3206
DEBUG: Obec 6/68: nalezeno 25 procentních hodnot
DEBUG: STAHUJI DATA Z URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xobec=540927&xvyber=3206
DEBUG: Obec 7/68: nalezeno 25 procentních hodnot

## Částečný výstup:
Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,OBČANÉ 2011-SPRAVEDL. PRO LIDI,Referendum o Evropské unii,TOP 09,ANO 2011,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů
541095,Bezděkov,103,73,73,"4,10 %","0,00 %","0,00 %","10,95 %","0,00 %","4,10 %","10,95 %","0,00 %","0,00 %","1,36 %","0,00 %","0,00 %","5,47 %","0,00 %","1,36 %","1,36 %","46,57 %","0,00 %","1,36 %","0,00 %","1,36 %","0,00 %","0,00 %","10,95 %","0,00 %"
559725,Břasy,1 817,1 106,1 103,"11,15 %","0,27 %","0,09 %","6,89 %","0,00 %","3,80 %","10,51 %","0,99 %","0,72 %","1,45 %","0,00 %","0,36 %","9,61 %","0,18 %","0,09 %","3,89 %","34,81 %","0,27 %","2,08 %","0,00 %","1,17 %","0,54 %","0,36 %","10,24 %","0,45 %"
559733,Březina,281,185,184,"13,58 %","0,00 %","0,00 %","3,80 %","0,00 %","6,52 %","4,89 %","0,54 %","0,00 %","0,54 %","0,00 %","0,00 %","3,80 %","0,00 %","0,00 %","4,34 %","49,45 %","0,00 %","1,63 %","0,00 %","1,63 %","0,54 %","0,00 %","8,69 %","0,00 %"
559741,Bujesily,55,39,38,"13,15 %","0,00 %","0,00 %","13,15 %","0,00 %","7,89 %","2,63 %","0,00 %","0,00 %","5,26 %","0,00 %","0,00 %","10,52 %","0,00 %","0,00 %","5,26 %","34,21 %","0,00 %","2,63 %","0,00 %","0,00 %","0,00 %","0,00 %","5,26 %","0,00 %"
559750,Bušovice,488,357,355,"10,14 %","1,12 %","0,00 %","5,91 %","0,28 %","5,35 %","9,85 %","1,40 %","1,12 %","1,12 %","0,28 %","1,12 %","10,70 %","0,00 %","0,84 %","5,63 %","31,54 %","0,28 %","1,40 %","0,00 %","1,69 %","0,00 %","0,00 %","9,57 %","0,56 %"
559768,Cekov,113,75,75,"32,00 %","0,00 %","0,00 %","4,00 %","0,00 %","4,00 %","14,66 %","0,00 %","0,00 %","1,33 %","0,00 %","0,00 %","10,66 %","0,00 %","0,00 %","1,33 %","21,33 %","0,00 %","1,33 %","0,00 %","0,00 %","0,00 %","0,00 %","9,33 %","0,00 %"
540927,Čilá,17,17,17,"41,17 %","0,00 %","0,00 %","0,00 %","0,00 %","0,00 %","0,00 %","5,88 %","0,00 %","0,00 %","0,00 %","0,00 %","29,41 %","0,00 %","0,00 %","0,00 %","23,52 %","0,00 %","0,00 %","0,00 %","0,00 %","0,00 %","0,00 %","0,00 %","0,00 %"
559776,Dobřív,986,615,613,"7,83 %","0,16 %","0,00 %","6,03 %","0,00 %","5,38 %","11,09 %","1,79 %","0,65 %","1,95 %","0,00 %","0,00 %","9,95 %","0,00 %","0,00 %","3,91 %","35,07 %","0,65 %","2,12 %","0,00 %","0,65 %","0,48 %","0,00 %","11,90 %","0,32 %"
530379,Drahoňův Újezd,112,85,85,"10,58 %","0,00 %","0,00 %","7,05 %","0,00 %","0,00 %","17,64 %","0,00 %","1,17 %","15,29 %","2,35 %","0,00 %","8,23 %","0,00 %","0,00 %","4,70 %","25,88 %","0,00 %","2,35 %","0,00 %","0,00 %","0,00 %","0,00 %","4,70 %","0,00 %"
559792,Ejpovice,519,351,349,"14,61 %","0,00 %","0,00 %","7,16 %","0,28 %","4,58 %","7,44 %","1,14 %","0,57 %","1,71 %","0,28 %","0,00 %","10,88 %","0,00 %","0,00 %","7,44 %","20,91 %","0,00 %","4,58 %","0,00 %","2,86 %","1,14 %","0,00 %","13,75 %","0,57 %"
559806,Hlohovice,279,189,189,"7,93 %","0,00 %","0,00 %","10,05 %","0,52 %","1,58 %","8,99 %","2,64 %","0,00 %","1,05 %","0,00 %","0,00 %","7,93 %","0,00 %","0,00 %","2,64 %","40,21 %","0,52 %","1,05 %","0,00 %","0,00 %","0,00 %","0,52 %","14,28 %","0,00 %"
559814,Holoubkov,1 172,720,715,"10,48 %","0,27 %","0,00 %","9,93 %","0,00 %","3,07 %","12,44 %","0,97 %","1,25 %","1,81 %","0,13 %","0,13 %","7,83 %","0,13 %","0,00 %","3,21 %","29,79 %","0,55 %","2,51 %","0,13 %","0,69 %","0,69 %","0,13 %","13,56 %","0,13 %"
559822,Hrádek,2 256,1 205,1 197,"9,94 %","0,25 %","0,00 %","7,60 %","0,25 %","2,84 %","14,53 %","1,33 %","1,08 %","1,08 %","0,16 %","0,16 %","7,76 %","0,25 %","0,16 %","3,09 %","31,16 %","0,25 %","2,00 %","0,00 %","1,08 %","0,75 %","0,33 %","12,61 %","1,25 %"
541001,Hradiště,24,21,21,"28,57 %","0,00 %","0,00 %","19,04 %","0,00 %","4,76 %","0,00 %","0,00 %","4,76 %","0,00 %","0,00 %","0,00 %","9,52 %","0,00 %","0,00 %","4,76 %","14,28 %","0,00 %","0,00 %","0,00 %","0,00 %","0,00 %","4,76 %","9,52 %","0,00 %"
559849,Hůrky,202,144,144,"5,55 %","0,00 %","0,00 %","6,94 %","0,00 %","1,38 %","16,66 %","2,77 %","1,38 %","0,00 %","0,00 %","0,69 %","7,63 %","0,00 %","0,00 %","2,08 %","38,19 %","0,69 %","5,55 %","0,00 %","2,08 %","0,00 %","0,69 %","6,25 %","1,38 %"


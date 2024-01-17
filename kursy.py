#autor: Kacper Grzesik
import datetime
import re
import requests
import os

def wyswietl():
    Lista_faktur = []
    Lista_wplat = []

    import_dane = []

    for line in os.listdir():
        if line.endswith('.faktura'):
            Lista_faktur.append(line[:-8:])

    for line in os.listdir():
        if line.endswith('.wplata'):
            Lista_wplat.append(line[:-7:])

    wybrana = input(f"\nWybierz z listy faktur:\n{Lista_faktur}\n\nWybierz z listy płatności:\n{Lista_wplat}\n\n")

    if wybrana in Lista_faktur:
        nazwa_faktury = wybrana + ".faktura"
        file = open(nazwa_faktury, 'r')
        
        for line in file:
            line = line.strip()
            import_dane.append(line)

        print(f"\nNazwa faktury: {nazwa_faktury}\nWartość: {import_dane[0]}\nWaluta: {import_dane[1]}\nData: {import_dane[2]}\n")
    
    elif wybrana in Lista_wplat:
        nazwa_wplaty = wybrana + ".wplata"
        file = open(nazwa_wplaty, 'r')

        for line in file:
            line = line.strip()
            import_dane.append(line)

        print(f"\nNazwa płatności: {nazwa_wplaty}\nWartość: {import_dane[0]}\nWaluta: {import_dane[1]}\nData: {import_dane[2]}\n")

    else:
        print("\nNie znaleziono pliku.\n")
    
    input("Naciśnij [Enter], aby kontynuować.\n")


def dane(czyFaktura):
    czy_zapisac = False

    if czyFaktura:
        print("\nWpisz dane faktury\n")
    else:
        print("\nWpisz dane płatności\n")
    
    while True:
        kwota = input("Podaj kwote: ")
        kwota = re.sub("\,", ".", kwota) #zamiana ewentualnego przecinka na kropke

        if kwota_walidacja(kwota): break

    while True:
        waluta = input("Podaj walute [PLN/EUR/USD/GBP]: ")
        waluta = waluta.upper() #przyjmowana jest dowolna wielkosc znakow

        if waluta_walidacja(waluta): break
    
    while True:
        data = input("Wprowadz date [rrrr-mm-dd]: ")

        if data_walidacja(data):
            print("\nPomyślnie wprowadzono dane faktury.\n")
            break

    if czyFaktura:
        while True:
            czy_zapisac = input("Czy chcesz zapisać dane faktury?\n[y] - Tak\n[n] - Nie\n")

            if czy_zapisac.lower() == "y":
                zapis_faktury(kwota, waluta, data, True)
                break

            if czy_zapisac.lower() == "n":
                break

            else: print("\nNie rozpoznano znaku.\n")
    
    else:
        while True:
            czy_zapisac = input("Czy chcesz zapisać dane płatności?\n[y] - Tak\n[n] - Nie\n")

            if czy_zapisac.lower() == "y":
                zapis_faktury(kwota, waluta, data, False)
                break

            if czy_zapisac.lower() == "n":
                break

            else: print("\nNie rozpoznano znaku.\n")

    if waluta != "PLN":
        kwotaPrzed = kwota
        kwota = przewalutowanie(kwota, waluta, data)
        print(f"\nPrzekonwertowano {kwotaPrzed} {waluta} na {kwota} PLN.")

    return kwota

def sprawdz_dostepnosc(nazwa):
    for line in os.listdir():
        if str(nazwa).lower() + ".faktura" == line.lower() or str(nazwa).lower() + ".wplata" == line.lower():
            return False
    return True

def zapis_faktury(fKwota, fWaluta, fData, czyFaktura):
    if czyFaktura:
        while True:
            nazwa = input("Wybierz nazwę: ")
            if sprawdz_dostepnosc(nazwa):
                nazwa = nazwa + ".faktura"
                
                if " " in nazwa:
                    print("\nTwoja nazwa nie może zawierać spacji.\n")
                else:
                    f = open(nazwa, "x")
                    f.write(f"{fKwota}\n{fWaluta}\n{fData}")
                    print(f"\nZapisano fakturę pod nazwą: {nazwa}")
                    f.close()
                    return 0
            else: print("\nNazwa niedostępna!\n")
    else:
        while True:
            nazwa = input("Wybierz nazwę: ")
            if sprawdz_dostepnosc(nazwa):
                nazwa = nazwa + ".wplata"
                
                if " " in nazwa:
                    print("\nTwoja nazwa nie może zawierać spacji.\n")
                else:
                    f = open(nazwa, "x")
                    f.write(f"{fKwota}\n{fWaluta}\n{fData}")
                    print(f"\nZapisano płatność pod nazwą: {nazwa}")
                    f.close()
                    return 0
            else: print("\nNazwa niedostępna!\n")

def przewalutowanie(kwota, waluta, data):
    #automatyczne przewalutowanie z pomocą API NBP  /   nie działa, kiedy wybrano dzień, w którym NBP nie zaktualizował dat
    url = 'http://api.nbp.pl/api/exchangerates/tables/A/' + data

    body = requests.get(url)
    response = body.json()

    for rate in response[0]['rates']:
        if waluta == rate['code']:
            wynik = float(kwota) * float(rate['mid'])
            wynik = round(wynik, 2)
            return wynik

def kwota_walidacja(kwota):
    try:
        float(kwota)    

    except ValueError:
        print("Niepoprawny format kwoty. Wprowadź liczbę.")
        return 0
    return 1

def waluta_walidacja(waluta):
    dozwolone = ['PLN', 'USD', 'EUR', 'GBP']

    if waluta in dozwolone: return 1
    else:
        print("Nieobsługiwana waluta.")
        return 0

def data_walidacja(data):
    try:
        datetime.date.fromisoformat(data)
        return 1
    
    except ValueError:
        print("Niepoprawny format daty.")
        return 0


def main():
    while True:
        tryb = input("Wybierz działanie:\n[1] - Dodaj/wpisz fakturę ręcznie\n[2] - Pobierz fakturę z pliku\n[3] - Dodaj/wpisz płatność ręcznie\n[4] - Pobierz fakturę z pliku\n[5] - Usuwanie załadowanych płatności\n[6] - Wyświetl pliki\n[7] - Usuwanie plików\n[8] - Zobacz ile zostało do opłacenia\n[0] - Wyjdź\n")

        if int(tryb) in range(7):
            if tryb == "1": #dodawanie i wpisywanie faktury
                suma = dane(1)
            
            if tryb == "2": #pobieranie faktury z pliku
                print("2")

            if tryb == "3": #dodawanie i wpisywanie platnosci
                platnosc = dane(0)

            if tryb == "4": #pobieranie platnosci z pliku
                print("4")

            if tryb == "5": #usuniecie aktywnej platnosci
                print("5")

            if tryb == "6": #wyswietlenie plikow
                wyswietl()

            if tryb == "7": #obliczenie, ile zostalo do oplacenia faktury
                print("6")

            if tryb == "0": #wyjscie z programu
                tekst = "Program autorstwa: Kacper Grzesik"

                print("-" * len(tekst))
                print(tekst)
                print("-" * len(tekst))
                return 0
        
        else: print("\nNie ropoznano znaku.\n")

if __name__ == "__main__":
    main()
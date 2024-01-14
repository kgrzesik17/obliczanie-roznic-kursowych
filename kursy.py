#autor: Kacper Grzesik
import datetime
import re
import requests

def przewalutowanie(kwota, waluta, data):
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
    #wprowadzanie danych faktury
    print("Wpisz dane faktury\n")
    
    while True:
        fKwota = input("Podaj kwote: ")
        fKwota = re.sub("\,", ".", fKwota) #zamiana ewentualnego przecinka na kropke

        if kwota_walidacja(fKwota): break

    while True:
        fWaluta = input("Podaj walute [PLN/EUR/USD/GBP]: ")
        fWaluta = fWaluta.upper() #przyjmowana jest dowolna wielkosc znakow

        if waluta_walidacja(fWaluta): break
    
    while True:
        fData = input("Wprowadz date [rrrr-mm-dd]: ")

        if data_walidacja(fData):
            print("\nPomyślnie wprowadzono dane faktury.")
            break

    if fWaluta != "PLN":
        fKwotaPrzed = fKwota
        fKwota = przewalutowanie(fKwota, fWaluta, fData)
        print(f"\nPrzekonwertowano {fKwotaPrzed} {fWaluta} na {fKwota} PLN.")

    #wprowadzanie danych platnosci
    print("\nPodaj dane platnosci\n")

    while True:
        pKwota = input("Podaj kwote: ")
        pKwota = re.sub("\,", ".", pKwota) #zamiana ewentualnego przecinka na kropke

        if kwota_walidacja(pKwota): break

    while True:
        pWaluta = input("Podaj walute [PLN/EUR/USD/GBP]: ")
        pWaluta = pWaluta.upper() #przyjmowana jest dowolna wielkosc znakow

        if waluta_walidacja(pWaluta): break

    while True:
        pData = input("Wprowadz date [rrrr-mm-dd]: ")

        if data_walidacja(pData):
            print("\nPomyślnie wprowadzono dane faktury.")
            break

    if pWaluta != "PLN":
        pKwotaPrzed = pKwota
        pKwota = przewalutowanie(pKwota, pWaluta, pData)
        print(f"\nPrzekonwertowano {pKwotaPrzed} {pWaluta} na {pKwota} PLN.")

if __name__ == "__main__":
    main()
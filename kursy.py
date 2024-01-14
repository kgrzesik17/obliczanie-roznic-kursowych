#autor: Kacper Grzesik
import datetime
import re

def kwota_walidacja(kwota):
    try:
        float(kwota)    

    except ValueError:
        print("Niepoprawny format kwoty. Wprowadź liczbę.")
        return 0
    return 1

def waluta_walidacja(waluta):
    dozwolone = ['pln', 'usd', 'eur', 'gbp']

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
        fWaluta = fWaluta.lower() #przyjmowana jest dowolna wielkosc znakow

        if waluta_walidacja(fWaluta): break
    
    while True:
        fData = input("Wprowadz date [rrrr-mm-dd]: ")

        if data_walidacja(fData):
            print("\nPomyślnie wprowadzono dane faktury.")
            break

    #wprowadzanie danych platnosci
    print("\nPodaj dane platnosci\n")

    while True:
        pKwota = input("Podaj kwote: ")

        if kwota_walidacja(pKwota): break

    while True:
        pWaluta = input("Podaj walute [PLN/EUR/USD/GBP]: ")

        if waluta_walidacja(pWaluta): break

    while True:
        pData = input("Wprowadz date [rrrr-mm-dd]: ")
        print("\nPomyślnie wprowadzono dane płatności.")

        if data_walidacja(pData): break

if __name__ == "__main__":
    main()
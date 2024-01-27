# autor: Kacper Grzesik
import datetime
import re
import requests
import os


def usunPlik(do_usuniecia):
    """
    Ta funkcja usuwa plik wybrany przez użytkownika.

    Argumenty: plik do usunięcia (string)
    Zwracane wartości: 0
    """

    potwierdzenie = "n"

    if do_usuniecia == "n n":
        return 0

    if not sprawdz_dostepnosc(do_usuniecia):
        potwierdzenie = input(f"\nCzy na pewno chcesz usunąć plik {do_usuniecia} [y] - Tak / [n] - Nie? ")
        if potwierdzenie == "y":
            if os.path.exists(do_usuniecia + ".faktura"):
                os.remove(do_usuniecia + ".faktura")
                input(f"\nFaktura [{do_usuniecia}] została usunięta. Naciśnij [Enter], aby kontynuować.\n")
            if os.path.exists(do_usuniecia + ".wplata"):
                os.remove(do_usuniecia + ".wplata")
                input(f"\nWpłata [{do_usuniecia}] została usunięta. Naciśnij [Enter], aby kontynuować.\n")
        else:
            return 0
    else:
        input("\nNie znaleziono pliku. Naciśnij [Enter], aby kontynuować.\n\n")


def wyswietl(usun, pobierz):
    """
    Ta funkcja wyświetla, usuwa lub pobiera (z pliku) wartości.

    Argumenty: tryb działania: czy usunąć (int), czy pobrać (int)
    Zwracane wartości: 0 lub pobrana wartość (lista - wartość (float), czy faktura (int))
    """

    Lista_faktur = []
    Lista_wplat = []

    Import_dane = []

    for line in os.listdir():
        if line.endswith('.faktura'):
            Lista_faktur.append(line[:-8:])

    for line in os.listdir():
        if line.endswith('.wplata'):
            Lista_wplat.append(line[:-7:])

    if usun:
        do_usuniecia = input(f"\nWybierz plik do usunięcia (wpisz [n n], jeśli chcesz przerwać akcję.):\nFaktury: {Lista_faktur}\nPłatności: {Lista_wplat}\n")
        if do_usuniecia == "n n":
            return 0
        else:
            usunPlik(do_usuniecia)
            return 0

    elif pobierz:
        wybrana = input(f"\nPobierz z listy faktur:\n{Lista_faktur}\nPobierz z listy płatności:\n{Lista_wplat}\n\n")

    else:
        wybrana = input(f"\nWybierz z listy faktur:\n{Lista_faktur}\n\nWybierz z listy płatności:\n{Lista_wplat}\n\n")

    if wybrana in Lista_faktur:
        nazwa_faktury = wybrana + ".faktura"
        file = open(nazwa_faktury, 'r')

        for line in file:
            line = line.strip()
            Import_dane.append(line)

        if pobierz:
            kwota = Import_dane[0]
            waluta = Import_dane[1]
            data = Import_dane[2]

            wartosc = przewalutowanie(kwota, waluta, data)

            if waluta == "PLN":
                wartosc = kwota

            print(f"\nPomyślnie pobrano fakturę {nazwa_faktury}.\n")

            return [wartosc, 1]

        print(f"\nNazwa faktury: {nazwa_faktury}\nWartość: {Import_dane[0]}\nWaluta: {Import_dane[1]}\nData: {Import_dane[2]}\n")

    elif wybrana in Lista_wplat:
        nazwa_wplaty = wybrana + ".wplata"
        file = open(nazwa_wplaty, 'r')

        for line in file:
            line = line.strip()
            Import_dane.append(line)

        if pobierz:
            kwota = Import_dane[0]
            waluta = Import_dane[1]
            data = Import_dane[2]

            wartosc = przewalutowanie(kwota, waluta, data)

            if waluta == "PLN":
                wartosc = kwota

            print(f"\nPomyślnie pobrano wpłatę {nazwa_wplaty}.\n")

            return [wartosc, 0]

        print(f"\nNazwa płatności: {nazwa_wplaty}\nWartość: {Import_dane[0]}\nWaluta: {Import_dane[1]}\nData: {Import_dane[2]}\n")

    else:
        print("\nNie znaleziono pliku.\n")

    input("Naciśnij [Enter], aby kontynuować.\n")


def dane(czyFaktura):
    """
    Ta funkcja przyjmuje dane od użytkownika.

    Argumenty: czy użytkownik chce dodać fakturę (jeśli nie, użytkownik dodaje płatność)
    Zwracane wartości: kwota (float)
    """

    czy_zapisac = False

    if czyFaktura:
        print("\nWpisz dane faktury\n")
    else:
        print("\nWpisz dane płatności\n")

    while True:
        kwota = input("Podaj kwote: ")
        kwota = re.sub("\,", ".", kwota)  # zamiana ewentualnego przecinka na kropkę

        if kwota_walidacja(kwota):
            break

    while True:
        waluta = input("Podaj walute [PLN/EUR/USD/GBP]: ")
        waluta = waluta.upper()  # przyjmowana jest dowolna wielkosc znakow

        if waluta_walidacja(waluta):
            break

    while True:
        data = input("Wprowadz date [rrrr-mm-dd]: ")

        if data_walidacja(data):
            print("\nPomyślnie wprowadzono dane faktury/płatności.\n")
            break

    if waluta != "PLN":
        kwotaPrzed = kwota
        kwota = przewalutowanie(kwota, waluta, data)
        print(f"Przekonwertowano {kwotaPrzed} {waluta} na {kwota} PLN.\n")

    if czyFaktura:
        while True:
            czy_zapisac = input("Czy chcesz zapisać dane faktury?\n[y] - Tak\n[n] - Nie\n")

            if czy_zapisac.lower() == "y":
                zapis_faktury(kwota, waluta, data, True)
                break

            if czy_zapisac.lower() == "n":
                break

            else:
                print("\nNie rozpoznano znaku.\n")

    else:
        while True:
            czy_zapisac = input("Czy chcesz zapisać dane płatności?\n[y] - Tak\n[n] - Nie\n")

            if czy_zapisac.lower() == "y":
                zapis_faktury(kwota, waluta, data, False)
                break

            if czy_zapisac.lower() == "n":
                break

            else:
                print("\nNie rozpoznano znaku.\n")

    return float(kwota)


def sprawdz_dostepnosc(nazwa):
    """
    Ta funkcja sprawdza dostępność nazwy pliku.

    Argumenty: nazwa pliku proponowana przez użytkownika (string)
    Zwracane wartości: True lub False (bool)
    """

    for line in os.listdir():
        if str(nazwa).lower() + ".faktura" == line.lower() or str(nazwa).lower() + ".wplata" == line.lower():
            return False
    return True


def zapis_faktury(fKwota, fWaluta, fData, czyFaktura):
    """
    Ta funkcja zapisuje wartości wprowadzone przez użytkownika w postaci pliku.

    Argumenty: kwota (float), waluta (string), data (string), czyFaktura(int)
    Zwracane wartości: 0
    """

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
                    print(f"\nZapisano fakturę pod nazwą: {nazwa}\n")
                    f.close()
                    return 0
            else:
                print("\nNazwa niedostępna!\n")
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
            else:
                print("\nNazwa niedostępna!\n")


def przewalutowanie(kwota, waluta, data):
    """
    Ta funkcja przewalutowuje wartość bazując na informacjach z API NBP.

    Argumenty: kwota (float), waluta (string), data (string)
    Zwracane wartości: wynik przewalutowania (float), czy błąd (int)
    """

    # automatyczne przewalutowanie z pomocą API NBP
    url = f'http://api.nbp.pl/api/exchangerates/tables/A/{data}'

    body = requests.get(url)

    if body.status_code == 200:  # sprawdzamy czy żądanie zostało poprawnie przetworzone
        response = body.json()

        for rate in response[0]['rates']:
            if waluta == rate['code']:
                wynik = float(kwota) * float(rate['mid'])
                wynik = round(wynik, 2)
                return wynik

    else:
        wynik = input("Błąd! NBP nie opublikował kursów walut dla tego dnia. Przeliczam wartość na podstawie dnia 2024-01-10.\n")
        
        url = 'http://api.nbp.pl/api/exchangerates/tables/A/2024-01-10'
        body = requests.get(url)

        if body.status_code == 200:  # sprawdzamy czy żądanie zostało poprawnie przetworzone
            response = body.json()

            for rate in response[0]['rates']:
                if waluta == rate['code']:
                    wynik = float(kwota) * float(rate['mid'])
                    wynik = round(wynik, 2)
                    return wynik


def kwota_walidacja(kwota):
    """
    Ta funkcja sprawdza czy użytkownik wpisał poprawny format kwoty.

    Argumenty: kwota (dowolny typ)
    Zwracane wartości: czy format jest prawidłowy (int)
    """

    try:
        float(kwota)

    except ValueError:
        print("Niepoprawny format kwoty. Wprowadź liczbę.")
        return 0
    return 1


def waluta_walidacja(waluta):
    """
    Ta funkcja sprawdza czy użytkownik wpisał poprawną walutę.

    Argumenty: waluta (string)
    Zwracane wartości: czy waluta jest prawidłowa (int)
    """

    dozwolone = ['PLN', 'USD', 'EUR', 'GBP']

    if waluta in dozwolone:
        return 1
    else:
        print("Nieobsługiwana waluta.")
        return 0


def data_walidacja(data):
    """
    Ta funkcja sprawdza czy użytkownik wpisał poprawnie datę.

    Argumenty: data (string)
    Zwracane wartości: czy data jest prawidłowa (int)
    """

    try:
        datetime.date.fromisoformat(data)
        return 1

    except ValueError:
        print("Niepoprawny format daty.")
        return 0


def oplacenie(faktura, platnosci):
    """
    Ta funkcja liczy stan płatności faktury.

    Argumenty: wartość faktury (float), suma wartości płatności (float)
    Zwracane wartości: 0
    """

    wartosc = float(faktura) - float(platnosci)
    wartosc = round(wartosc, 2)

    print(f"\nWartość faktury: {faktura} PLN")
    print(f"Suma wartości wpłat: {platnosci} PLN")

    if wartosc < 0:
        print(f"\nFaktura została opłacona z nadpłatą: {abs(wartosc)} PLN\n")
        input("Naciśnij [Enter], aby kontynuować.\n")
        return 0

    if wartosc > 0:
        print(f"\nFaktura nie została opłacona. Do dopłaty zostało: {wartosc} PLN\n")
        input("Naciśnij [Enter], aby kontynuować.\n")
        return 0

    if wartosc == 0:
        print("\nFaktura została opłacona w całości.\n")
        input("Naciśnij [Enter], aby kontynuować.\n")
        return 0


def main():
    tryby = ['1', '2', '3', '4', '5', '6', '7', '0', '1 -h', '2 -h', '3 -h', '4 -h', '5 -h', '6 -h', '7 -h', '0 -h']
    suma_faktura = 0
    platnosci = []
    nadpisanie = 0

    while True:
        tryb = input("Wybierz działanie:\n[1] - Dodaj/wpisz fakturę ręcznie\n[2] - Dodaj/wpisz płatność ręcznie\n[3] - Pobierz fakturę/płatność z pliku\n[4] - Usuwanie załadowanych płatności/faktur\n[5] - Wyświetl pliki\n[6] - Usuwanie plików\n[7] - Zobacz ile zostało do opłacenia\n[0] - Wyjdź\nWpisz -h po cyfrze (np. [1 -h]), aby wyświetlić pomoc dotyczącą działania.\n")

        if tryb in tryby:
            if tryb == "1":  # dodawanie i wpisywanie faktury
                suma_faktura_n = dane(1)

                while True:
                    if not nadpisanie:
                        suma_faktura = suma_faktura_n
                        nadpisanie = "n"
                        break

                    nadpisanie = input(f"Czy na pewno chcesz nadpisać obecną fakturę opiewającą na {suma_faktura} PLN? [y] - Tak, [n] - Nie: ")

                    if nadpisanie == "y":
                        suma_faktura = suma_faktura_n
                        break
                    elif nadpisanie == "n":
                        print("\nAnulowano.\n")
                        break
                    else:
                        print("\nNie rozpoznano znaku\n")

            if tryb == "1 -h":
                print("\n[1] Pyta użytkownika o dane faktury (wartość, waluta, data). Następnie przeliczą jej wartość na PLN i załadowuje do systemu. W systemie może być jednocześnie aktywna tylko jedna faktura. Jeśli w systemie jest już aktywna faktura, użytkownik będzie musiał potwierdzić jej nadpisanie. Po wpisaniu danych, program spyta użytkownika czy zapisać fakturę do pliku.\n")

                input("Naciśnij [Enter], aby kontynuować.\n")

            if tryb == "2":  # dodawanie i wpisywanie platnosci
                platnosci.append(dane(0))

            if tryb == "2 -h":
                print("\n[2] Pyta użytkownika o dane płatności (wartość, waluta, data). Następnie przelicza jej wartość na PLN i załadowuje ją do systemu. Po wpisaniu danych, program spyta użytkownika czy zapisać płatność do pliku.\n")

                input("Naciśnij [Enter], aby kontynuować.\n")

            if tryb == "3":  # pobieranie danych z pliku
                pobrany = wyswietl(0, 1)

                if pobrany[1]:
                    suma_faktura = float(pobrany[0])
                else:
                    print(pobrany)
                    platnosci.append(float(pobrany[0]))

            if tryb == "3 -h":
                print("\n[3] Pozwala na wybranie faktury lub płatności do załadowania z poprzednio utworzonego pliku.\n")

                input("Naciśnij [Enter], aby kontynuować.\n")

            if tryb == "4":  # usuniecie załadowanej platnosci lub faktury
                usun_zaladowane = input("\nCo chcesz usunąć?\n[1] - Załadowaną fakturę\n[2] - Załadowane płatności\n[0] - Anuluj akcję\n")

                if usun_zaladowane == "1":
                    suma_faktura = 0
                    print("\nPomyślnie usunięto załadowaną fakturę.\n")

                elif usun_zaladowane == "2":
                    wartosc = input(f"\nPłatność o jakiej wartości [PLN] chcesz usunąć? (wpisz [n n], aby przerwać akcję): {platnosci} ")

                    if wartosc == "n n":
                        print("\nAnulowano.\n")
                    elif float(wartosc) in platnosci:
                        platnosci.remove(float(wartosc))
                        print(f"\nPomyślnie usunięto płatność o wartości {wartosc}.\n")
                    else:
                        print("\nNie znaleziono płatności.\n")

                else:
                    print("\nAnulowano akcję.\n")

            if tryb == "4 -h":
                print("\n[4] Pozwala na usunięcie załadowanej faktury lub płatności.\n")

                input("Naciśnij [Enter], aby kontynuować.\n")

            if tryb == "5":  # wyswietlenie plikow
                wyswietl(0, 0)

            if tryb == "5 -h":
                print("\n[5] Wyświetla listę plików utworzonych przez użytkownika oraz pozwala na ich odczytanie.\n")

                input("Naciśnij [Enter], aby kontynuować.\n")

            if tryb == "6":  # usuwanie plików
                wyswietl(1, 0)

            if tryb == "6 -h":
                print("\n[6] Pozwala na usunięcie plików utworzonych przez użytkownika.\n")

                input("Naciśnij [Enter], aby kontynuować.\n")

            if tryb == "7":  # sprawdzenie ile zostalo do oplacenia
                oplacenie(suma_faktura, sum(platnosci))

            if tryb == "7 -h":
                print("\n[7] Oblicza i wyświetla, ile zostało do opłacenia faktury.\n")

                input("Naciśnij [Enter], aby kontynuować.\n")

            if tryb == "0":  # wyjscie z programu
                tekst = "Program autorstwa: Kacper Grzesik"

                print("-" * len(tekst))
                print(tekst)
                print("-" * len(tekst))
                input()
                return 0

            if tryb == "0 -h":
                print("\n[0] Niepotrzebna funkcja. Po co ktoś chciałby zamykać ten świetny program? :)\n")

                input("Naciśnij [Enter], aby kontynuować.\n")

        else:
            print("\nNie ropoznano znaku.\n")


if __name__ == "__main__":
    main()

import math

def wczytaj_dane(nazwa_pliku):
    dane = []
    with open(nazwa_pliku, 'r') as plik:
        for linia in plik:
            linia = linia.strip()  # Usuń białe znaki z początku i końca linii
            if linia:  # Sprawdź, czy linia nie jest pusta
                dane.append([int(x) for x in linia.split(',')])  # Podziel linię na elementy i przekonwertuj je na liczby całkowite
    return dane

# Przykładowe użycie funkcji
nazwa_pliku = 'gieldaLiczby.txt'
tablica_danych = wczytaj_dane(nazwa_pliku)
print(tablica_danych)

def wystapienia_kolumn(tab):
    dicArray = []
    for i in range(len(tab[0])):
        dictionary = {}
        for j in range(len(tab)):
            value = tab[j][i]
            if value not in dictionary:
                dictionary[value] = 1
            else:
                dictionary[value] += 1

        dicArray.append(dictionary)


    return dicArray

dicArray = wystapienia_kolumn(tablica_danych)
print(dicArray)

def entropia(*args):
    entP = 0
    for arg in args:
        entP += arg * math.log(arg,2)
    entP *= -1
    return entP

def oblicz_p(slownik):
    suma_zdarzen = sum(slownik.values())
    prawdopodobienstwo = {}
    for key, value in slownik.items():
        prawdopodobienstwo[key] = value / suma_zdarzen
    return prawdopodobienstwo
def oblicz_prawdopodobienstwo(lista_slownikow):
    wynik = []
    for slownik in lista_slownikow:
        suma_zdarzen = sum(slownik.values())
        prawdopodobienstwo = {}
        for key, value in slownik.items():
            prawdopodobienstwo[key] = value / suma_zdarzen
        wynik.append(prawdopodobienstwo)
    return wynik

prawdopodobienstwoDecyzyjnej = oblicz_prawdopodobienstwo(dicArray)
print(prawdopodobienstwoDecyzyjnej)


#entropia kolumny decyzyjnej
entropiaD = entropia(*prawdopodobienstwoDecyzyjnej[len(prawdopodobienstwoDecyzyjnej)-1].values())
print(entropiaD)
#mała entropia
def znajdz_wartosci_i_indeksy(tabela, wartosc, index_kolumny):
    wyniki = {}
    for wiersz in tabela:
        if wiersz[index_kolumny] == wartosc:
            ostatnia_wartosc = wiersz[-1]
            wyniki[ostatnia_wartosc] = wyniki.get(ostatnia_wartosc, 0) + 1
    return wyniki


#szukana_wartosc = 1
#index_kolumny = 1
#wynik = znajdz_wartosci_i_indeksy(tablica_danych, szukana_wartosc, index_kolumny)
#print("Słownik wartości z ostatniej kolumny dla wartości", szukana_wartosc, "w kolumnie", index_kolumny, "to:")
#print(wynik)

def funkcja_informacji(praw, dane):
    index = 0
    wynik = {}
    for slownik in praw:
        print(slownik)
        funcInf = 0

        for klucz, wartosc in slownik.items():
            #funkcja (klucz,index)
            #print(f"wartość: {wartosc}")
            #print(f"znajdz_wartosci_i_indeksy(dane, klucz, index): {znajdz_wartosci_i_indeksy(dane, klucz, index)}")
           # print(f"*oblicz_p(znajdz_wartosci_i_indeksy(dane, klucz, index)).values(): {oblicz_p(znajdz_wartosci_i_indeksy(dane, klucz, index)).values()}")
           # print(f"entropia(*oblicz_p(znajdz_wartosci_i_indeksy(dane, klucz, index)).values(): {entropia(*oblicz_p(znajdz_wartosci_i_indeksy(dane, klucz, index)).values())}")
            funcInf += wartosc * entropia(*oblicz_p(znajdz_wartosci_i_indeksy(dane, klucz, index)).values())#entropia
        print(f"Wynik{index}: {funcInf}\n")

        if index == len(praw)-1:
            return wynik
        else:
            wynik[index] = funcInf

        index += 1



func_inf = funkcja_informacji(prawdopodobienstwoDecyzyjnej, tablica_danych)

def gain(ent, inf):
    gain_tab = []
    for gain_elem in inf.values():
        gain_tab.append(ent-gain_elem)
    return gain_tab



print(f"Info: {func_inf}")
print(f"EntropD: {entropiaD}")
print(f"Gain: {gain(entropiaD, func_inf)}")

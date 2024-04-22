import math

class wezel:
    def __init__(self):
        self.potomki = []
        self.value = None
        self.decision = None
        self.level = 0
        self.attribute = None

    def __str__(self):
        childrens = ""
        for child in self.potomki:
            childrens += "\n    "
            childrens += "       " * self.level
            childrens += f"{child}"
        node = (
            f"Attribute a{self.attribute + 1}:"
            if self.attribute is not None
            else f" D: {self.decision}"
        )
        value = (
            f" {self.value} ->" if self.value is not None else f" Value: Root ->"
        )
        return f"└─ {value}{node}{childrens}"


def wczytaj_dane(nazwa_pliku):
    dane = []
    with open(nazwa_pliku, 'r') as plik:
        for linia in plik:
            linia = linia.strip()  # Usuń białe znaki z początku i końca linii
            if linia:  # Sprawdź, czy linia nie jest pusta
                dane.append([x for x in linia.split(',')])  # Podziel linię na elementy i przekonwertuj je na liczby całkowite
    return dane

# Przykładowe użycie funkcji
nazwa_pliku = 'breast-cancer.data'
tablica_danych = wczytaj_dane(nazwa_pliku)

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

def entropia(*args):
    entP = 0
    for arg in args:
        entP += arg * math.log(arg,2)
    entP *= -1
    return entP

def oblicz_prawdopodobienstwo(lista_slownikow):
    wynik = []
    for slownik in lista_slownikow:
        suma_zdarzen = sum(slownik.values())
        prawdopodobienstwo = {}
        for key, value in slownik.items():
            prawdopodobienstwo[key] = value / suma_zdarzen
        wynik.append(prawdopodobienstwo)
    return wynik

def znajdz_wartosci(tabela, wartosc, index_kolumny):
    wyniki = {}
    for wiersz in tabela:
        if wiersz[index_kolumny] == wartosc:
            ostatnia_wartosc = wiersz[-1]
            wyniki[ostatnia_wartosc] = wyniki.get(ostatnia_wartosc, 0) + 1
    return wyniki

test = 0
def funkcja_informacji(praw, dane):
    global test
    index = 0
    wynik = {}

    for slownik in praw:
        funcInf = 0

        for klucz, wartosc in slownik.items():
            subTab = [row for row in dane if row[index] == klucz]

            praw = oblicz_prawdopodobienstwo(wystapienia_kolumn(subTab))

            ent = entropia(*praw[len(praw)-1].values())
            funcInf += wartosc * ent

        if index == len(praw)-1:
            return wynik
        else:
            wynik[index] = funcInf

        index += 1


def gain(ent, inf):
    gain_tab = []
    for gain_elem in inf.values():
        if ent - gain_elem >=0:
            gain_tab.append(ent-gain_elem)
        else:
            gain_tab.append(0)
    return gain_tab

def gainRatio(gain,splitInfo):
    gainR = []
    index = 0
    for i in gain:
        if splitInfo[index] != 0:
            gainR.append(i/splitInfo[index])
        else:
            gainR.append(0)
        index += 1
    return gainR

def indeks_najwyzszej_wartosci(tablica):
    if not tablica:  # Sprawdzanie, czy tablica nie jest pusta
        return None
    indeks = 0
    najwyzsza_wartosc = tablica[0]
    for i in range(1, len(tablica)):
        if tablica[i] > najwyzsza_wartosc:
            indeks = i
            najwyzsza_wartosc = tablica[i]
    return indeks

def pobierz_klucze_słownika(tablica, indeks_słownika):
    if not tablica or indeks_słownika >= len(tablica):  # Sprawdzenie, czy tablica nie jest pusta i czy indeks jest prawidłowy
        print("Nieprawidłowy indeks słownika lub tablica jest pusta.")
        return []
    słownik = tablica[indeks_słownika]
    return list(słownik.keys())

def licz(dane):
    dicArray = wystapienia_kolumn(dane)
    prawdopodobienstwoWszystkichSlowników = oblicz_prawdopodobienstwo(dicArray)
    entropiaD = entropia(*prawdopodobienstwoWszystkichSlowników[len(prawdopodobienstwoWszystkichSlowników) - 1].values()) #entropia decyzynjej
    #print(f"Prawdopodobieństwo do Entropii: {prawdopodobienstwoWszystkichSlowników[len(prawdopodobienstwoWszystkichSlowników) - 1].values()}")
    praw = []
    for i in prawdopodobienstwoWszystkichSlowników:
        ent = entropia(*i.values())
        praw.append(ent)
    #print(f"EntropiaD(id{len(prawdopodobienstwoWszystkichSlowników) - 1}): {entropiaD}")
    func_inf = funkcja_informacji(prawdopodobienstwoWszystkichSlowników, dane)
    splitInfo = []
    for i in prawdopodobienstwoWszystkichSlowników:
        splitInfo.append(entropia(*i.values()))

    g = gain(entropiaD, func_inf)
    Ratio = gainRatio(g, splitInfo) #toooo najlepsze Ratio
    index = indeks_najwyzszej_wartosci(Ratio) #toooo index najlepszego ratio
    uniqueValues = pobierz_klucze_słownika(dicArray, index) #tooo wartości uniwersalne węzłów
    return{
        "Ratio" : Ratio,
        "Index" : index,
        "Unique_values": uniqueValues,
        "FuncInf": func_inf,
        "Gain": g
    }

def createNode(dane, value = None, level = 0):
    n = wezel()
    n.value = value
    n.level = level

    wynik = licz(dane)

    bestIndex = wynik["Index"]
    ratio = wynik["Ratio"]
    uniqueValues = wynik["Unique_values"]
    infres = wynik["FuncInf"]
    gain = wynik["Gain"]

    if level == 0:
        index = 0
        for i in infres:
            print(f"Info(a{index + 1}): {infres[index]}")
            index += 1
        index = 0
        print(f"\n")

        for i in gain:
            print(f"Gain(a{index + 1}): {gain[index]}")
            index += 1
        index = 0
        print(f"\n")

        for i in infres:
            print(f"GainRatio(a{index + 1}): {ratio[index]}")
            index += 1
        print(f"\n")


    if ratio[bestIndex] != 0:
        n.attribute = bestIndex
        for value in uniqueValues:
            subTab = [row for row in dane if row[bestIndex] == value]
            child = createNode(subTab, value, level+1)
            n.potomki.append(child)

    else:
        n.decision = dane[0][-1]

    return n


tree = createNode(tablica_danych)

print(tree, "\n" * 5)


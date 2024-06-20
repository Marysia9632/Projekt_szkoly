from tkinter import *
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import tkintermapview


# Ustawienia
szkoly = []
pracownicy = []
zalogowany = False



def ustaw_marker(nazwa, wspolrzedne):
    return map_widget.set_marker(wspolrzedne[0], wspolrzedne[1], text=nazwa)

class Szkoly:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = ustaw_marker(self.nazwa, self.wspolrzedne)

    def pobierz_wspolrzedne(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]


class Pracownik:
    def __init__(self, nazwa, wsp_x, wsp_y, szkola):
        self.nazwa = nazwa
        self.wspolrzedne = (wsp_x, wsp_y)
        self.szkola = szkola
        self.marker = ustaw_marker(self.nazwa, self.wspolrzedne)


def lista_szkol():
    listbox_lista_szkol.delete(0, END)
    for idx, szkola in enumerate(szkoly):
        listbox_lista_szkol.insert(idx, f'{szkola.nazwa} {szkola.lokalizacja}')

def lista_pracownikow():
    listbox_lista_pracownikow.delete(0, END)
    for idx, pracownik in enumerate(pracownicy):
        listbox_lista_pracownikow.insert(idx, f'{pracownik.nazwa} {pracownik.szkola}')

def dodaj_szkole():
    nazwa = entry_nazwa.get()
    lokalizacja = entry_lokalizacja.get()
    nowa_szkola = Szkoly(nazwa, lokalizacja)
    szkoly.append(nowa_szkola)
    lista_szkol()
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_nazwa.focus()

def pokaz_szczegoly_szkol():
    i = listbox_lista_szkol.index(ACTIVE)
    szkola = szkoly[i]
    label_nazwa_szczegoly_szkoly_wartosc.config(text=szkola.nazwa)
    label_lokalizacja_szczegoly_szkoly_wartosc.config(text=szkola.lokalizacja)
    label_wspolrzedne_szczegoly_szkoly_wartosc.config(text=f"{szkola.wspolrzedne[0]:.2f}, {szkola.wspolrzedne[1]:.2f}")
    map_widget.set_zoom(12)
    map_widget.set_position(szkola.wspolrzedne[0], szkola.wspolrzedne[1])

def edytuj_szkole():
    i = listbox_lista_szkol.index(ACTIVE)
    entry_nazwa.insert(0, szkoly[i].nazwa)
    entry_lokalizacja.insert(0, szkoly[i].lokalizacja)
    button_dodaj_szkole.config(text="Zapisz zmiany", command=lambda: aktualizuj_szkole(i))

def aktualizuj_szkole(i):
    szkoly[i].nazwa = entry_nazwa.get()
    szkoly[i].lokalizacja = entry_lokalizacja.get()
    szkoly[i].wspolrzedne = szkoly[i].pobierz_wspolrzedne()
    szkoly[i].marker.delete()
    szkoly[i].marker = map_widget.set_marker(szkoly[i].wspolrzedne[0], szkoly[i].wspolrzedne[1], text=szkoly[i].nazwa)
    lista_szkol()
    button_dodaj_szkole.config(text="Dodaj szkołę", command=dodaj_szkole)
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_nazwa.focus()

def usun_szkole():
    i = listbox_lista_szkol.index(ACTIVE)
    szkoly[i].marker.delete()
    szkoly.pop(i)
    lista_szkol()

def dodaj_pracownika():
    nazwa = entry_nazwa_pracownika.get()
    wsp_x = float(entry_wsp_x.get())
    wsp_y = float(entry_wsp_y.get())
    szkola = entry_szkola.get()
    nowy_pracownik = Pracownik(nazwa, wsp_x, wsp_y, szkola)
    pracownicy.append(nowy_pracownik)
    lista_pracownikow()
    entry_nazwa_pracownika.delete(0, END)
    entry_wsp_x.delete(0, END)
    entry_wsp_y.delete(0, END)
    entry_szkola.delete(0, END)
    entry_nazwa_pracownika.focus()

def pokaz_szczegoly_pracownika():
    i = listbox_lista_pracownikow.index(ACTIVE)
    pracownik = pracownicy[i]
    label_nazwa_szczegoly_pracownika_wartosc.config(text=pracownik.nazwa)
    label_szkola_szczegoly_pracownika_wartosc.config(text=pracownik.szkola)
    label_wspolrzedne_szczegoly_pracownika_wartosc.config(text=f"{pracownik.wspolrzedne[0]}, {pracownik.wspolrzedne[1]}")
    # Zoom na mapie do pozycji pracownika
    map_widget.set_position(pracownik.wspolrzedne[0], pracownik.wspolrzedne[1])
    map_widget.set_zoom(12)

def edytuj_pracownika():
    i = listbox_lista_pracownikow.index(ACTIVE)
    entry_nazwa_pracownika.insert(0, pracownicy[i].nazwa)
    entry_wsp_x.insert(0, pracownicy[i].wspolrzedne[0])
    entry_wsp_y.insert(0, pracownicy[i].wspolrzedne[1])
    entry_szkola.insert(0, pracownicy[i].szkola)
    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: aktualizuj_pracownika(i))

def aktualizuj_pracownika(i):
    pracownicy[i].nazwa = entry_nazwa_pracownika.get()
    pracownicy[i].wspolrzedne = (float(entry_wsp_x.get()), float(entry_wsp_y.get()))
    pracownicy[i].szkola = entry_szkola.get()
    pracownicy[i].marker.delete()
    pracownicy[i].marker = map_widget.set_marker(pracownicy[i].wspolrzedne[0], pracownicy[i].wspolrzedne[1], text=pracownicy[i].nazwa)
    lista_pracownikow()
    button_dodaj_pracownika.config(text="Dodaj pracownika", command=dodaj_pracownika)
    entry_nazwa_pracownika.delete(0, END)
    entry_wsp_x.delete(0, END)
    entry_wsp_y.delete(0, END)
    entry_szkola.delete(0, END)
    entry_nazwa_pracownika.focus()

def usun_pracownika():
    i = listbox_lista_pracownikow.index(ACTIVE)
    pracownicy[i].marker.delete()
    pracownicy.pop(i)
    lista_pracownikow()

def dodaj_poczatkowe_szkoly():
    poczatkowe_szkoly = [
        {"nazwa": "Szkoła Podstawowa nr.8 w Gdańsku", 'lokalizacja': 'Gdańsk'},
        {"nazwa": "Liceum Ogólnokształcące nr.3 w Poznaniu", 'lokalizacja': 'Poznań'},
        {"nazwa": "Technikum nr.2 w Krakowie", 'lokalizacja': 'Kraków'},
        {"nazwa": "Szkoła Podstawowa nr.1 we Wrocławiu", 'lokalizacja': 'Wrocław'},
        {"nazwa": "Liceum Ogólnokształcące nr.4 w Szczecinie", 'lokalizacja': 'Szczecin'}
    ]
    for szkola in poczatkowe_szkoly:
        nowe_szkoly = Szkoly(szkola["nazwa"], szkola["lokalizacja"])
        szkoly.append(nowe_szkoly)
    lista_szkol()

def dodaj_poczatkowych_pracownikow():
    poczatkowi_pracownicy = [
        {"nazwa": "Jakub Kowalski", 'wsp_x': 54.352024, 'wsp_y': 18.646639, 'szkola': 'Szkoła Podstawowa nr.8 w Gdańsku'},
        {"nazwa": "Anna Wiśniewska", 'wsp_x': 52.406374, 'wsp_y': 16.925168, 'szkola': 'Liceum Ogólnokształcące nr.3 w Poznaniu'},
        {"nazwa": "Jan Nowak", 'wsp_x': 50.064651, 'wsp_y': 19.944981, 'szkola': 'Technikum nr.2 w Krakowie'},
        {"nazwa": "Dorota Kaczmarek", 'wsp_x': 51.107883, 'wsp_y': 17.038538, 'szkola': 'Szkoła Podstawowa nr.1 we Wrocławiu'},
        {"nazwa": "Sylwia Wójcik", 'wsp_x': 53.428543, 'wsp_y': 14.552812, 'szkola': 'Liceum Ogólnokształcące nr.4 w Szczecinie'}
    ]
    for pracownik in poczatkowi_pracownicy:
        nowy_pracownik = Pracownik(pracownik["nazwa"], pracownik["wsp_x"], pracownik["wsp_y"], pracownik["szkola"])
        pracownicy.append(nowy_pracownik)
    lista_pracownikow()

def logowanie():
    global zalogowany
    nazwa_uzytkownika = entry_nazwa_uzytkownika.get()
    haslo = entry_haslo.get()
    if nazwa_uzytkownika == "maria" and haslo == "maria":
        zalogowany = True
        login_frame.grid_forget()
        main_frame.grid(row=0, column=0, padx=50)
        dodaj_poczatkowe_szkoly()
        dodaj_poczatkowych_pracownikow()
    else:
        messagebox.showerror("Błąd logowania", "Niepoprawna nazwa użytkownika lub hasło")



# Graficzny interfejs użytkownika(GUI)
root = Tk()
root.title("Aplikacja szkoły")
root.geometry("1200x1000")

# Ramka logowania
login_frame = Frame(root)
label_nazwa_uzytkownika = Label(login_frame, text="Nazwa użytkownika:")
entry_nazwa_uzytkownika = Entry(login_frame)
label_haslo = Label(login_frame, text="Hasło:")
entry_haslo = Entry(login_frame, show="*")
button_login = Button(login_frame, text="Zaloguj się", command=logowanie)

label_nazwa_uzytkownika.grid(row=0, column=0, sticky=W)
entry_nazwa_uzytkownika.grid(row=0, column=1)
label_haslo.grid(row=1, column=0, sticky=W)
entry_haslo.grid(row=1, column=1)
button_login.grid(row=2, column=0, columnspan=2)

login_frame.grid(row=0, column=0, padx=400, pady=100)

# Ramka główna
main_frame = Frame(root)
main_frame.grid_forget()

# Ramki do organizowania struktury
ramka_lista_szkol = Frame(main_frame)
ramka_lista_pracownikow = Frame(main_frame)
ramka_formularz_szkoly = Frame(main_frame)
ramka_formularz_pracownik = Frame(main_frame)
ramka_szczegoly_szkol = Frame(main_frame)
ramka_szczegoly_pracownikow = Frame(main_frame)

ramka_lista_szkol.grid(row=0, column=0, padx=20, sticky=N)
ramka_lista_pracownikow.grid(row=0, column=1, padx=20, sticky=N)
ramka_formularz_szkoly.grid(row=1, column=0, padx=20, pady=20, sticky=N)
ramka_formularz_pracownik.grid(row=1, column=1, padx=20, pady=20, sticky=N)
ramka_szczegoly_szkol.grid(row=0, column=2, rowspan=2, padx=20, pady=20, sticky=N)
ramka_szczegoly_pracownikow.grid(row=2, column=2, rowspan=2, padx=20, pady=20, sticky=N)

# Lista szkol
label_lista_szkol = Label(ramka_lista_szkol, text="Lista szkół: ")
listbox_lista_szkol = Listbox(ramka_lista_szkol, width=50)
button_pokaz_szczegoly_szkoly = Button(ramka_lista_szkol, text="Pokaż szczegóły", command=pokaz_szczegoly_szkol)
button_usun_szkole = Button(ramka_lista_szkol, text="Usuń szkołę", command=usun_szkole)
button_edytuj_szkole = Button(ramka_lista_szkol, text="Edytuj szkołę", command=edytuj_szkole)

label_lista_szkol.grid(row=0, column=0, columnspan=3)
listbox_lista_szkol.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_szkoly.grid(row=2, column=0)
button_usun_szkole.grid(row=2, column=1)
button_edytuj_szkole.grid(row=2, column=2)

# Lista pracowników
label_lista_pracownikow = Label(ramka_lista_pracownikow, text="Lista pracowników: ")
listbox_lista_pracownikow = Listbox(ramka_lista_pracownikow, width=50)
button_pokaz_szczegoly_pracownik = Button(ramka_lista_pracownikow, text="Pokaż szczegóły", command=pokaz_szczegoly_pracownika)
button_usun_pracownika = Button(ramka_lista_pracownikow, text="Usuń pracownika", command=usun_pracownika)
button_edytuj_pracownika = Button(ramka_lista_pracownikow, text="Edytuj pracownika", command=edytuj_pracownika)

label_lista_pracownikow.grid(row=0, column=0, columnspan=3)
listbox_lista_pracownikow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_pracownik.grid(row=2, column=0)
button_usun_pracownika.grid(row=2, column=1)
button_edytuj_pracownika.grid(row=2, column=2)

# Formularz szkoly
label_formularz_szkoly = Label(ramka_formularz_szkoly, text="Formularz szkoły")
label_nazwa = Label(ramka_formularz_szkoly, text="Nazwa szkoły: ")
label_lokalizacja = Label(ramka_formularz_szkoly, text="Lokalizacja szkoły: ")

entry_nazwa = Entry(ramka_formularz_szkoly)
entry_lokalizacja = Entry(ramka_formularz_szkoly)

label_formularz_szkoly.grid(row=0, column=0, columnspan=2)
label_nazwa.grid(row=1, column=0, sticky=W)
label_lokalizacja.grid(row=2, column=0, sticky=W)

entry_nazwa.grid(row=1, column=1)
entry_lokalizacja.grid(row=2, column=1)

button_dodaj_szkole = Button(ramka_formularz_szkoly, text="Dodaj szkołę", command=dodaj_szkole)
button_dodaj_szkole.grid(row=3, column=1, columnspan=2)

# Formularz pracowników
label_formularz_pracownik = Label(ramka_formularz_pracownik, text="Formularz pracownika")
label_nazwa_pracownika = Label(ramka_formularz_pracownik, text="Nazwa pracownika: ")
label_wsp_x = Label(ramka_formularz_pracownik, text="Współrzędna X: ")
label_wsp_y = Label(ramka_formularz_pracownik, text="Współrzędna Y: ")
label_szkola = Label(ramka_formularz_pracownik, text="Szkoła: ")

entry_nazwa_pracownika = Entry(ramka_formularz_pracownik)
entry_wsp_x = Entry(ramka_formularz_pracownik)
entry_wsp_y = Entry(ramka_formularz_pracownik)
entry_szkola = Entry(ramka_formularz_pracownik)

label_formularz_pracownik.grid(row=0, column=0, columnspan=2)
label_nazwa_pracownika.grid(row=1, column=0, sticky=W)
label_wsp_x.grid(row=2, column=0, sticky=W)
label_wsp_y.grid(row=3, column=0, sticky=W)
label_szkola.grid(row=4, column=0, sticky=W)

entry_nazwa_pracownika.grid(row=1, column=1)
entry_wsp_x.grid(row=2, column=1)
entry_wsp_y.grid(row=3, column=1)
entry_szkola.grid(row=4, column=1)

button_dodaj_pracownika = Button(ramka_formularz_pracownik, text="Dodaj pracownika", command=dodaj_pracownika)
button_dodaj_pracownika.grid(row=5, column=1, columnspan=2)

# Szczegóły szkol
label_szczegoly_szkoly = Label(ramka_szczegoly_szkol, text="Szczegóły szkoły")
label_nazwa_szczegoly_szkoly = Label(ramka_szczegoly_szkol, text="Nazwa szkoły: ")
label_lokalizacja_szczegoly_szkoly = Label(ramka_szczegoly_szkol, text="Lokalizacja szkoły: ")
label_wspolrzedne_szczegoly_szkoly = Label(ramka_szczegoly_szkol, text="Współrzędne szkoły: ")

label_nazwa_szczegoly_szkoly_wartosc = Label(ramka_szczegoly_szkol, text="")
label_lokalizacja_szczegoly_szkoly_wartosc = Label(ramka_szczegoly_szkol, text="")
label_wspolrzedne_szczegoly_szkoly_wartosc = Label(ramka_szczegoly_szkol, text="")

label_szczegoly_szkoly.grid(row=0, column=0, columnspan=2)
label_nazwa_szczegoly_szkoly.grid(row=1, column=0, sticky=W)
label_lokalizacja_szczegoly_szkoly.grid(row=2, column=0, sticky=W)
label_wspolrzedne_szczegoly_szkoly.grid(row=3, column=0, sticky=W)

label_nazwa_szczegoly_szkoly_wartosc.grid(row=1, column=1, sticky=W)
label_lokalizacja_szczegoly_szkoly_wartosc.grid(row=2, column=1, sticky=W)
label_wspolrzedne_szczegoly_szkoly_wartosc.grid(row=3, column=1, sticky=W)

# Szczegóły pracowników
label_szczegoly_pracownik = Label(ramka_szczegoly_pracownikow, text="Szczegóły pracownika")
label_nazwa_szczegoly_pracownik = Label(ramka_szczegoly_pracownikow, text="Nazwa pracownika: ")
label_szkola_szczegoly_pracownik = Label(ramka_szczegoly_pracownikow, text="Szkoła: ")
label_wspolrzedne_szczegoly_pracownik = Label(ramka_szczegoly_pracownikow, text="Współrzędne pracownika: ")

label_nazwa_szczegoly_pracownika_wartosc = Label(ramka_szczegoly_pracownikow, text="")
label_szkola_szczegoly_pracownika_wartosc = Label(ramka_szczegoly_pracownikow, text="")
label_wspolrzedne_szczegoly_pracownika_wartosc = Label(ramka_szczegoly_pracownikow, text="")

label_szczegoly_pracownik.grid(row=0, column=0, columnspan=2)
label_nazwa_szczegoly_pracownik.grid(row=1, column=0, sticky=W)
label_szkola_szczegoly_pracownik.grid(row=2, column=0, sticky=W)
label_wspolrzedne_szczegoly_pracownik.grid(row=3, column=0, sticky=W)

label_nazwa_szczegoly_pracownika_wartosc.grid(row=1, column=1, sticky=W)
label_szkola_szczegoly_pracownika_wartosc.grid(row=2, column=1, sticky=W)
label_wspolrzedne_szczegoly_pracownika_wartosc.grid(row=3, column=1, sticky=W)

# Mapa
map_frame = Frame(main_frame)
map_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=20, sticky= W)

map_widget = tkintermapview.TkinterMapView(map_frame, width=600, height=250, corner_radius=0)
map_widget.set_position(52.237049, 21.017532)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0)

root.mainloop()
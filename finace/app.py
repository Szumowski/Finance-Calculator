import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Funkcja do tworzenia bazy danych
def utworz_baze():
    conn = sqlite3.connect('finanse.db')
    c = conn.cursor()

    # Tworzenie tabeli transakcji, jeśli nie istnieje
    c.execute('''CREATE TABLE IF NOT EXISTS transakcje (
                    id INTEGER PRIMARY KEY,
                    data TEXT,
                    kategoria TEXT,
                    kwota REAL,
                    typ TEXT)''')

    conn.commit()
    conn.close()

# Uruchomienie funkcji tworzenia bazy danych
utworz_baze()

class Aplikacja:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.geometry("600x400")
        
        # Tworzenie Notebooka (zakładek)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Zakładka 1: Formularz do wpisywania transakcji
        self.frame1 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame1, text="Dodaj Transakcje")

        self.data_label = tk.Label(self.frame1, text="Data (YYYY-MM-DD):")
        self.data_label.grid(row=0, column=0, padx=10, pady=5)
        self.data_entry = tk.Entry(self.frame1)
        self.data_entry.grid(row=0, column=1, padx=10, pady=5)
        self.data_error = tk.Label(self.frame1, text="", fg="red")
        self.data_error.grid(row=1, columnspan=2)

        self.kategoria_label = tk.Label(self.frame1, text="Kategoria:")
        self.kategoria_label.grid(row=2, column=0, padx=10, pady=5)
        self.kategoria_entry = tk.Entry(self.frame1)
        self.kategoria_entry.grid(row=2, column=1, padx=10, pady=5)
        self.kategoria_error = tk.Label(self.frame1, text="", fg="red")
        self.kategoria_error.grid(row=3, columnspan=2)

        self.kwota_label = tk.Label(self.frame1, text="Kwota:")
        self.kwota_label.grid(row=4, column=0, padx=10, pady=5)
        self.kwota_entry = tk.Entry(self.frame1)
        self.kwota_entry.grid(row=4, column=1, padx=10, pady=5)
        self.kwota_error = tk.Label(self.frame1, text="", fg="red")
        self.kwota_error.grid(row=5, columnspan=2)

        self.typ_label = tk.Label(self.frame1, text="Typ (dochod/wydatek):")
        self.typ_label.grid(row=6, column=0, padx=10, pady=5)
        self.typ_entry = tk.Entry(self.frame1)
        self.typ_entry.grid(row=6, column=1, padx=10, pady=5)
        self.typ_error = tk.Label(self.frame1, text="", fg="red")
        self.typ_error.grid(row=7, columnspan=2)

        self.dodaj_button = tk.Button(self.frame1, text="Dodaj Transakcję", command=self.dodaj_transakcje)
        self.dodaj_button.grid(row=8, columnspan=2, pady=10)

        # Zakładka 2: Wykres wydatków
        self.frame2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2, text="Wykres")

        self.wykres_button = tk.Button(self.frame2, text="Pokaż wykres", command=self.pokaz_wykres)
        self.wykres_button.pack(pady=20)

        # Przechowywanie obiektu wykresu
        self.canvas = None

    def dodaj_transakcje(self):
        # Pobranie wartości z pól formularza
        data = self.data_entry.get()
        kategoria = self.kategoria_entry.get()
        kwota_str = self.kwota_entry.get()  # Pobieramy wartość jako string
        typ = self.typ_entry.get()

        # Resetowanie komunikatów o błędach
        self.data_error.config(text="")
        self.kategoria_error.config(text="")
        self.kwota_error.config(text="")
        self.typ_error.config(text="")

        # Walidacja danych
        valid = True
        if not data:
            self.data_error.config(text="Pole nie może być puste")
            valid = False
        if not kategoria:
            self.kategoria_error.config(text="Pole nie może być puste")
            valid = False
        if not kwota_str:
            self.kwota_error.config(text="Pole nie może być puste")
            valid = False
        else:
            try:
                kwota = float(kwota_str)  # Próba konwersji na float
            except ValueError:
                self.kwota_error.config(text="Kwota musi być liczbą")
                valid = False
        if not typ:
            self.typ_error.config(text="Pole nie może być puste")
            valid = False

        # Jeśli dane są poprawne, zapisujemy transakcję
        if valid:
            conn = sqlite3.connect('finanse.db')
            c = conn.cursor()
            c.execute('''INSERT INTO transakcje (data, kategoria, kwota, typ) 
                         VALUES (?, ?, ?, ?)''', (data, kategoria, kwota, typ))
            conn.commit()
            conn.close()

            # Czyszczenie pól po dodaniu
            self.data_entry.delete(0, 'end')
            self.kategoria_entry.delete(0, 'end')
            self.kwota_entry.delete(0, 'end')
            self.typ_entry.delete(0, 'end')
        else:
            print("Błąd w danych!")

    def pokaz_wykres(self):
        # Jeśli wykres już istnieje, usuwamy go przed rysowaniem nowego
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Pobranie danych do wykresu z bazy danych
        conn = sqlite3.connect('finanse.db')
        c = conn.cursor()
        c.execute('''SELECT kategoria, SUM(kwota) FROM transakcje
                     WHERE typ = 'wydatek' GROUP BY kategoria''')
        dane = c.fetchall()
        conn.close()

        if not dane:
            print("Brak danych do wykresu!")
            return

        kategorie = [item[0] for item in dane]
        kwoty = [item[1] for item in dane]

        # Tworzenie wykresu
        fig, ax = plt.subplots()
        ax.pie(kwoty, labels=kategorie, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Sprawia, że wykres jest okrągły

        # Osadzanie wykresu w aplikacji Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame2)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

# Tworzenie głównego okna
root = tk.Tk()
app = Aplikacja(root)
root.mainloop()

import sqlite3

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

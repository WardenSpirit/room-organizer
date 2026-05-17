# Room Organizer

Room Organizer je nástroj, který automaticky navrhne vhodné rozmístění nábytku v místnosti s omezenými rozměry.  
Cílem projektu je ušetřit uživatelům čas při hledání optimálního uspořádání a nabídnout rychlou vizuální představu o tom, jak může být prostor efektivně využit.

---

## ✨ Funkce

- řešení rozmístění nábytku pomocí matematické optimalizace (SCIP)
- zajištění, že se objekty nepřekrývají
- podpora rotace objektů
- vizuální zobrazení výsledného návrhu pomocí matplotlib
- uživatelský vstup ve formátu JSON

---

## 📦 Instalace

Projekt používá virtuální prostředí a instalaci závislostí přes `requirements.txt`.

1. vytvoř nové prostředí:

```bash
python3 -m venv scipenv
```

2. aktivuj ho:

```bash
source scipenv/bin/activate      # Linux / macOS
scipenv\Scripts\activate         # Windows
```

3. nainstaluj závislosti:

```bash
pip install -r requirements.txt
```

---

## ▶️ Spuštění

Aplikaci lze spustit jednoduchým příkazem:

```bash
python main.py
```

Program:

- načte konfiguraci z `problem.json`
- vyřeší rozmístění nábytku
- otevře grafické okno s vizualizací výsledku

---

## 📝 Příklad vstupu

Soubor `problem.json` obsahuje jednoduchou konfiguraci místnosti a nábytku, například:

```json
{
    "room_size": [
        5.0,
        4.5
    ],
    "rectangles": [
        {
            "index": 0,
            "name": "postel",
            "size": [
                1.8,
                2.1
            ]
        },
        {
            "index": 1,
            "name": "skříň",
            "size": [
                0.8,
                0.6
            ]
        },
        {
            "index": 1,
            "name": "koberec",
            "size": [
                3.2,
                2.4
            ]
        }
    ]
}
```

---

## 🎨 Příklad výstupu

Výstupem je grafické okno s návrhem rozmístění.

---

## 📚 Licence

Tento projekt je licencován pod **[Creative Commons Attribution‑NonCommercial 4.0 International (CC BY‑NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/legalcode)**.

To znamená:

- projekt je možné používat, upravovat a sdílet
- **komerční použití není povoleno**
- je nutné uvést autora

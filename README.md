# Room Organizer

Room Organizer je nástroj, který automaticky navrhne vhodné rozmístění nábytku v místnosti s omezenými rozměry.
Uživatelům může ušetřit čas při hledání uspořádání nábytku a dalších předmětů v místnosti. Využívá přitom metody lineárního programování.

---

## ✨ Funkce

Řeší rozmístění nábytku pomocí matematické optimalizace. (SCIP)

- uživatelský vstup ve formátu JSON
- zajišťuje, že všechny objekty jsou umístěny
- zajišťuje, že se objekty nepřekrývají
- předpokládá obdélníkový tvar objektů
- využívá možnost otáčet objekty o 90°
- možnost vynutit umístění objektu ke stěně
- možnost vynutit umístění objektů vedle sebe
- vizuální zobrazení výsledného návrhu (matplotlib)
    - barvy objektů lze volitelně nastavit

Plánu je se:

- možnost nechat minimalizovat/maximalizovat
    - vzdálenost mezi dvěma objekty
    - rozměr(y) objektu

---

## 📦 Instalace

1. **Vytvoření nového prostředí:**

```bash
python3 -m venv room_organizer_env
```

2. **Aktivace prostředí:**

```bash
source room_organizer_env/bin/activate      # Linux / macOS
room_organizer_env\Scripts\activate         # Windows
```

3. **Instalace závislostí:**
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

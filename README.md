# 🇨🇿 Room Organizer

*English version follows*

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
- možnost nechat minimalizovat/maximalizovat vzdálenost mezi dvěma objekty
- vizuální zobrazení výsledného návrhu (matplotlib)
    - barvy objektů lze volitelně nastavit

Co program neumí (zatím):
- možnost nechat minimalizovat/maximalizovat rozměr(y) objektu s omezením
- možnost zakázat rotaci objektu
- validace konfiguračního souboru
- libovolnost názvu konfiguračního souboru
- interaktivnější grafika
- možnost zadat semínko pro ILP solver
- zlepšená adaptabilita na ILP solver
- složitější tvar místnosti
- zaručení existence přístupové cesty ke všem objektům
    - navíc by cesta měla mít rozumnou šířku

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

Soubor `problem.json` obsahuje jednoduchou konfiguraci místnosti a nábytku. Zde jsou vysvětlivky atributů:

```json
{
    "room_size": [
        4.5,                                    // šířka místnosti*
        3.5                                     // výška místnosti*
    ],
    "items": [
        {
            "name": "postel",                   // jméno
            "size": [
                1.8,                            // šířka objektu*
                2.05                            // výška objektu*
            ],
            "color": "red",                     // barva ve vizualizaci
            "against_wall": {                   // vynutí umístění objektu ke stěně
                "with_side": "vertical",        // strana umístěná ke stěně
                "allowed_walls": [              // povolené stěny, k nimž je umístění vynucováno (implicitně všechny)
                    "left",
                    "bottom",
                    "right"
                ]
            },
            "distance_bonus": {                 // přidá preferenci vzdálenosti od jiného objektu
                "name": "noční stolek",         // odkazovaný objekt*
                "weight": -0.5                  // váha (hodí se v případě více preferencí), implicitně 1
            }
        },
        {
            "name": "noční stolek",
            "size": [
                0.5,
                0.3
            ],
            "color": "black",
            "beside": {                         // vynucení umístění tohoto objektu vedle jiného
                "name": "postel",               // odkazovaný objekt*
                "self_side": "horizontal",      // sousedící strana tohoto objektu (stolku)*
                "that_side": "horizontal"       // sousedící strana odkazovaného objektu (postele)*
            }
        }
    ]
}
```
*: atribut je na této úrovni povinný

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


Here is the **English translation** of your README — clear, natural, and faithful to the original meaning, while keeping the structure intact.

---

# 🇬🇧 Room Organizer

Room Organizer is a tool that automatically proposes suitable furniture layouts for a room with limited dimensions.
It can save users time when searching for an arrangement of furniture and other items in a room. Using linear programming methods.

---

## ✨ Features

Solves furniture placement using mathematical optimization (SCIP).

- user input in JSON format
- ensures that all objects are placed
- ensures that objects do not overlap
- assumes rectangular object shapes
- supports 90° object rotation
- option to force an object to be placed against a wall
- option to force objects to be placed next to each other
- option to minimize/maximize the distance between two objects
- visual representation of the final layout (matplotlib)
    - object colors can be optionally customized

What the program cannot do (yet):

- minimize/maximize object dimension(s) with constraints
- forbid object rotation
- configuration file validation
- arbitrary configuration file name
- more interactive graphics
- ability to set a seed for the ILP solver
- improved adaptability to different ILP solvers
- more complex room shapes
- guarantee that all objects are reachable via a path
    - and the path should have a reasonable width

---

## 📦 Installation

1. **Create a new environment:**

```bash
python3 -m venv room_organizer_env
```

2. **Activate the environment:**

```bash
source room_organizer_env/bin/activate      # Linux / macOS
room_organizer_env\Scripts\activate         # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## ▶️ Running

You can run the application with a simple command:

```bash
python main.py
```

The program will:

- load the configuration from `problem.json`
- solve the furniture layout
- open a graphical window with the visualization of the result

---

## 📝 Example Input

The file `problem.json` contains a simple configuration of a room and furniture.
Here is an explanation of the attributes:

```json
{
    "room_size": [
        4.5,                                    // room width*
        3.5                                     // room height*
    ],
    "items": [
        {
            "name": "bed",                      // name
            "size": [
                1.8,                            // object width*
                2.05                            // object height*
            ],
            "color": "red",                     // color in visualization
            "against_wall": {                   // force object placement against a wall
                "with_side": "vertical",        // side placed against the wall
                "allowed_walls": [              // allowed walls (defaults to all)
                    "left",
                    "bottom",
                    "right"
                ]
            },
            "distance_bonus": {                 // adds a distance preference to another object
                "name": "nightstand",           // referenced object*
                "weight": -0.5                  // weight (useful for multiple preferences), default 1
            }
        },
        {
            "name": "nightstand",
            "size": [
                0.5,
                0.3
            ],
            "color": "black",
            "beside": {                         // force this object to be placed next to another
                "name": "bed",                  // referenced object*
                "self_side": "horizontal",      // touching side of this object*
                "that_side": "horizontal"       // touching side of the referenced object*
            }
        }
    ]
}
```

\*: attribute is required at this level

---

## 🎨 Example Output

The output is a graphical window showing the proposed layout.

---

## 📚 License

This project is licensed under the **[Creative Commons Attribution‑NonCommercial 4.0 International (CC BY‑NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/legalcode)** license.

This means:

- the project may be used, modified, and shared
- **commercial use is not allowed**
- attribution to the author is required

---

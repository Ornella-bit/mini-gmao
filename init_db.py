import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "gmao.db"
SCHEMA = Path(__file__).parent / "schema.sql"

connexion = sqlite3.connect(DB)
connexion.executescript(SCHEMA.read_text(encoding="utf-8"))

# Données fictives, ajoutées seulement si la base est vide
if connexion.execute("SELECT COUNT(*) FROM lieux").fetchone()[0] == 0:
    connexion.executemany(
        "INSERT INTO lieux (nom, type) VALUES (?, ?)",
        [
            ("Appartement A1", "Appartement"),
            ("Duplex B2", "Duplex"),
            ("Local technique", "Partie commune"),
        ],
    )
    connexion.executemany(
        "INSERT INTO equipements (nom, categorie, lieu_id, etat, date_installation) "
        "VALUES (?, ?, ?, ?, ?)",
        [
            ("Chauffe-eau", "Plomberie", 1, "En service", "2023-03-10"),
            ("Climatiseur salon", "Climatisation", 2, "En panne", "2022-07-01"),
            ("Groupe électrogène", "Électricité", 3, "En service", "2021-11-15"),
        ],
    )
    connexion.commit()

connexion.close()
print("Base de données prête.")

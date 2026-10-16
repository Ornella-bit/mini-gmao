import sqlite3
from pathlib import Path
from flask import Flask, render_template

DB = Path(__file__).parent / "gmao.db"

app = Flask(__name__)


def get_db():
    connexion = sqlite3.connect(DB)
    connexion.row_factory = sqlite3.Row    # accès aux colonnes par leur nom
    return connexion


@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/equipements")
def liste_equipements():
    connexion = get_db()
    equipements = connexion.execute(
        """SELECT equipements.id, equipements.nom, equipements.categorie,
                  equipements.etat, lieux.nom AS lieu
           FROM equipements
           JOIN lieux ON equipements.lieu_id = lieux.id
           ORDER BY equipements.nom"""
    ).fetchall()
    connexion.close()
    return render_template("equipements.html", equipements=equipements)


if __name__ == "__main__":
    app.run(debug=True)
    
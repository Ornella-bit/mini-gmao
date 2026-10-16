import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, abort

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

@app.route("/equipements/ajouter", methods=["GET", "POST"])
def ajouter_equipement():
    connexion = get_db()

    if request.method == "POST":
        nom = request.form["nom"].strip()
        categorie = request.form["categorie"].strip()
        lieu_id = request.form["lieu_id"]
        etat = request.form["etat"]
        date_installation = request.form["date_installation"] or None

        if nom and categorie:
            connexion.execute(
                "INSERT INTO equipements (nom, categorie, lieu_id, etat, date_installation) "
                "VALUES (?, ?, ?, ?, ?)",
                (nom, categorie, lieu_id, etat, date_installation),
            )
            connexion.commit()
            connexion.close()
            return redirect(url_for("liste_equipements"))

    lieux = connexion.execute("SELECT id, nom FROM lieux ORDER BY nom").fetchall()
    connexion.close()
    return render_template("ajouter_equipement.html", lieux=lieux)

@app.route("/equipements/<int:equipement_id>/modifier", methods=["GET", "POST"])
def modifier_equipement(equipement_id):
    connexion = get_db()
    equipement = connexion.execute(
        "SELECT * FROM equipements WHERE id = ?", (equipement_id,)
    ).fetchone()
    if equipement is None:
        connexion.close()
        abort(404)

    if request.method == "POST":
        nom = request.form["nom"].strip()
        categorie = request.form["categorie"].strip()
        if nom and categorie:
            connexion.execute(
                "UPDATE equipements SET nom = ?, categorie = ?, lieu_id = ?, "
                "etat = ?, date_installation = ? WHERE id = ?",
                (
                    nom,
                    categorie,
                    request.form["lieu_id"],
                    request.form["etat"],
                    request.form["date_installation"] or None,
                    equipement_id,
                ),
            )
            connexion.commit()
            connexion.close()
            return redirect(url_for("liste_equipements"))

    lieux = connexion.execute("SELECT id, nom FROM lieux ORDER BY nom").fetchall()
    connexion.close()
    return render_template("modifier_equipement.html", equipement=equipement, lieux=lieux)


@app.route("/equipements/<int:equipement_id>/supprimer", methods=["POST"])
def supprimer_equipement(equipement_id):
    connexion = get_db()
    connexion.execute("DELETE FROM equipements WHERE id = ?", (equipement_id,))
    connexion.commit()
    connexion.close()
    return redirect(url_for("liste_equipements"))

if __name__ == "__main__":
    app.run(debug=True)
    
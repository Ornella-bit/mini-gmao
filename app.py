import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import date

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
    connexion.execute("DELETE FROM pannes WHERE equipement_id = ?", (equipement_id,))
    connexion.execute("DELETE FROM equipements WHERE id = ?", (equipement_id,))
    connexion.commit()
    connexion.close()
    return redirect(url_for("liste_equipements"))

@app.route("/pannes")
def liste_pannes():
    connexion = get_db()
    pannes = connexion.execute(
        """SELECT pannes.id, pannes.date_declaration, pannes.description,
                  pannes.gravite, pannes.statut, equipements.nom AS equipement
           FROM pannes
           JOIN equipements ON pannes.equipement_id = equipements.id
           ORDER BY (pannes.statut = 'Résolue'), pannes.date_declaration DESC"""
    ).fetchall()
    connexion.close()
    return render_template("pannes.html", pannes=pannes)


@app.route("/pannes/declarer", methods=["GET", "POST"])
def declarer_panne():
    connexion = get_db()
    if request.method == "POST":
        description = request.form["description"].strip()
        equipement_id = request.form["equipement_id"]
        if description:
            connexion.execute(
                "INSERT INTO pannes (equipement_id, date_declaration, description, gravite) "
                "VALUES (?, ?, ?, ?)",
                (equipement_id, date.today().isoformat(), description, request.form["gravite"]),
            )
            connexion.execute(
                "UPDATE equipements SET etat = 'En panne' WHERE id = ?", (equipement_id,)
            )
            connexion.commit()
            connexion.close()
            return redirect(url_for("liste_pannes"))
    equipements = connexion.execute(
        "SELECT id, nom FROM equipements ORDER BY nom"
    ).fetchall()
    connexion.close()
    return render_template("declarer_panne.html", equipements=equipements)


@app.route("/pannes/<int:panne_id>/statut", methods=["POST"])
def changer_statut_panne(panne_id):
    nouveau_statut = request.form["statut"]
    if nouveau_statut not in ("Ouverte", "En cours", "Résolue"):
        abort(400)
    connexion = get_db()
    panne = connexion.execute(
        "SELECT equipement_id FROM pannes WHERE id = ?", (panne_id,)
    ).fetchone()
    if panne is None:
        connexion.close()
        abort(404)

    connexion.execute("UPDATE pannes SET statut = ? WHERE id = ?", (nouveau_statut, panne_id))

    if nouveau_statut == "Résolue":
        restantes = connexion.execute(
            "SELECT COUNT(*) FROM pannes WHERE equipement_id = ? AND statut != 'Résolue'",
            (panne["equipement_id"],),
        ).fetchone()[0]
        if restantes == 0:    # plus aucune panne ouverte : l'équipement est réparé
            connexion.execute(
                "UPDATE equipements SET etat = 'En service' WHERE id = ?",
                (panne["equipement_id"],),
            )
    else:
        connexion.execute(
            "UPDATE equipements SET etat = 'En panne' WHERE id = ?",
            (panne["equipement_id"],),
        )
    connexion.commit()
    connexion.close()
    return redirect(url_for("liste_pannes"))

if __name__ == "__main__":
    app.run(debug=True)
    
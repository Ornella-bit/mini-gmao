# Mini-GMAO

**Démo en ligne : https://ashley.pythonanywhere.com** (données fictives)

Application web de gestion de maintenance (GMAO) : suivi des équipements, des pannes, des interventions et du stock de pièces détachées.

## Fonctionnalités
- **Équipements** : ajout, modification, suppression, fiche détaillée avec l'historique des pannes et interventions.
- **Pannes** : déclaration avec gravité, suivi du statut (ouverte, en cours, résolue).
- **Interventions** : technicien, travaux réalisés, durée, pièces utilisées.
- **Stock de pièces** : décompte automatique à chaque intervention, alerte de stock bas, réapprovisionnement.
- **Tableau de bord** : indicateurs, pannes à traiter, pièces à réapprovisionner.

## Règles métier
- Un équipement repasse « En service » seulement quand **toutes** ses pannes sont résolues.
- Une intervention ne peut pas consommer plus de pièces que le stock disponible.

## Technologies
Python, Flask, SQLite, templates Jinja2, HTML/CSS. Hébergé sur PythonAnywhere.

## Lancer en local
```
git clone https://github.com/Ornella-bit/mini-gmao.git
cd mini-gmao
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
python app.py
```
Puis ouvrir http://127.0.0.1:5000

## Base de données
Six tables : `lieux`, `equipements`, `pannes`, `interventions`, `pieces`, `interventions_pieces`. Le schéma est dans `schema.sql`, les données fictives de démonstration dans `init_db.py`.

## Limites et pistes d'amélioration
- Pas d'authentification : c'est une démonstration avec des données fictives.
- Idées : connexion des utilisateurs, recherche et filtres, export CSV, tests automatisés.

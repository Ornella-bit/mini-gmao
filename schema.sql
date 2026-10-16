CREATE TABLE IF NOT EXISTS lieux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equipements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    categorie TEXT NOT NULL,
    lieu_id INTEGER NOT NULL,
    etat TEXT NOT NULL DEFAULT 'En service',
    date_installation TEXT,
    FOREIGN KEY (lieu_id) REFERENCES lieux (id)
);

CREATE TABLE IF NOT EXISTS pannes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipement_id INTEGER NOT NULL,
    date_declaration TEXT NOT NULL,
    description TEXT NOT NULL,
    gravite TEXT NOT NULL DEFAULT 'Moyenne',
    statut TEXT NOT NULL DEFAULT 'Ouverte',
    FOREIGN KEY (equipement_id) REFERENCES equipements (id)
);

CREATE TABLE IF NOT EXISTS interventions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    panne_id INTEGER NOT NULL,
    date_intervention TEXT NOT NULL,
    technicien TEXT NOT NULL,
    description TEXT NOT NULL,
    duree_heures REAL,
    FOREIGN KEY (panne_id) REFERENCES pannes (id)
);


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

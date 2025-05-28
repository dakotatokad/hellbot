CREATE TABLE IF NOT EXISTS weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class INT NOT NULL,
    category INT NOT NULL,
    FOREIGN KEY (class) REFERENCES weapon_class(id),
    FOREIGN KEY (category) REFERENCES weapon_category(id)
);

CREATE TABLE IF NOT EXISTS weapon_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class VARCHAR(50) NOT NULL
);

INSERT INTO weapon_class (class) VALUES
('assault rifle'),
('submachine gun'),
('shotgun'),
('marksman rifle'),
('energy weapon'),
('explosive'),
('pistol'),
('melee'),
('special'),
('throwable');

CREATE TABLE IF NOT EXISTS weapon_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(50) NOT NULL
);

INSERT INTO weapon_category (category) VALUES
('primary'),
('sidearm'),
('grenades');

CREATE TABLE IF NOT EXISTS strategems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type INT NOT NULL,
    class INT NOT NULL,
    FOREIGN KEY (type) REFERENCES strategem_type(id),
    FOREIGN KEY (class) REFERENCES strategem_class(id)
);


CREATE TABLE IF NOT EXISTS strategem_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50) NOT NULL
);

INSERT INTO strategem_type (type) VALUES
('offensive'),
('supply'),
('defensive'),
('support');


CREATE TABLE IF NOT EXISTS strategem_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class TEXT NOT NULL
);

INSERT INTO strategem_class (class) VALUES
('orbital strike'),
('backpacks'),
('eagle'),
('vehicles'),
('weapon'),
('sentry'),
('emplacement');

INSERT INTO strategems (name, type, class) VALUES
('Orbital Precision Strike', 1, 1),
('Orbital Gatling Barrage', 1, 1),
('Orbital Airburst Strike', 1, 1),
('Orbital Napalm Barrage', 1, 1),
('Orbital 120MM HE Barrage', 1, 1),
('Orbital Walking Barrage', 1, 1),
('Orbital 380MM HE Barrage', 1, 1),
('Orbital Railcannon Strike', 1, 1),
('Orbital Laser', 1, 1),
('Orbital EMS Strike', 1, 1),
('Orbital Gas Strike', 1, 1),
('Orbital Smoke Strike', 1, 1),
('Shield Generator Pack', 2, 2),
('Directional Shield', 2, 2),
('Ballistic Shield Backpack', 2, 2),
('Hover Pack', 2, 2),
('Supply Pack', 2, 2),
('Portable Hellbomb', 2, 2),
('Jump Pack', 2, 2),
('"Guard Dog"', 2, 2),
('"Guard Dog" Rover', 2, 2),
('"Guard Dog" Dog Breath', 2, 2),
('Fast Recon Vehicle', 2, 4),
('Emancipator Exosuit', 2, 4),
('Patriot Exosuit', 2, 4),
('Eagle 500kg Bomb', 1, 3),
('Eagle Strafing Run', 1, 3),
('Eagle 110MM Rocket Pods', 1, 3),
('Eagle Airstrike', 1, 3),
('Eagle Cluster Bomb', 1, 3),
('Eagle Napalm Strike', 1, 3),
('Eagle Smoke Strike', 1, 3),
('One True Flag', 4, 2),
('Machine Gun', 4, 5),
('Stalwart', 4, 5),
('Heavy Machine Gun', 4, 5),
('Railgun', 4, 5),
('Anti-Material Rifle', 4, 5),
('Grenade Launcher', 4, 5),
('Sterilizer', 4, 5),
('Flamethrower', 4, 5),
('Laser Cannon', 4, 5),
('Quasar Cannon', 4, 5),
('Arc Thrower', 4, 5),
('Commando', 4, 5),
('Expendable Anti-Tank', 4, 5),
('Autocannon', 4, 2),
('Airburst Rocket Launcher', 4, 2),
('Spear', 4, 2),
('StA-X3_W.A.S.P.', 4, 2),
('Recoilless Rifle', 4, 2),
('Gatling Sentry', 3, 6),
('Machine Gun Sentry', 3, 6),
('Flame Sentry', 3, 6),
('Rocket Sentry', 3, 6),
('Autocannon Sentry', 3, 6),
('EMS Mortar Sentry', 3, 6),
('Mortar Sentry', 3, 6),
('Shield Generator Relay', 3, 7),
('Grenadier Battlement', 3, 7),
('Anti-Tank Emplacement', 3, 7),
('HMG Emplacement', 3, 7),
('Tesla Tower', 3, 7),
('Anti-Tank Mines', 3, 7),
('Gas Mines', 3, 7),
('Anti-Personnel Minefield', 3, 7),
('Incendiary Mines', 3, 7)

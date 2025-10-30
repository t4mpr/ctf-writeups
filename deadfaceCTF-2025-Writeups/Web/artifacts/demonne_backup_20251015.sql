-- De Monne Financial Database Backup
-- Generated: 2025-10-15 03:42:18
-- Database Version: SQLite 3.39.4
-- Backup Type: Full

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    department TEXT NOT NULL
);

INSERT INTO users VALUES(1,'jreed80','J0nnyR#ed80!','Johnathan Reed','jreed@demonne.com','Finance');
INSERT INTO users VALUES(2,'lrebarchek','SecureP@ss123','Lorianne Rebarchek','lrebarchek@demonne.com','IT Infrastructure');
INSERT INTO users VALUES(3,'mthompson','Welcome2024!','Michael Thompson','mthompson@demonne.com','Operations');
INSERT INTO users VALUES(4,'sdavis','Bank$ecure99','Sarah Davis','sdavis@demonne.com','Compliance');
INSERT INTO users VALUES(5,'admin','Admin2025!Secure','System Administrator','admin@demonne.com','IT Security');

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    description TEXT,
    date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO transactions VALUES(1,1,5000.00,'Wire Transfer - Q4 Operations','2025-09-12');
INSERT INTO transactions VALUES(2,1,-2500.00,'Vendor Payment - TechSupply Co','2025-09-15');
INSERT INTO transactions VALUES(3,2,1250.00,'Payroll Deposit','2025-09-30');
INSERT INTO transactions VALUES(4,3,75000.00,'Investment Transfer','2025-10-01');
INSERT INTO transactions VALUES(5,4,-450.00,'Compliance Software License','2025-10-05');

CREATE TABLE system_config (
    config_key TEXT PRIMARY KEY,
    config_value TEXT NOT NULL,
    last_modified TEXT
);

INSERT INTO system_config VALUES('backup_schedule','daily','2025-10-15');
INSERT INTO system_config VALUES('encryption_enabled','true','2025-09-01');
INSERT INTO system_config VALUES('maintenance_mode','false','2025-10-10');

COMMIT;

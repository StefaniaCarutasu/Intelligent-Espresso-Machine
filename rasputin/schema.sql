DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  remember BOOLEAN,
  birth_date DATE
);


DROP TABLE IF EXISTS beverages_types;

CREATE TABLE beverages_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    coffee_quantity INTEGER NOT NULL,              -- ml of espresso
    milk_quantity INTEGER NOT NULL,                -- ml of milk
    milk_froth BOOLEAN NOT NULL,
    coffee_type TEXT NOT NULL                      -- hot or cold
);


DROP TABLE IF EXISTS user_preference;

CREATE TABLE user_preference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE ,
    beverage_id INTEGER,
    roast_type TEXT NOT NULL,
    flavour_type TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (beverage_id) REFERENCES beverages_types(id)
);


DROP TABLE IF EXISTS preprogrammed_coffee;

CREATE TABLE preprogrammed_coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    beverage_id INTEGER,
    roast_type TEXT NOT NULL,
    flavour_type TEXT,
    start_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (beverage_id) REFERENCES beverages_types(id)
);


DROP TABLE IF EXISTS machine_state;

CREATE TABLE machine_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coffee_quantity INTEGER NOT NULL,
    milk_quantity INTEGER NOT NULL,
    syrup_quantity INTEGER NOT NULL,
    broken BOOLEAN NOT NULL
);




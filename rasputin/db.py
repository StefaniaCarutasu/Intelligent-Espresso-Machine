import sqlite3
import click
from flask import g, current_app
from flask.cli import with_appcontext

# getting db connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'rasputin.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# closing db connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# initialize db
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command(name='alter-db')
@with_appcontext
def alter_db_command():
    db = get_db()
    db.execute("ALTER TABLE user_preference ADD COLUMN syrup boolean")
    db.execute("ALTER TABLE preprogrammed_coffee ADD COLUMN syrup boolean")
    db.commit()

    click.echo('Altered the database.')

@click.command(name='populate-coffee-table')
@with_appcontext
def populateCoffeeTable():
    db_local = get_db()
    db_local.execute(
        "INSERT INTO beverages_types (name, coffee_quantity, milk_quantity, milk_froth, coffee_type) VALUES (?, ?, ?, ?, ?)",
        ("Latte", 100, 80, True, 'Hot'),
    )
    db_local.execute(
        "INSERT INTO beverages_types (name, coffee_quantity, milk_quantity, milk_froth, coffee_type) VALUES (?, ?, ?, ?, ?)",
        ("Machiatto", 150, 0, True, 'Hot'),
    )
    db_local.execute(
        "INSERT INTO beverages_types (name, coffee_quantity, milk_quantity, milk_froth, coffee_type) VALUES (?, ?, ?, ?, ?)",
        ("Frappe", 70, 100, True, 'Cold'),
    )
    db_local.execute(
        "INSERT INTO beverages_types (name, coffee_quantity, milk_quantity, milk_froth, coffee_type) VALUES (?, ?, ?, ?, ?)",
        ("Espresso", 50, 0, False, 'Hot'),
    )
    db_local.execute(
        "INSERT INTO beverages_types (name, coffee_quantity, milk_quantity, milk_froth, coffee_type) VALUES (?, ?, ?, ?, ?)",
        ("Cappuccino", 100, 100, True, 'Hot'),
    )
    db_local.execute(
        "INSERT INTO beverages_types (name, coffee_quantity, milk_quantity, milk_froth, coffee_type) VALUES (?, ?, ?, ?, ?)",
        ("Flat White", 80, 120, False, 'Hot'),
    )
    db_local.execute(
        "INSERT INTO beverages_types (name, coffee_quantity, milk_quantity, milk_froth, coffee_type) VALUES (?, ?, ?, ?, ?)",
        ("Iced Coffee", 120, 30, False, 'Cold'),
    )
    db_local.commit()
    click.echo("Coffee table modified")
    
def get_min_milk_val():
    db_local = get_db()
    cursor = db_local.cursor()
    tableList = cursor.execute("SELECT milk_quantity FROM beverages_types").fetchall()
    milk_vals = [table[0] for table in tableList]
    min_val = min([elem for elem in milk_vals])
    return min_val

def get_min_coffee_val():
    db_local = get_db()
    cursor = db_local.cursor()
    tableList = cursor.execute("SELECT coffee_quantity FROM beverages_types").fetchall()
    coffee_vals = [table[0] for table in tableList]
    min_val = min([elem for elem in coffee_vals])
    return min_val

def get_syrup_val():
    db_local = get_db()
    cursor = db_local.cursor()
    min_val = cursor.execute("SELECT syrup_quantity FROM machine_state").fetchone()
    return min_val

@click.command(name='populate-machine-state')
@with_appcontext
def populate_machine_state():
    db_local = get_db()
    db_local.execute(
        "INSERT INTO machine_state (coffee_quantity, milk_quantity, syrup_quantity, broken) VALUES (?, ?, ?, ?)",
        (1000, 1000, 100, False),
    )
    db_local.commit()

@click.command(name='change-machine-state')
@with_appcontext
def change_machine_state():
    db_local = get_db()
    cursor = db_local.cursor()
    
    cursor.execute("SELECT * from machine_state")
    machine_id = cursor.fetchone()['id']

    db_local.execute(
        "UPDATE machine_state SET coffee_quantity = ?, milk_quantity = ?, syrup_quantity = ? WHERE id = ?",
        (49, 49, 9, machine_id)
    )
    db_local.commit()
    click.echo("Machine state modified")

@click.command(name='broken-machine')
@with_appcontext
def add_broken_state():
    db_local = get_db()
    cursor = db_local.cursor()
    
    cursor.execute("SELECT * from machine_state")
    machine_id = cursor.fetchone()['id']

    db_local.execute(
        "UPDATE machine_state SET broken = True WHERE id = ?",
        (machine_id,),
    )
    db_local.commit()

@click.command(name='fix-machine')
@with_appcontext
def add_fixed_state():
    db_local = get_db()
    cursor = db_local.cursor()
    
    cursor.execute("SELECT * from machine_state")
    machine_id = cursor.fetchone()['id']

    db_local.execute(
        "UPDATE machine_state SET broken = False WHERE id = ?",
        (machine_id,),
    )
    db_local.commit()


# register db functions to app
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(alter_db_command)
    app.cli.add_command(populateCoffeeTable)
    app.cli.add_command(populate_machine_state)
    app.cli.add_command(change_machine_state)
    app.cli.add_command(add_broken_state)
    app.cli.add_command(add_fixed_state)
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
    # db.execute("ALTER TABLE user ADD COLUMN birth_date date")
    # db.commit()

    # click.echo('Altered the database.')

    cursor = db.cursor()
    cursor.execute("SELECT * FROM beverages_types")
    tableList = cursor.fetchall()
    for table in tableList:
        click.echo(table[0])
        click.echo(table[1])
        click.echo(table[2])
        click.echo(table[3])
        click.echo(table[4])

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

@click.command(name='select-min-milk-val')
@with_appcontext
def get_min_milk_val():
    db_local = get_db()
    tableList = db.execute("SELECT milk_quantity FROM beverages_types").fetchall()
    min_val = min([elem for elem in tableList])
    return  min_val

@click.command(name='select-min-coffee-val')
@with_appcontext
def get_min_coffee_val():
    db_local = get_db()
    tableList = db.execute("SELECT coffee_quantity FROM beverages_types").fetchall()
    min_val = min([elem for elem in tableList])
    return min_val

@click.command(name='select-syrup-val')
@with_appcontext
def get_syrup_val():
    db_local = get_db()
    return db.execute("SELECT syrup_quantity FROM machine_state").fetchall()
@click.command(name='populate-machine_state')
@with_appcontext
def populate_machine_state():
    db_local = get_db()
    db_local.execute(
        "INSERT INTO machine_state (coffee_quantity, milk_quantity, syrup_quantity, broken) VALUES (?, ?, ?, ?, ?)",
        (50, 50, 10, False)
    )
# register db functions to app
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(alter_db_command)
    app.cli.add_command(populateCoffeeTable)
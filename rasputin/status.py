from . import db

def get_status():
    user = db.get_db().execute(
        'SELECT id, username, birth_date'
        ' FROM user'
    ).fetchone()

    beverage = db.get_db().execute(
        'SELECT id, name, coffee_type, coffee_quantity'
        ' FROM beverages_types'
    ).fetchone()

    saved_coffee = db.get_db().execute(
        'SELECT id, user_id, beverage_id, roast_type'
        ' FROM preprogrammed_coffee'
    ).fetchone()

    if user is None:
        return {'status': 'Please create a user to start using the machine!'}

    if beverage is None:
        return {'status': 'Please select a beverage!'}

    if saved_coffee is None:
        return {'status': 'Add a beverage to Favorites to use this functionality!'}

    return {
        'data': {
            'user': user['username'],
            'beverage': {
                'name': beverage['name'],
                'coffee_quantity': beverage['coffee_quantity']
            },
            'saved_coffee': saved_coffee['roast_type']
        }
    }
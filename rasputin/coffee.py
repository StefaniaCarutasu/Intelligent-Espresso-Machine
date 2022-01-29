from rasputin import db


class BeverageType:
    def __init__(self, name, coffee_quantity, milk_quantity, milk_froth, roast_type, flavour):
        self.name = name
        self.coffee_quantity = coffee_quantity
        self.milk_quantity = milk_quantity
        self.milk_froth = milk_froth
        self.added_flavour = flavour
        self.roast_type = roast_type

    def changeCaffeineQuantity(self, caffeine_quantity):
        self.coffee_quantity = caffeine_quantity


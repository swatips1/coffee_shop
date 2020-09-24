from .database.models import db_drop_and_create_all, setup_db, Drink

# Function to return all drinks with just color and composition of each component of the recipe
def get_drinks():
    print('getting drinks')
    drinks = Drink.query.order_by('id').all()
    for drink in drinks:
        print("id:", drink.id)
    formmated_drinks = [drink.short() for drink in drinks]
    return formmated_drinks

# Function to return all drinks, with complete recipies
def get_detailed_drinks():
    print('getting drinks with details')
    drinks = Drink.query.order_by('id').all()
    for drink in drinks:
        print("id:", drink.id)
    formmated_drinks =''
    if drinks is not None:
        formmated_drinks = [drink.long() for drink in drinks]
    return formmated_drinks

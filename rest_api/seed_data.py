from pathlib import Path

from peewee import IntegrityError
from playhouse.dataset import DataSet

# Note that we can use a separate library here to interact with the same database

db = DataSet("sqlite:///user.db")
try:
    test_users_table = db["usertable"]
    test_users_table.insert(user_id='lucky.leprechaun', email='leprechaun@lucky.com', user_name='Lucky', user_last_name='Leprechaun')
    test_users_table.insert(user_id='mater.cars', email='mater@carsthemovie.com', user_name='Mater', user_last_name='Cars')

    test_picture_table = db["picturetable"]
    test_picture_table.insert(picture_id='0000000001', user_id='lucky.leprechaun', tags='#favoritecereal #stpats ')
    test_picture_table.insert(picture_id='0000000002', user_id='mater.cars', tags='#chevrolet #boomtruck ')
    
except IntegrityError:

    print(f"{Path(__file__).name} is already seeded, skipping")

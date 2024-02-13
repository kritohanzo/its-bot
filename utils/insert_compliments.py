from db import Database as db
from models import Compliment

with open('compliments.txt') as file:
    compliments = (string.strip() for string in file)

with db.session() as session:
    for compliment in compliments:
        compliment_obj = Compliment(text=compliment)
        session.add()
    session.commit()
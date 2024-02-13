from utils.models import Compliment

def insert_compliments(session):
    with open('compliments.txt', 'r') as file:
        compliments = (string.strip() for string in file.readlines())


    for compliment in compliments:
        compliment_obj = Compliment(text=compliment)
        session.add(compliment_obj)
    session.commit()
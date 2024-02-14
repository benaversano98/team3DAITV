from createdb import *
from date_from_csv import *


def inserisci_dati(connection):
    with open(r"csv\movies_pulito.csv", encoding='latin1', newline='') as input:
        lettore = csv.reader(input, delimiter=';')
        next(lettore)
        lista_movies = list(lettore)
    pop_movies = f"""
    INSERT INTO `movies`
    VALUES
    (%s, %s, %s, %s);
    """
    executemany_query(connection, pop_movies, lista_movies)

    with open(r"csv\users.csv", encoding='utf-8', newline='') as input:
        lettore = csv.reader(input, delimiter=',')
        next(lettore)
        lista_users = list(lettore)
        pop_users = f"""
           INSERT INTO `users`
           VALUES
           (%s, %s, %s, %s, %s);
           """
        executemany_query(connection, pop_users, lista_users)

        with open(r"csv\ratings.csv", encoding='utf-8', newline='') as input:
            lettore = csv.reader(input, delimiter=',')
            next(lettore)
            lista_ratings = list(lettore)
            pop_ratings = f"""
               INSERT INTO `ratings`
               VALUES
               ('', %s, %s, %s, %s);
               """
            executemany_query(connection, pop_ratings, lista_ratings)


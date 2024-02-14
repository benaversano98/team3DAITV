from createdb import *
from cleancsv import *


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

    with open(r"csv\genres.csv", encoding='latin1', newline='') as input:
        lettore = csv.reader(input, delimiter=';')
        next(lettore)
        lista_genres = list(lettore)
    pop_genres = f"""
        INSERT INTO `genres`
        VALUES
        (%s, %s);
        """
    executemany_query(connection, pop_genres, lista_genres)

    list_genres_movies = dati_puliti()[-1]
    pop_genres_movies = f"""
            INSERT INTO `genres_movies`
            VALUES
            ('',%s, %s);
            """
    executemany_query(connection, pop_genres_movies, list_genres_movies)


    with open(r"csv\users.csv", encoding='utf-8', newline='') as input:
        lettore = csv.reader(input, delimiter=',')
        next(lettore)
        lista_users = list(lettore)
        pop_users = f"""
           INSERT INTO `users`
           VALUES
           (%s, %s, %s, %s, %s, '');
           """
        executemany_query(connection, pop_users, lista_users)

    with open(r"csv\cap_zona.csv", encoding='utf-8', newline='') as input:
        lettore = csv.reader(input, delimiter=';')
        next(lettore)
        lista_cities = list(lettore)
        pop_cities = f"""
              INSERT INTO `cities`
              VALUES
              (%s, %s);
              """
        executemany_query(connection, pop_cities, lista_cities)

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


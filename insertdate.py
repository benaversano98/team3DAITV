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
    (%s, %s, %s, %s, 0);
    """
    executemany_query(connection, pop_movies, lista_movies)
    print("Fase 1")

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
    print("Fase 2")

    list_genres_movies = dati_puliti()[-1]
    pop_genres_movies = f"""
            INSERT INTO `genres_movies`
            VALUES
            ('',%s, %s);
            """
    executemany_query(connection, pop_genres_movies, list_genres_movies)
    print("Fase 3")

    with open(r"csv\users.csv", encoding='utf-8', newline='') as input:
        lettore = csv.reader(input, delimiter=',')
        next(lettore)
        lista_users = list(lettore)
        pop_users = f"""
           INSERT INTO `users`
           VALUES
           (%s, %s, %s, %s, %s, '', '');
           """
        executemany_query(connection, pop_users, lista_users)
    print("Fase 4")

    with open(r"csv\id_cap_provincia2.csv", encoding='utf-8', newline='') as input:
        lettore = csv.reader(input, delimiter=';')
        next(lettore)
        lista_cities = list(lettore)
        pop_cities = f"""
              INSERT INTO `cities`
              VALUES
              (%s,%s, %s);
              """
        executemany_query(connection, pop_cities, lista_cities)
    print("Fase 5")

    # cap = [(e[3],) for e in lista_users]
    cap = {e[1]: e[2] for e in lista_cities if e[1]}
    city = []
    for e in lista_users:
        city.append((cap[e[3]], e[3]))
    query = "UPDATE users SET city = %s WHERE cap= %s;"
    executemany_query(connection, query, city)


    with open(r"csv\ratings.csv", encoding='utf-8', newline='') as input:
        lettore = csv.reader(input, delimiter=',')
        next(lettore)
        lista_ratings = list(lettore)
        avg_ratings = {}
        for e in lista_ratings:
            if e[1] not in avg_ratings.keys():
                avg_ratings[e[1]] = [int(e[2]), 1]
            else:
                avg_ratings[e[1]][0] += int(e[2])
                avg_ratings[e[1]][1] += 1
        # for elem in avg_ratings.keys():
        #     avg_ratings[elem] = round(avg_ratings[elem][0] / avg_ratings[elem][1], 2)
        # avg_rating = list(avg_ratings.items())
        # avg_rating = [(avg_rating[i][1], avg_rating[i][0]) for i in range(len(avg_rating))]
        avg_ratings = {int(elem): round(avg_ratings[elem][0] / avg_ratings[elem][1], 2) for elem in avg_ratings.keys()}
        avg_ratings = list(avg_ratings.items())
        avg_ratings = [(avg_ratings[i][1], avg_ratings[i][0]) for i in range(len(avg_ratings))]
        pop_ratings = f"""
           INSERT INTO `ratings`
           VALUES
           ('', %s, %s, %s, %s);
           """
        executemany_query(connection, pop_ratings, lista_ratings)
        print("Fase 6")

        query = "UPDATE movies SET media_rating = %s WHERE movie_id = %s"
        executemany_query(connection, query, avg_ratings)
        print("Fase 7")

        trigger_media_rating = """
        CREATE TRIGGER media_valutazioni_add
        AFTER INSERT ON ratings
        FOR EACH ROW
        BEGIN
        UPDATE movies
        SET media_rating = (
            SELECT AVG(rating)
            FROM ratings
            WHERE movie_id = NEW.movie_id
        )
        WHERE movie_id=NEW.movie_id;
        END;
        """

        execute_query(connection, trigger_media_rating)

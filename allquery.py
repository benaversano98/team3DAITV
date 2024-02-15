from createdb import *


def query1(connection):
    query1 = "SELECT year, COUNT(*) as numero_film FROM `movies` GROUP BY year;"
    result = read_query(connection, query1)
    # return result
    print(result)


def query2(connection):
    query2 = """
    SELECT genres.genre, COUNT(*) as numero_film 
    FROM `movies` JOIN `genres_movies` JOIN `genres` 
    ON movies.movie_id = genres_movies.movie_id AND genres_movies.genre_id = genres.genre_id
    GROUP BY genres.genre;
    """
    result = read_query(connection, query2)
    print(result)


def query3(connection):
    query = "SELECT movie_id FROM movies WHERE media_rating < 3 AND media_rating > 0;"
    id_movie = read_query(connection, query)
    query = "SELECT movie_id, COUNT(ratings.user_id) FROM ratings WHERE movie_id=%s;"
    id_movie = readmany_query(connection, query, id_movie)
    dati = []
    for e in id_movie:
        if e[2] > 250:
            dati.append(e)


def query4(connection):
    fasciaeta = read_query(connection, "SELECT DISTINCT fasciaeta FROM users")
    sesso = read_query(connection, "SELECT DISTINCT gender FROM users")
    dati = [(e[0],f[0]) for f in sesso for e in fasciaeta]
    query = """
    SELECT users.fasciaeta, users.gender, movies.title, COUNT(ratings.user_id) as numero_visualizzazioni
    FROM movies JOIN ratings JOIN users
    ON movies.movie_id=ratings.movie_id AND ratings.user_id=users.user_id
    WHERE users.fasciaeta = %s AND users.gender= %s 
    GROUP BY movies.movie_id
    ORDER BY COUNT(ratings.user_id) DESC
    LIMIT 10;
    """
    result1 = readmany_query(connection, query, dati)
    print(result1)


def query5(connection):
    fasciaeta = read_query(connection, "SELECT DISTINCT fasciaeta FROM users")
    query = """
    SELECT movies.title, ROUND(CAST(AVG(ratings.rating) AS FLOAT), 2) as media_rating, users.fasciaeta
    FROM movies 
    JOIN ratings 
    ON movies.movie_id=ratings.movie_id
    JOIN users 
    ON ratings.user_id=users.user_id
    WHERE users.fasciaeta = %s
    GROUP BY movies.movie_id
    ORDER BY AVG(ratings.rating);
    """
    result1 = readmany_query(connection, query, fasciaeta)
    print(result1)

def query6(connection):
    query = """
    SELECT city, COUNT(city)
    FROM users
    GROUP BY city
    LIMIT 20;
    """
    result = read_query(connection, query)
